#!/usr/bin/env python3

# Luke Wendel 12/13/22

import sys
import Adafruit_BBIO.GPIO as GPIO
import time
import smbus


GPIO.cleanup()

yMax = 8
xMax = 8
level = 0
size = [1,1,1]
change = 0
speed = 0.5
gaming = True
saved_indices = []
bounce = 40


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


def ISR_P9_23(channel):  # This is the ISR that's invoked when a pulse is detected
    
#
# Clear the interrupt and re-enable it for the next time
#
    GPIO.remove_event_detect("P9_23")
    time.sleep(0.1)
    GPIO.add_event_detect("P9_23", GPIO.RISING, callback=ISR_P9_23, bouncetime=bounce)

GPIO.setup("P9_23", GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect("P9_23", GPIO.RISING, callback=ISR_P9_23, bouncetime=bounce)



# Current position of the cursor
y = 0
x = 0

# Creating the etch-a-sketch grid space
grid = [[' ' for i in range(xMax)] for j in range (yMax)]


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



while gaming:
    for i in range(xMax - len(size)+1):
        print("here")
        if GPIO.input("P9_23") == 0:
            change = 1
            if level != 0:
                for l in range(len(size)):
                    if i == 0:
                        test = grid[level][i+l]
                        test2 = grid[level-1][i+l]
                    else:
                        test = grid[level][i-1+l]
                        test2 = grid[level-1][i-1+l]
                    if test != test2:
                        saved_indices.append(l)
                        for u in range(level):
                            if i == 0:
                                grid[level - u][i+l] = "0"
                                grid[level - (u+1)][i+l] = "*"
                            else: 
                                grid[level-u][i-1+l] = "0"
                                grid[level-(u+1)][i-1+l] = "*"
                            led_update(grid)
                            time.sleep(0.5)
                        if i == 0:
                            grid[0][i+l] = "0"
                        else:
                            grid[0][i-1+l] = "0"
                        led_update(grid)
            for t in range(len(saved_indices)):
                try: 
                    del size[saved_indices[t]]
                except:
                    del size[0]
            saved_indices = []
            level = level+1
            speed = speed - 0.005           
            break
        grid[level] = ["0" for x in grid[level]]
        for k in range(len(size)):
            grid[level][k+i] = "*"
        led_update(grid)
        time.sleep(speed)
    if size.count(1) == 0:
        gaming = False
        break
    for i in reversed(range(xMax - len(size)+1)):
        if change == 1:
            change = 0
            time.sleep(1)
            break
        if GPIO.input("P9_23") == 0:
            if level != 0:
                for l in reversed(range(len(size))):
                    if i == 5:
                        test = grid[level][i+l]
                        test2 = grid[level-1][i+l] 
                    else:   
                        test = grid[level][i+l+1]
                        test2 = grid[level-1][i+l+1]
                    if test != test2:
                        saved_indices.append(l)
                        for u in range(level):
                            if i == 5:
                                grid[level-u][i+l] = "0"
                                grid[level-(u+1)][i+l] = "*"   
                            else: 
                                grid[level-u][i+l+1] = "0"
                                grid[level-(u+1)][i+l+1] = "*"
                            led_update(grid)
                            time.sleep(0.5)
                        if i == 5:
                            grid[0][i+l] = "0"
                        else:
                            grid[0][i+l+1] = "0"   
                        led_update(grid)
            for t in range(len(saved_indices)):
                try: 
                    del size[saved_indices[t]]
                except:
                    del size[0]
            level = level+1
            speed = speed - 0.005                   
            break
        grid[level] = ["0" for x in grid[level]]
        for k in range(len(size)):
            grid[level][k+i] = "*"
        saved_indices = []
        led_update(grid)
        time.sleep(speed)
        if size.count(1) == 0:
            gaming = False
    
print("game over")