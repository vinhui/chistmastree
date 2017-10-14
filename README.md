# Raspberry Christmas Tree
Control your christmas tree with this simple program.

## Requirements
- Raspberry Pi
- Neopixel LED strip
- External 5v power supply for the LED strip
- Python 3

## Installation
1. Clone this project on your Raspberry
2. Follow the instructions on this page https://learn.adafruit.com/neopixels-on-raspberry-pi/software to install the required library.
3. Wire up the hardware as explained on this page: https://learn.adafruit.com/neopixels-on-raspberry-pi/wiring
4. Check the `config.py` script and check if you need to change any settings
5. Run the server.py script as follows: `sudo python3 server.py`
6. Open your browser on and go to `http://[raspberry ip]:8000/`

## Notes
If you want to add new sequences, you can place the text file in the Sequences directory and it'll be automatically updated. You don't have to restart the server for it to be recognized.
