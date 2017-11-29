# Raspberry Christmas Tree
Control your christmas tree with this simple program.

## Requirements
- Raspberry Pi
- Neopixel LED strip
- External 5v power supply for the LED strip
- Python 3

## Installation
1. Clone this project on your Raspberry
2. Follow the instructions on https://learn.adafruit.com/neopixels-on-raspberry-pi/software to install the required library
3. Wire up the hardware as explained on this page: https://learn.adafruit.com/neopixels-on-raspberry-pi/wiring
4. Check the `config.py` script and check if you need to change any settings
5. Run the server.py script as follows: `sudo python3 server.py` (yes, this needs to run as sudo since you need to be root to access the GPIO)
6. Open your browser on and go to `http://[raspberry ip]:8000/` (the port is configurable in the config file)

## Notes
If you want to add new sequences, you can place the text file in the `Sequences` directory and it'll be automatically updated. You don't have to restart the server for it to be recognized.

You can also test this program when you're not on a Raspberry Pi. You just need to set `NO_PI` to `True` in `config.py`.

## API
You can also control the strip with HTTP requests.

| Url                   | Method    | Description |
|-----------------------|-----------|-------------|
|`/get/sequences/`      | GET       | Get a list of available sequences, one item on each line |
|`/get/current/`        | GET       | Get the name of the currently running sequence |
|`/set/[name]`          | GET       | Play a sequence by name |
|`/set/`                | POST      | Play a sequence file that is passed as the body of the POST request |
|`/stop/`               | GET       | Stop any running sequence |