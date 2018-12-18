NO_PI = False

HTML_FILE = "WebFiles/index.html"
PORT = 80

REQUIRES_AUTH = False
USE_ADMIN_AUTH = True

AUTH_USER = "user"
AUTH_PASS = "pass"
AUTH_ADMIN_USER = "admin"
AUTH_ADMIN_PASS = "pass"

STARTUP_SEQUENCE = "red-green"
SEQUENCE_DIR = "Sequences/"
PLAYLIST_DIR = "Playlist/"

LED_COUNT = 30
LED_DATA_PIN = 18
LED_FREQ_HZ = 800000
LED_DMA = 5
LED_BRIGHTNESS = 255
LED_INVERT = False
LED_CHANNEL = 0

if not NO_PI:
    from neopixel import ws
    LED_STRIP = ws.WS2811_STRIP_GRB

VERBOSE_LOGGING = False
