from telegram.ext import Updater, CommandHandler
from subprocess import call
import random

from gifgen import genAnimation

def genAndRespond(update, broken):
    file = genAnimation(broken)
    with open(file, "r") as fd:
        update.message.reply_animation(fd)

def status(bot, update):
    genAndRespond(update, [])

def demo(bot, update):
    broken_bitset = random.randrange(1, 255)
    broken = []
    for i in range(0, 8):
        if broken_bitset & (1 << i):
            broken.append(i)

    genAndRespond(update, broken)

updater = Updater("614125047:AAHF18r1EaTd9KaveJnZIxsM3kT1mcu1QWw")

updater.dispatcher.add_handler(CommandHandler('status', status))
updater.dispatcher.add_handler(CommandHandler('demo', demo))

updater.start_polling()
updater.idle()
