# Lucozade Halo Promotion Bot

## Installation and Setup
* `pip install -r requirements.txt`
* Download ChromeDriver from https://chromedriver.chromium.org/downloads and place executable in this directory
* Enter your information in config.json. Microsoft credentials are used to auto-login to Waypoint to
  redeem the XP codes as they are generated. `num_completed` is the total number of codes you have generated from Lucozade
  so far
  
## Running
* `python3 bot.py` or `python bot.py`
* It will sometimes pass the Captcha check, sometimes not, so you may need to monitor it on the side to manually
  complete the captcha, but that is the only manual interaction required.
* All generated codes will also be stored in `codes.txt` which will be created in this directory.

Different browser support coming...soon? Maybe?