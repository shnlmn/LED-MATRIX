import configparser

filename = 'config.ini'

config = configparser.RawConfigParser()
config.read(filename)

host = config.get('network', 'host')
port = config.getint('network', 'port')

w = config.getint('hardware', 'w')
h = config.getint('hardware', 'h')
LED_COUNT = config.getint('hardware', 'w')*config.getint('hardware', 'h')
LED_PIN = config.getint('hardware', 'LED_PIN')
LED_FREQ_HZ = config.getint('hardware', 'LED_FREQ_HZ')
LED_DMA = config.getint('hardware', 'LED_DMA')
LED_BRIGHTNESS = config.getint('hardware', 'LED_BRIGHTNESS')
LED_INVERT = config.getboolean('hardware', 'LED_INVERT')
LED_CHANNEL = config.getint('hardware', 'LED_CHANNEL')
LED_STRIP = config.get('hardware', 'LED_STRIP')




# Only store values that are supposed to be changes
def store():
	config.set('hardware', 'brightness', brightness)
	with open(filename, 'wb') as configfile:
   		config.write(configfile)