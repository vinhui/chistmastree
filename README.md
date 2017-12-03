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
6. Open your browser on and go to `http://[raspberry ip]/` (the port is configurable in the config file)

## Authentication
__Change the username and password in the config file!__
You can enable the requirement for authentication in the config file. Enabling this will require the user to login to access any page. By default there is some functionality that is only for admins, this can be disabled. Authentication is done with [HTTP Basic Auth](https://en.wikipedia.org/wiki/Basic_access_authentication).
If you have `REQUIRES_AUTH` set to `False`, you can go to `http://[raspberry ip]/auth` to login as admin.

## Notes
If you want to add new sequences, you can place the text file in the `Sequences` directory and it'll be automatically updated. You don't have to restart the server for it to be recognized.

You can also test this program when you're not on a Raspberry Pi. You need to set `NO_PI` to `True` in `config.py` and you'll also need to install Tkinter: `sudo apt install python3-tk`. Tkinter needs to be installed for the window that will be used instead to show what otherwise would be on the LED strip.

## API
You can also control the strip with HTTP requests.

| Url              | Admin auth  | Method    | Description |
|------------------|----------------|-----------|-------------|
|`/get/sequences/` | No             | GET       | Get a list of available sequences, one item on each line |
|`/get/current/`   | No             | GET       | Get the name of the currently running sequence |
|`/set/[name]`     | No             | GET       | Play a sequence by name |
|`/set/`           | Yes            | POST      | Play a sequence file that is passed as the body of the POST request |
|`/stop/`          | No             | GET       | Stop any running sequence |