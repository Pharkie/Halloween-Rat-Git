"""
MP3 player using the I2S bus.
"""
import board
import audiomp3
import audiobusio
import random
import os
import time

def main():
    audio = audiobusio.I2SOut(board.GP0, board.GP1, board.GP2)

    folder_path = "/mp3"
    mp3s = []

    for filename in os.listdir(folder_path):
        if filename.endswith(".mp3"):
            mp3s.append(filename)

    if not mp3s:
        print("No mp3 files found in /mp3 directory")
        return

    last_mp3 = None
    mp3_file = None

    try:
        while True:
            # Select a random mp3 file that is different from the last one played
            while mp3_file == last_mp3:
                mp3_file = random.choice(mp3s)
            last_mp3 = mp3_file

            # Load and play the selected mp3 file
            mp3 = audiomp3.MP3Decoder(open(folder_path + os.sep + mp3_file, "rb"))
            audio.play(mp3)

            # Wait for a random amount of time between 5 and 10 seconds before playing the next mp3
            delay = random.randint(10, 20)
            time.sleep(delay)

    except KeyboardInterrupt:
        print("Program stopped by user")

if __name__ == "__main__":
    main()