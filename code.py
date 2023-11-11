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
WAIT_TIME = 5*60 # Seconds (+- 30%) to wait before playing the next mp3
WAIT_VARIANCE = 30/100 # 30% variance in wait time

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
    """Animate LED eyes with the given colours and speed"""
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

    # Randomly select an eye function with the specified weighting
    # 1 = flash_eyes fast with random colour
    # 2 = flash_eyes alternating at random speed with random colour
    # 3 = cycle_eyes
    r = random.random()

    if r < 0.6:
        eye_animation_choice = 1
    elif r < 0.8:
        eye_animation_choice = 2
        eye_colour2 = random.choice(list(set(EYE_COLOURS) - {eye_colour}))
        flash_speed = random.randint(1, 10)
    else:
        eye_animation_choice = 3

    # Flash the LED while the MP3 is playing
    while audio.playing:
        # Call the selected function with the selected colours and speed
        if eye_animation_choice == 1:
            # print("Animation 1")
            flash_eyes(eye_colour, COLOUR_OFF, 10, True)
        elif eye_animation_choice == 2:
            # print("Animation 2")
            flash_eyes(eye_colour, eye_colour2, flash_speed, False)
        elif eye_animation_choice == 3:
            # print("Animation 3")
            cycle_eyes()

        # Set the previous eye colour to the current one
        prev_eye_colour = eye_colour

        # Check if the button has been pressed
        if button.value != button_last_value:
            # Exit the loop if the button has been pressed
            audio.stop()
            break

    rgbled1.color = COLOUR_OFF
    rgbled2.color = COLOUR_OFF

def main():
    """Run my rat"""
    global button_last_value
    
    print("Running my Tory rat")

    try:
        play_mp3("startup.mp3")
    except OSError:
        print("The file 'startup.mp3' does not exist.")

    mp3s = []
    for filename in os.listdir(FOLDER_PATH):
        if filename.endswith(".mp3") and not filename.startswith("._"):
            mp3s.append(filename)

    # Only play startup.mp3 once, on boot
    if "startup.mp3" in mp3s:
        mp3s.remove("startup.mp3")

    if not mp3s:
        print("No mp3 files found in /mp3 directory")
        return
    else:
        print(mp3s)

    last_mp3 = None
    mp3_file = None

    try:
        while True:
            # Wait for a time before automatically playing the next mp3
            delay = random.randint(int(WAIT_TIME*(1-WAIT_VARIANCE)), int(WAIT_TIME*(1+WAIT_VARIANCE)))
            print(f"Delay set to {delay} seconds")

            for i in range(delay * 10):
                if button.value != button_last_value: # Make the on/off button into a toggle switch
                    break
                time.sleep(0.1)
            
            button_last_value = button.value

            if len(mp3s) == 1:
                # If there is only one mp3, play it and set last_mp3 to None
                mp3_file = mp3s[0]
            elif len(mp3s) == 2:
                # If there are only 2 mp3s, select the one that is different from the last one played
                mp3_file = mp3s[0] if mp3s[0] != last_mp3 else mp3s[1]
            else:
                # If there are more than 2 mp3s, select a random one that is different from the last one played
                while mp3_file == last_mp3:
                    mp3_file = random.choice(mp3s)

            last_mp3 = mp3_file

            # Load and play the selected mp3 file
            play_mp3(mp3_file)

    except KeyboardInterrupt:
        print("Program stopped by user")

if __name__ == "__main__":
    main()