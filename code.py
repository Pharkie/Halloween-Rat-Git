"""
MP3 player using the I2S bus.
"""
import os
import random
import time
import math
import board
import audiomp3
import audiobusio
import adafruit_rgbled
from digitalio import DigitalInOut, Direction, Pull

FOLDER_PATH = "/mp3"
audio = audiobusio.I2SOut(board.GP0, board.GP1, board.GP2)
# Create a RGB LED object
rgbled1 = adafruit_rgbled.RGBLED(board.GP10, board.GP11, board.GP12, invert_pwm=True)
rgbled2 = adafruit_rgbled.RGBLED(board.GP18, board.GP19, board.GP20, invert_pwm=True)

button = DigitalInOut(board.GP16)
button.direction = Direction.INPUT
button.pull = Pull.UP

COLOUR_RED = (255, 0, 0)
COLOUR_GREEN = (0, 255, 0)
COLOUR_BLUE = (0, 0, 255)
COLOUR_YELLOW = (255, 255, 0)
COLOUR_MAGENTA = (255, 0, 255)
COLOUR_CYAN = (0, 255, 255)
COLOUR_WHITE = (255, 255, 255)
COLOUR_ORANGE = (255, 165, 0)
COLOUR_PURPLE = (128, 0, 128)
COLOUR_PINK = (255, 192, 203)
COLOUR_OFF = (0, 0, 0)

EYE_COLOURS = [
    COLOUR_RED,
    COLOUR_GREEN,
    COLOUR_BLUE,
    COLOUR_YELLOW,
    COLOUR_MAGENTA,
    COLOUR_CYAN,
    COLOUR_WHITE,
    COLOUR_ORANGE,
    COLOUR_PURPLE,
    COLOUR_PINK
]

prev_eye_colour = None
button_last_value = button.value

def cycle_eyes():
    """Cycle both eyes through a circular rainbow pattern"""
    for i in range(256):
        r = int(255 * abs(math.sin(i / 255.0 * math.pi)))
        g = int(255 * abs(math.sin((i / 255.0 + 1.0 / 3.0) * math.pi)))
        b = int(255 * abs(math.sin((i / 255.0 + 2.0 / 3.0) * math.pi)))
        rgbled1.color = (r, g, b)
        rgbled2.color = (255 - r, 255 - g, 255 - b)
        time.sleep(0.001)

def flash_eyes(colour1, colour2, speed, eyes_together=True):
    """Flash both eyes with the given colours and speed"""
    sleep_time = (11 - speed) / 20.0 * 0.5

    if eyes_together:
        rgbled1.color = colour1
        rgbled2.color = colour1
        time.sleep(sleep_time)
        
        rgbled1.color = colour2
        rgbled2.color = colour2
        time.sleep(sleep_time)
    else:
        rgbled1.color = colour1
        rgbled2.color = colour2
        time.sleep(sleep_time)
        
        rgbled1.color = colour2
        rgbled2.color = colour1
        time.sleep(sleep_time)

def play_mp3(mp3_file):
    global prev_eye_colour
    global button_last_value

    # Load and play the selected mp3 file
    mp3 = audiomp3.MP3Decoder(open(FOLDER_PATH + os.sep + mp3_file, "rb"))
    audio.play(mp3)

    # Randomly select a new eye colour that is different from the previous one
    eye_colour = random.choice(list(set(EYE_COLOURS) - {prev_eye_colour}))

    # Randomly select a new eye function
    eye_function = random.choice([flash_eyes, flash_eyes, flash_eyes, cycle_eyes])

    # Randomly select the second eye colour and flash speed
    if random.random() < 0.5:
        eye_colour2 = COLOUR_OFF
        flash_speed = 10
    else:
        eye_colour2 = random.choice(list(set(EYE_COLOURS) - {eye_colour}))
        flash_speed = random.randint(1, 10)

    # Flash the LED while the MP3 is playing
    while audio.playing:
        # Call the selected function with the selected colours and speed
        if eye_function == cycle_eyes:
            eye_function()
        else:
            eye_function(eye_colour, eye_colour2, flash_speed, True)

        # Set the previous eye colour to the current one
        prev_eye_colour = eye_colour

        # Check if the button has been pressed
        if button.value != button_last_value:
            # Exit the loop if the button has been pressed
            break

    rgbled1.color = COLOUR_OFF
    rgbled2.color = COLOUR_OFF

def main():
    """Run my rat"""
    global button_last_value
    
    print("Running my Tory rat")

    play_mp3("startup.mp3")

    mp3s = []
    for filename in os.listdir(FOLDER_PATH):
        if filename.endswith(".mp3") and not filename.startswith("._"):
            mp3s.append(filename)

    # Only play startup.mp3 once, on boot
    mp3s.remove("startup.mp3")

    if not mp3s:
        print("No mp3 files found in /mp3 directory")
        return

    print(mp3s)

    last_mp3 = None
    mp3_file = None

    try:
        while True:
            # Wait for a random amount of time between 5 and 10 seconds before playing the next mp3
            delay = random.randint(5, 10)
            for i in range(delay * 10):
                if button.value != button_last_value: # Make the on/off button into a toggle switch
                    break
                time.sleep(0.1)
            
            button_last_value = button.value

            # Select a random mp3 file that is different from the last one played
            while mp3_file == last_mp3:
                mp3_file = random.choice(mp3s)
            last_mp3 = mp3_file

            # Load and play the selected mp3 file
            play_mp3(mp3_file)

    except KeyboardInterrupt:
        print("Program stopped by user")

if __name__ == "__main__":
    main()