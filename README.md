## Arcade Stacker Game
# Introduction
- For this project Josh Mitterling and Luke Wendel set out to make one of the favorite games to play at an arcade, Stacker.
- This project will show you how to wire up the circuit you need along with how to run the code in order to play.

# Hardware
- This project requires you to have the BeagleBone Black, 1 of the I2C 8x8 Bi-Color LED Matrix and, 1 pushbutton.
- The pushbutton is wired up to pin P9_23.
- The LED Matrix's "D" pin is wired up to P9_20 and the "C" pin is wired up to P9_19.
- Once you wired up the full circuit you are good to go

# Software
- In order to play this game, you must download this repo.
- Once downloaded, run the install.sh in order to install the Adafruit BBIO library
- After that all you need to do is run the Arcade_games.py script to start playing

# How to play
- The game is simple, you are trying to stack your bricks all the way to the top. In order to do this you need to put them on top of each other.
- You press the pushbutton to stop the brick from moving and place it in the spot that you stopped at.
- If a port of a brick you placed has nothing below it, then that part of the brick will fall.
- The game gets faster everytime that you successfully place a brick.
- If you make it all the way to the top, then you win. If you fail to, you lose.
- Once you are on the lose or win screen, press the button again to play again.
