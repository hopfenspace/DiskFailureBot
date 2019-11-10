from telegram.ext import Updater, CommandHandler
from subprocess import call
import json, random

from gifgen import genAnimation
from failure_listener import startListener

with open("./config.json", "r") as fd:
	config = json.load(fd)

updater = Updater(config["telegram_token"])
currentlyBroken = []

def genCaption(broken):
	if len(broken) == 0:
		return "ALL DISKS OPERATIONAL"

	broken = sorted(broken)
	broken = map(str, broken)
	broken = ", ".join(broken)
	return "PLEASE REPLACE DISK(S) " + broken

def sendFailures(broken):
	global currentlyBroken

	if currentlyBroken == broken:
		return
	currentlyBroken = broken

	file = genAnimation(broken)
	with open(file, "rb") as fd:
		updater.bot.send_animation(config["group_id"], fd, caption=genCaption(broken))

def genAndRespond(update, broken):
	file = genAnimation(broken)
	with open(file, "rb") as fd:
		res = update.message.reply_animation(fd, caption=genCaption(broken))

def status(bot, update):
	genAndRespond(update, currentlyBroken)

def demo(bot, update):
	broken_bitset = random.randrange(1, 2 ** config["disk_count"])
	broken = []
	for i in range(0, config["disk_count"]):
		if broken_bitset & (1 << i):
			broken.append(i + 1)

	genAndRespond(update, broken)

startListener(config, sendFailures)

updater.dispatcher.add_handler(CommandHandler('status', status))
updater.dispatcher.add_handler(CommandHandler('demo', demo))

updater.start_polling()
updater.idle()
