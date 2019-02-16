from telegram.ext import Updater, CommandHandler
from subprocess import call
import json, random

from gifgen import genAnimation
from failure_listener import startListener

with open("./config.json", "r") as fd:
	config = json.load(fd)

updater = Updater(config["telegram_token"])
currentlyBroken = []

def sendFailures(broken):
	global currentlyBroken

	if currentlyBroken == broken:
		return
	currentlyBroken = broken

	file = genAnimation(broken)
	with open(file, "r") as fd:
		updater.bot.send_animation(config["group_id"], fd)

def genAndRespond(update, broken):
	file = genAnimation(broken)
	with open(file, "r") as fd:
		res = update.message.reply_animation(fd)

def status(bot, update):
	genAndRespond(update, currentlyBroken)

def demo(bot, update):
	broken_bitset = random.randrange(1, 255)
	broken = []
	for i in range(0, 8):
		if broken_bitset & (1 << i):
			broken.append(i + 1)

	genAndRespond(update, broken)

startListener(config, sendFailures)

updater.dispatcher.add_handler(CommandHandler('status', status))
updater.dispatcher.add_handler(CommandHandler('demo', demo))

updater.start_polling()
updater.idle()
