"""
MP3 player using the I2S bus.
"""
import board
import audiomp3
import audiobusio
import random

audio = audiobusio.I2SOut(board.GP0, board.GP1, board.GP2)

mp3s = ["cardiff.mp3", "standup-low.mp3", "slow.mp3"]
mp3_file = random.choice(mp3s)

mp3 = audiomp3.MP3Decoder(open(mp3_file, "rb"))

audio.play(mp3)
while audio.playing:
    pass

print("Done playing!")