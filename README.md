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
New playlists can be added by placing a text file in the `Playlists` directory. Each line should contain the name of a sequence in the `Sequences` directory.

You can also test this program when you're not on a Raspberry Pi. You need to set `NO_PI` to `True` in `config.py` and you'll also need to install Tkinter: `sudo apt install python3-tk`. Tkinter needs to be installed for the window that will be used instead to show what otherwise would be on the LED strip.

## API
You can also control the strip with HTTP requests.

| Url              | Admin auth  | Method    | Description |
|------------------|----------------|-----------|-------------|
|`/get/sequences/` | No             | GET       | Get a list of available sequences, one item on each line |
|`/get/playlists/` | No             | GET       | Get a list of available playlists, one item on each line |
|`/get/current/`   | No             | GET       | Get the name of the currently running sequence |
|`/set/sequence/[name]`     | No             | GET       | Play a sequence by name |
|`/set/playlist/[name]`     | No             | GET       | Play a playlist by name |
|`/stop/`          | No             | GET       | Stop any running sequence |
|`/set/sequence/`           | Yes            | POST      | Play a sequence file that is passed as the body of the POST request |
|`/set/playlist/`      | Yes            | POST      | Play a playlist file that is passed as the body of the POST request |