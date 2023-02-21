#!/usr/bin/env python3

# Luke Wendel 1and Josh Mitterling 2/20/22
# A stack game that uses the I2C 8x8 Bi-color LED Matrix
# The goal of the game is to stack the bricks to the top without letting them all fall
# You use the one button in order to stop the brick
# When you win or lose, you hit the button again to restart the game

import sys
import Adafruit_BBIO.GPIO as GPIO
import time
import smbus


yMax = 8 #global variable for the y size of the matrix
xMax = 8 #global variable for the x size of the matrix
level = 0 #global variable for which row the game is on
size = [1,1,1] #global list for the size of the block that you are stopping
change = 0 #global variable to skip steps if the button has been pressed
speed = 0.1 #global variable for the speed of the block
gaming = True #global variable to see if the game is being played
saved_indices = [] #global list to see what indicies to delete from list "size"
bounce = 40 #global variable for debounce time for button
indicie = 0 #global variable for the current indicie  of the LED matrix
trigger = 0 #checks to see if the button interrupt as activated

win = [["*", "", "", "", "", "", "", "*"], #matrix screen for winning
        ["*", "*", "", "", "", "", "*", "*"],
        ["*", "", "*", "", "", "*", "", "*"],
        ["*", "", "", "*", "*", "", "", "*"],
        ["*", "", "", "", "", "", "", "*"],
        ["*", "", "", "", "", "", "", "*"],
        ["*", "", "", "", "", "", "", "*"],
        ["*", "", "", "", "", "", "", "*"]]
lose = [["", "", "*", "*", "*", "*", "*", "*"], #matrix screen for losing
        ["", "", "", "", "", "", "", "*"],
        ["", "", "", "", "", "", "", "*"],
        ["", "", "", "", "", "", "", "*"],
        ["", "", "", "", "", "", "", "*"],
        ["", "", "", "", "", "", "", "*"],
        ["", "", "", "", "", "", "", "*"],
        ["", "", "", "", "", "", "", "*"]]
perfect = [["", "", "", "", "", "", "", "*"], #matrix screen for perfect win
        ["", "", "", "", "", "", "", "*"],
        ["", "", "", "", "*", "*", "*", "*"],
        ["", "", "", "*", "", "", "", "*"],
        ["", "", "", "*", "", "", "", "*"],
        ["", "", "", "*", "", "", "", "*"],
        ["", "", "", "", "*", "", "", "*"],
        ["", "", "", "", "", "*", "*", "*"]]
firework1 = [["", "", "", "", "", "", "", ""], #matrix screen for beginning of firework
        ["", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", ""],
        ["", "", "", "*", "*", "", "", ""],
        ["", "", "", "*", "*", "", "", ""],
        ["", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", ""]]
firework2 = [["", "", "", "", "", "", "", ""], #matrix screen for middle of firework
        ["", "", "", "", "", "", "", ""],
        ["", "", "*", "*", "*", "*", "", ""],
        ["", "", "*", "", "", "*", "", ""],
        ["", "", "*", "", "", "*", "", ""],
        ["", "", "*", "*", "*", "*", "", ""],
        ["", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", ""]]
firework3 = [["", "", "", "", "", "", "", ""], #matrix screen for middle of firework
        ["", "*", "*", "*", "*", "*", "*", ""],
        ["", "*", "", "", "", "", "*", ""],
        ["", "*", "", "", "", "", "*", ""],
        ["", "*", "", "", "", "", "*", ""],
        ["", "*", "", "", "", "", "*", ""],
        ["", "*", "*", "*", "*", "*", "*", ""],
        ["", "", "", "", "", "", "", ""]]
firework4 = [["*", "*", "*", "*", "*", "*", "*", "*"], #matrix screen for ending of firework
        ["*", "", "", "", "", "", "", "*"],
        ["*", "", "", "", "", "", "", "*"],
        ["*", "", "", "", "", "", "", "*"],
        ["*", "", "", "", "", "", "", "*"],
        ["*", "", "", "", "", "", "", "*"],
        ["*", "", "", "", "", "", "", "*"],
        ["*", "*", "*", "*", "*", "*", "*", "*"]]


bus = smbus.SMBus(2)
matrix_address = 0x70
# set up the LED led_matrix
time.sleep(0.5)
bus.write_byte_data(matrix_address, 0x21, 0)
time.sleep(0.5)
bus.write_byte_data(matrix_address, 0x81, 0)
time.sleep(0.5)
bus.write_byte_data(matrix_address, 0xe7, 0)
time.sleep(0.5)

GPIO.setup("P9_23", GPIO.IN, pull_up_down=GPIO.PUD_UP) #set up the pushbutton as a pullup


def ISR_P9_23(channel):  # This is the ISR that's invoked when a pulse is detected
    global trigger
    trigger = 1
#
# Clear the interrupt and re-enable it for the next time
#
    GPIO.remove_event_detect("P9_23")
    time.sleep(0.1)
    GPIO.add_event_detect("P9_23", GPIO.FALLING, callback=ISR_P9_23, bouncetime=bounce)

#add event detect and event callback for button press
GPIO.add_event_detect("P9_23", GPIO.FALLING)
GPIO.add_event_callback("P9_23", ISR_P9_23, bouncetime=bounce)



# Creating the stacker virtual grid space
grid = [[' ' for i in range(xMax)] for j in range (yMax)]

# Function that updates the LED matrix based on the virtual grid space given
def led_update(grid):
    led_matrix = ["", "", "", "", "", "", "", ""]
    # binary for led led_matrix
    for i in range(len(grid)):
      for j in range(len(grid)):
        if grid[j][i] == '*':
          led_matrix[i] += '1'
        else:
          led_matrix[i] += '0'
    for i in range(len(led_matrix)):
      led_matrix[i] = int(led_matrix[i], 2)

    # make red
    block_data = []
    for i in range(len(led_matrix)):
      block_data.append(0)
      block_data.append(led_matrix[i])
    # write to the i2c bus
    bus.write_i2c_block_data(matrix_address, 0, block_data)

# Function that checks the position of the blocks
def check_blocks(reverse):
    global saved_indices
    global speed
    global level
    global change
    if reverse == 1: #determines which was the block was going
        if level != 0: #checks to make sure that its not the first level
            for l in reversed(range(len(size))):
                if indicie >= 5: #check if the indicie is on the end and prevents out of range errors
                    test = grid[level][i+l] #checks if the current brick indicie is lit up
                    test2 = grid[level-1][i+l] #checks if the brick under the current brick indicie is lit up
                else:   
                    test = grid[level][i+l+1] #checks if the current brick indicie is lit up
                    test2 = grid[level-1][i+l+1] #checks if the brick under the current brick indicie is lit up
                if test != test2: #go in this if the brick above and below are not both lit
                    saved_indices.append(l)
                    for u in range(level): #this for loop makes it so the brick falls all the way to the bottom and destroys everything in its path
                        if indicie >= 5:
                            grid[level-u][i+l] = "0"
                            grid[level-(u+1)][i+l] = "*"   
                        else: 
                            grid[level-u][i+l+1] = "0"
                            grid[level-(u+1)][i+l+1] = "*"
                        led_update(grid)
                        time.sleep(0.5) 
                    if indicie >= 5: #this destorys the falling brick when its on the bottom
                        grid[0][i+l] = "0"
                    else:
                        grid[0][i+l+1] = "0"   
                    led_update(grid)
        for t in range(len(saved_indices)): #this for loop deletes the indicies that did not have a lit brick beneath it
            try: 
                del size[saved_indices[t]] #some try excepts for out of range index errors
            except:
                try:
                    if size.count(1) == 1:
                        del size[0]
                except:
                    break
        level = level+1 #increases the level of the game
        speed = speed - 0.005 #increases the speed of the game                 
    else:
        change = 1
        if level != 0: #checks to make sure that its not the first level
            for l in range(len(size)):
                if indicie == 0: #check if the indicie is on the end and prevents out of range errors
                    test = grid[level][i+l] #checks if the current brick indicie is lit up
                    test2 = grid[level-1][i+l] #checks if the brick under the current brick indicie is lit up
                else:
                    test = grid[level][i-1+l] #checks if the current brick indicie is lit up
                    test2 = grid[level-1][i-1+l] #checks if the brick under the current brick indicie is lit up
                if test != test2: #go in this if the brick above and below are not both lit
                    saved_indices.append(l)
                    for u in range(level): #this for loop makes it so the brick falls all the way to the bottom and destroys everything in its path
                        if indicie == 0:
                            grid[level - u][i+l] = "0"
                            grid[level - (u+1)][i+l] = "*"
                        else: 
                            grid[level-u][i-1+l] = "0"
                            grid[level-(u+1)][i-1+l] = "*"
                        led_update(grid)
                        time.sleep(0.5)
                    if indicie == 0: #this destorys the falling brick when its on the bottom
                        grid[0][i+l] = "0"
                    else:
                        grid[0][i-1+l] = "0"
                    led_update(grid)
        for t in range(len(saved_indices)): #this for loop deletes the indicies that did not have a lit brick beneath it
            try: 
                del size[saved_indices[t]] #some try excepts for out of range index errors
            except:
                try:
                    if size.count(1) == 1:
                        del size[0]
                except:
                    break
        level = level+1 #increases the level of the game
        speed = speed - 0.005 #increases the speed of the game           
    saved_indices = []
while True: #Main Loop
    while gaming: #While loop that runs while the game is being played
        for i in range(xMax - len(size)+1): #loop that runs through the brick moving forth
            if trigger == 1: #check to see if the button was pressed
                check_blocks(0)
                trigger = 0
                break
            indicie = i #set the indicie of the brick
            try:
                grid[level] = ["0" for x in grid[level]] #set all the bricks in the level to be turned off
                for k in range(len(size)): #this for loops lights up the brick the size it needs to be
                    grid[level][k+i] = "*"
                led_update(grid)
                time.sleep(speed) #sleep for the amount of time the speed is set at
            except:
                gaming = False #if there is an index error on top you have won the game
                break 
            if size.count(1) == 0: #also if there is no bricks for you to stack left then you have lost the game
                gaming = False
                break  
        for i in reversed(range(xMax - len(size)+1)): #loop that runs through the brick moving back
            if gaming == False: #checks to see if the game has ended and breaks out of the while loop
                break
            if trigger == 1: #check to see if the button was pressed
                check_blocks(1)
                trigger = 0
                break
            indicie = i #set the indicie of the brick
            if change == 1: #checks to see if the button was pressed earlier to skip this code
                change = 0
                time.sleep(1)
                break
            try:
                grid[level] = ["0" for x in grid[level]] #set all the bricks in the level to be turned off
                for k in range(len(size)): #this for loops lights up the brick the size it needs to be
                    grid[level][k+i] = "*"
                led_update(grid)
                time.sleep(speed) #sleep for the amount of time the speed is set at
            except:
                gaming = False #if there is an index error on top you have won the game
                break
            if size.count(1) == 0: #also if there is no bricks for you to stack left then you have lost the game
                gaming = False
                break
    if size.count(1) == 0: #checks to see if you lost and plays the lose screen
        led_update(lose)
    elif size.count(1) == 3: #checks to see if you won perfectly and plays the perfect win screen
        led_update(firework1)
        time.sleep(0.5)
        led_update(firework2)
        time.sleep(0.5)
        led_update(firework3)
        time.sleep(0.5)
        led_update(firework4)
        time.sleep(0.5)
        led_update(perfect)
        time.sleep(0.5)
    else:
        led_update(firework1) #checks to see if you won and plays the win screen
        time.sleep(0.5)
        led_update(firework2)
        time.sleep(0.5)
        led_update(firework3)
        time.sleep(0.5)
        led_update(firework4)
        time.sleep(0.5)
        led_update(win)
        time.sleep(0.5)
    if trigger == 1: #waits for the button to be pressed again and restarts the game
        grid = [[' ' for i in range(xMax)] for j in range (yMax)]
        level = 0
        speed = 0.1
        saved_indicies = []
        size = [1,1,1]
        gaming = True
        indicie = 0
        change = 0
        trigger = 0