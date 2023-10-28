"""
MP3 player using the I2S bus.
"""
import os
import random
import time
import board
import audiomp3
import audiobusio
import adafruit_rgbled

FOLDER_PATH = "/mp3"

def play_mp3(mp3_file):
    # Load and play the selected mp3 file
    mp3 = audiomp3.MP3Decoder(open(FOLDER_PATH + os.sep + mp3_file, "rb"))
    audio.play(mp3)

    # Flash the LED while the MP3 is playing
    while audio.playing:
        rgbled.color = (0, 255, 0)
        time.sleep(0.1)
        rgbled.color = (0, 0, 0)
        time.sleep(0.1)

def main():
    """Run my rat"""
    print("Running my Tory rat")
    RED_LED = board.GP10
    GREEN_LED = board.GP11
    BLUE_LED = board.GP12

    # Create a RGB LED object
    rgbled = adafruit_rgbled.RGBLED(RED_LED, BLUE_LED, GREEN_LED, invert_pwm=True)

    audio = audiobusio.I2SOut(board.GP0, board.GP1, board.GP2)

    mp3s = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".mp3") and not filename.startswith("._"):
            mp3s.append(filename)

    if not mp3s:
        print("No mp3 files found in /mp3 directory")
        return

    print(mp3s)

    last_mp3 = None
    mp3_file = None

    try:
        while True:
            # Select a random mp3 file that is different from the last one played
            while mp3_file == last_mp3:
                mp3_file = random.choice(mp3s)
            last_mp3 = mp3_file

            # Load and play the selected mp3 file
            play_mp3(mp3_file)

            # Wait for a random amount of time between 5 and 10 seconds before playing the next mp3
            delay = random.randint(5, 10)
            time.sleep(delay)

    except KeyboardInterrupt:
        print("Program stopped by user")

if __name__ == "__main__":
    main()