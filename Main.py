# Pi controller for LED Matrix
# displays options to a web page
# controls how the led matrix functions
# Made by Shane Leaman
__author__ = 'shaleaman'

# import modules
# from flask import Flask
import Perlin.perlin2d
import Video.gifplayer
import Video.ytplayer 
import sys
import os
import argparse
import config


players = {
            "perlin2d":{
                "file":"Perlin/perlin2d.py",
                "name":"Perlin noise color field",
                "desc":"Play perlin noise with web interface"},
            "gifplayer":{
                "file":"Video/gifplayer.py",
                "name":"GIF Player",
                "desc":"Play GIF from local files or url"},
            "ytplayer":{
                "file":"Video/ytplayer.py",
                "name":"YouTube Player",
                "desc":"Play a youtube video from url"
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
    
    config_list = read_config()
    for i,section in enumerate(config_list,1):
        print("{}: {}".format(i, section))
    player_select = int(input("Select type of player:"))
    player = config.load(config_list[player_select-1])
    print(player)   
