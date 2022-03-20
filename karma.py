###
# Kopyleft 2022, SirVo
# All rights unreserved.
###

import re
from sopel.plugin import search, require_admin, rate
from sopel.module import commands, example

KPLUS = "karmaplus"
KMINUS = "karmaminus"

nonAdminMSG="This command requires bot admin privileges."

# using regex instead of a plain command allows for fun things like
# incrementing karma++ in the start/middle of a line
# or catching karma changes from users connected via bridge bot
@rate(user=1)
@search('(\w+)(\+\+|\-\-)')
@example("<nick>++ to increment, or <nick>-- to decrement, i.e. Sopel++")
def giveKarma(bot, trigger):
    """Increases/decreases a user's karma - no spaces allowed"""
    nick = trigger.group(1)
    nickdb = nick.lower()
    change = [0,1][trigger.group(2) == '++']
    
    # command user matches karma target - or multiple karma in single line
    if (nickdb == trigger.nick.lower()) or trigger.count(['--','++'][change]) > 1 or ('--' in trigger and '++' in trigger):
        bot.reply("Nice try.")
        return

    try:
        current_plus = int(bot.db.get_nick_value(nickdb, KPLUS, 0))
        current_minus = int(bot.db.get_nick_value(nickdb, KMINUS, 0))
    except NameError:
        current_plus, current_minus = 0, 0

    if change > 0:
        bot.db.set_nick_value(nickdb, KPLUS, current_plus + 1)
        karma_val = int(current_plus - current_minus + 1)
    else:
        bot.db.set_nick_value(nickdb, KMINUS, current_minus + 1)
        karma_val = int(current_plus - current_minus - 1)
    
    bot.say("%s's karma is now %d" % (nick, karma_val))

@commands("karma")
@example(".karma buddha")
def getKarma(bot, trigger):
    """Display current karma of <nick>"""

    nick = trigger.group(2) or trigger.nick
    nickdb = nick.lower().strip()
    
    try:
        current_plus = int(bot.db.get_nick_value(nickdb, KPLUS, 0))
        current_minus = int(bot.db.get_nick_value(nickdb, KMINUS, 0))
    except NameError:
        current_plus, current_minus = 0, 0

    if current_plus or current_minus:
        bot.say('Karma for "%s" has been increased %d times and decreased %d times for a total karma of %d.'  % (nick, current_plus, current_minus, current_plus - current_minus))
    else:
        bot.say('%s has not gained or lost any karma.' % nick)

@require_admin(message=nonAdminMSG, reply=True)
@commands("wipekarma")
@example(".wipekarma <nick>")
def wipeKarma(bot, trigger):
    """Deletes the karma entries for <nick>"""
    nick = trigger.group(2)

    if ' ' in nick:
        bot.reply('Syntax: Nick contains spaces.')
        return

    nickdb = nick.lower().strip()

    bot.db.delete_nick_value(nickdb, KPLUS)
    bot.db.delete_nick_value(nickdb, KMINUS)

    bot.reply('Karma for %s has been wiped.' % nick)

@require_admin(message=nonAdminMSG, reply=True)
@commands("setkarma")
@example(".setkarma <nick> <incremented> <decremented>")
def setKarma(bot, trigger):
    """Sets the karma entries for <nick>"""

    if trigger.group(2).count(' ') > 2:
        bot.reply('Too many arguments. Syntax: .set <nick> <incremented> <decremented>')

    nick = trigger.group(3)
    nickdb = nick.lower()
    inc = trigger.group(4)
    dec = trigger.group(5)
    
    try:
        inc = int(inc)
        dec = int(dec)
    except ValueError:
        bot.reply("Give integer values for <incremented> and <decremented>, i.e. .set Sopel 69 33")

    bot.db.set_nick_value(nickdb, KPLUS, inc)
    bot.db.set_nick_value(nickdb, KMINUS, dec)

    bot.reply('Karma set - nick: %s inc: %s dec: %s' % (nick, inc, dec))

##TODO: Dump/backup command
##      Import command
