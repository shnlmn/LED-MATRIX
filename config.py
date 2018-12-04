import configparser
import os
import sys

#filename = os.path.abspath(sys.argv[0]+"/../../")+'/config.ini'
filename = os.path.join(os.path.dirname(__file__), "config.ini")
#print(os.path.dirname(__file__))
#print(filename)

config = configparser.RawConfigParser()
config.read(filename)

def load(fixture):
    fixturevars = {
            "w": config.getint(fixture, 'w'),
            "h":config.getint(fixture, 'h'),
            "LED_COUNT":config.getint(fixture, 'w')*config.getint(fixture, 'h'),
            "LED_PIN":config.getint(fixture, 'LED_PIN'),
            "LED_FREQ_HZ":config.getint(fixture, 'LED_FREQ_HZ'),
            "LED_DMA":config.getint(fixture, 'LED_DMA'),
            "LED_BRIGHTNESS":config.getint(fixture, 'LED_BRIGHTNESS'),
            "LED_INVERT":config.getboolean(fixture, 'LED_INVERT'),
            "LED_CHANNEL":config.getint(fixture, 'LED_CHANNEL'),
            "LED_STRIP":config.get(fixture, 'LED_STRIP')
            }
    return(fixturevars)
# Only store values that are supposed to be changes
def store():
	config.set(fixture, 'brightness', brightness)
	with open(filename, 'wb') as configfile:
   		config.write(configfile)

if __name__ == "__main__":
    print(load('5x5'))
