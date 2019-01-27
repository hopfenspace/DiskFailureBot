# DiskFailureBot
Bot which sends blinking gifs when disks fail.

We wanted to have a Telegram bot which notifies everyone when one of the disks in a RAID dies. The idea came up to use a stock image of the server and simulate the broken disk blinking light.

## Setup

- Install dependencies
```sh
apt install python python-pip python-opencv imagemagick ffmpeg
pip install python-telegram-bot
```
- Edit `config.json`
- Find a good stock photo of your server
- Add disk LED coordinates to `gifgen.py`
- Run the bot using `python telegram_bot.py`

## Commands
- `/status` retrieve the current status of all disks
- `/demo` get a demo gif with randomly broken disks (it needs some way of showing off its coolness, even when all disks are operational)

## Examples

![](https://i.m4gnus.de/5a511.gif)
![](https://i.m4gnus.de/5a512.gif)
