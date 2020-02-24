import config
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import ephem


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log'
                    )


def main():
    mybot = Updater(config.TOKEN, request_kwargs=config.PROXY, use_context=False)
    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(CommandHandler("planet", ephem_planet))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))    
    mybot.start_polling() 
    mybot.idle()


def ephem_planet(bot, update):
    list_planets = ['Mercury', 'Venus', 'Earth', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune', 'Pluto']
    user_text = update.message.text.split()
    selected_planet = user_text[1].title()
    if selected_planet in list_planets and len(user_text) == 2:
        ephem_planet = getattr(ephem, selected_planet)()
        update.message.reply_text(str(ephem_planet))
    elif selected_planet in list_planets and len(user_text) == 3:
        ephem_coordinates_planet = getattr(ephem, selected_planet)()
        ephem_coordinates_planet.compute(user_text[2])
        update.message.reply_text(str(ephem.constellation(ephem_coordinates_planet)))
        print(ephem.constellation(ephem_coordinates_planet))


def greet_user(bot, update):
    text = 'Вызван /start'
    print(text)
    update.message.reply_text(text)


def talk_to_me(bot, update):
    pass
    # user_text = update.message.text 
    # print(user_text)
    # update.message.reply_text(user_text)


main()


