# Auto137

There already is quite a bunch of programs doing the same, that is managing an automatic satellite receiving / decoding station aimed at NOAA / METEOR, but none worked the way I wanted it to... So was born Auto137, a python-based autonomous APT / LRPT / etc station made to easily support more options and be cleaner (only 1 language).

### What it does

This program, along with the necessary external tools and libraries, can do all this :
*  TLE fetching from Celestrak
*  Predict passes
*  Record satellites passes
*  Decode it
*  Pass conflict solving, including priorities
*  Easy support for other protocols
*  Multi-Threaded, decoding does not impact reception

All decoded data is saved into the chosen directory and an optional RSS feed can be enabled (no history saving to save on size).

### Requirements

* rtl_sdr (could be modified to use anything else)
* ffmpeg
* [noaa-apt](https://github.com/martinber/noaa-apt) (APT decoding)
* [Meteor M2 Demodulator](https://github.com/dbdexter-dev/meteor_demod) (QPSK demodulation)
* [LRPT Decoder](https://github.com/artlav/meteor_decoder) (LRPT image decoding)
* [satellitetle](https://gitlab.com/librespacefoundation/python-satellitetle) (TLE fetching)
* [orbit-predictor](https://github.com/satellogic/orbit-predictor) (Pass prediction)
* [pyyaml](https://github.com/yaml/pyyaml) (YAML config file)
* [apscheduler](https://github.com/agronholm/apscheduler) (Task scheduling)
* [PyRSS2Gen](http://dalkescientific.com/Python/PyRSS2Gen.html) (Rss feed generation)

### Installation

This procedure should work on any debian-based system (including Raspbian). If using anything else replace apt with your distro's package manager (eg. dnf, yum, pacman, opkg).

Start by installing all required packages through your package manager, including pip for other dependencies.

`sudo apt install ffmpeg rtl-sdr python3-pip python3-numpy`

Then install all python libraries.

`sudo pip3 install satellitetle orbit_predictor apscheduler pyyaml`

Now clone this git repo, edit the config file to your likings and start main.py using `python3 main.py`. If you experience an exception concerning `config = yaml.load(f, Loader=yaml.FullLoader)`, change it into `config = yaml.load(f)`.