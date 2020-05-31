import os
import urllib
import uuid

import telebot
from webcolors import hex_to_rgb

from common.services.PaletteService import PaletteService

bot_token = os.environ['BOT_TOKEN']
bot = telebot.TeleBot(bot_token)

print(bot)


@bot.message_handler(content_types=['photo'])
def handle_docs_audio(message):
    try:
        reply_to = message.from_user.id
        file_id = message.photo[1].file_id

        file_info = bot.get_file(file_id)

        file_name = f'{str(uuid.uuid4())}.jpg'
        urllib.request.urlretrieve('https://api.telegram.org/file/bot{0}/{1}'
                                   .format(bot_token, file_info.file_path),
                                   file_name)

        res_path = PaletteService.get_image_with_palette(file_name, 4, 10, hex_to_rgb('#ffffff'))
        photo = open(res_path, 'rb')
        bot.send_photo(reply_to, photo)
        os.remove(file_name)
    except Exception:
        pass


while True:
    try:
        bot.polling()
    except Exception:
        pass

