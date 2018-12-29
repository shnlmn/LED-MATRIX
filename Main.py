# Pi controller for LED Matrix
# displays options to a web page
# controls how the led matrix functions
# Made by Shane Leaman
__author__ = 'shaleaman'

# import modules
# from flask import Flask
import Perlin.perlin2d
from Video.gifplayer import GifPlayer
import Video.ytplayer 
from neopixel import *
from device_list import devices as dl
import sys
import os
import argparse
import config

players = {
            "perlin2d":{
                "file":"Perlin/perlin2d.py",
                "name":"Perlin noise color field",
                "desc":"Play perlin noise with web interface",
                "order": 0,
                "func": Perlin.perlin2d.play
                },
            "gifplayer":{
                "file":"Video/gifplayer.py",
                "name":"GIF Player",
                "desc":"Play GIF from local files or url",
                "order": 1,
                "func": GifPlayer

                },
            "ytplayer":{
                "file":"Video/ytplayer.py",
                "name":"YouTube Player",
                "desc":"Play a youtube video from url",
                "order": 2,
                "func": Video.ytplayer.play
                }
        }
# Collect info from argument
parser = argparse.ArgumentParser()
parser.add_argument('-c', action='store_true', help='clear the display on exit')
parser.add_argument('-profile', type=str, help='profile name from config.json')
args = parser.parse_args()
if not args.profile:
    print("no profile")
if args.c:
    signal.signal(signal.SIGINT, signal_handler)

def read_config():

    matrix_configs = config.read_sections()
    return matrix_configs

def load_config(type):

    # load fixture details from config
    fixture = config.load(args.profile)
    h = fixture["h"] # height of pixel matrix
    w = fixture["w"]  # width of pixel matrix



if __name__ == "__main__":

    print("LED COLOR MATRIX CONTROLLER")

    # READ CONFIGURATION LIST 
    config_list = read_config()

    # PRINT LIST    
    for i,section in enumerate(config_list,1):
        print("{}: {}".format(i, section))
    
    # PROMPT USER FOR SELECTION
    config_select = int(input("Select LED matrix configuration:"))
    seld_config = config.load(config_list[config_select-1])
    for k,v in seld_config.items():
        print(type(v), v)

    # SET STRIP TO CONFIG
    strip = Adafruit_NeoPixel(seld_config['LED_COUNT'],
                              seld_config['LED_PIN'], 
                              seld_config['LED_FREQ_HZ'],
                              seld_config['LED_DMA'],
                              seld_config['LED_INVERT'],
                              seld_config['LED_BRIGHTNESS'],
                              seld_config['LED_CHANNEL'],
                              seld_config['LED_STRIP'])

    strip.begin()
    #strip = Adafruit_NeoPixel(25, 18, 800000, 10, False, 255, 0, ws.WS2811_STRIP_GBR)
    # DISPLAY OPTIONS FOR PLAYERS
    for i, player in enumerate(sorted(players.keys(), key=lambda x: players[x]["order"]),1):
        print("{}: {} - {}".format(i,players[player]['name'], players[player]['desc']))

    # PROMPT USER FOR PLAYER SELECTION 
    player_select = int(input("Choose a player:"))
    seld_player = [v for v in players.values() if player_select-1 is v["order"]][0]
    player = seld_player['func'](strip, seld_config)
    player.play()
    print(seld_player['func'](strip, seld_config))


