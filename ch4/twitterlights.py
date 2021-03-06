#!/usr/bin/env python

import twit
import time

# Define this to NeoPixel or DotStar
type = "NeoPixel"
num_pixels = 7

# Set up whichever type of strip we're using:
if type == "DotStar":
    # For DotStars:
    from dotstar import Adafruit_DotStar, Color
    strip = Adafruit_DotStar(num_pixels, 12000000)
    strip.begin()

else:
    # For NeoPixels:
    from neopixel import Adafruit_NeoPixel, Color, ws

    # LED strip configuration:
    LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
    LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
    LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
    LED_BRIGHTNESS = 64      # Set to 0 for darkest and 255 for brightest
    LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
    LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
    LED_STRIP      = ws.WS2811_STRIP_GRB   # Strip type and colour ordering

    strip = Adafruit_NeoPixel(num_pixels, LED_PIN,
                              LED_FREQ_HZ, LED_DMA, LED_INVERT,
                              LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)

# Initialize the strip, whichever type it is:
strip.begin()

# Following topics:
topicwords = {
    'tech':   [ 'raspberry pi', 'linux', 'maker', 'arduino', 'open source', 'earthquake', 'eclipse', 'pyroclastic' ],
    'nature': [ 'bike', 'hike', 'bird', 'bear', 'trail', 'island', 'nature' ]
    }

topiccolors = {
    'nature': Color(  0, 255,   0),
    'tech':   Color(255,   0, 255),
    }

TWITTER_CHECK_TIME = 120       # How often to check Twitter
TIME_BETWEEN_PIXELS = .02      # Seconds from one pixel to the next
led_number = 0                 # Which LED are we setting right now?
tot_time = TWITTER_CHECK_TIME  # So we'll check immediately

twitapi = twit.init_twitter()

while True:
    if tot_time >= TWITTER_CHECK_TIME:
        keywords_found = twit.match_keywords(twitapi, topicwords)
        tot_time = 0
        print(keywords_found)

    tot_hits = sum(keywords_found[i] for i in keywords_found)
    if num_pixels % tot_hits == 0 or tot_hits % num_pixels == 0:
        keywords_found['blank'] = 1

    # Loop over the topics:
    for topic in keywords_found:
        # For this topic, keywords_found[topic] is the number of keywords
        # we matched on Twitter. Show that number of pixels.
        # The color for this topic is topiccolors[topic].
        for i in range(keywords_found[topic]):
            strip.setPixelColor(led_number, topiccolors[topic])
            strip.show()

            led_number = (led_number + 1) % num_pixels
            time.sleep(TIME_BETWEEN_PIXELS)
            tot_time += TIME_BETWEEN_PIXELS
