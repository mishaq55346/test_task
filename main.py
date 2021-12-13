import telegram.telegramBotHandler as telegram_bot
import skype.skypeBotHandler as skype_bot
import vk.vkBotHandler as vk_bot
import facebook.facebookBotHandler as facebook_bot
import threading

threading.Thread(telegram_bot.start()).start()
threading.Thread(facebook_bot_handler.start()).start()
#threading.Thread(vk_bot_handler.start()).start()
#threading.Thread(skype_bot_handler.start()).start()

