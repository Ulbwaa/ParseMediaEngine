from aiogram import types
from bs4 import BeautifulSoup


class Message:
    def __init__(self, text: str,
                 plain_text: str,
                 parse_mode: str,
                 media: (str, None),
                 reply_markup: (types.ReplyKeyboardMarkup, None)):
        self.is_media = media is not None
        self.text = text
        self.plain_text = plain_text
        self.parse_mode = parse_mode
        self.media = media
        self.reply_markup = reply_markup


class PME:
    def __init__(self):
        self.version = '1.0-release'
        self.result = Message

    def parser(self, text: str):
        soup = BeautifulSoup(text, features="html5lib")
        buttons = list()
        images = list()

        for tag in soup.find_all("img"):
            images.append(tag.get("source"))
            tag.decompose()

        for tag in soup.find_all("button"):
            buttons.append({"text": tag.text,
                            "url": tag.get('href')})
            tag.decompose()

        kb = None if len(buttons) < 1 else types.InlineKeyboardMarkup()

        for button in buttons:
            kb.row(
                types.InlineKeyboardButton(
                    text=button['text'],
                    url=button['url']
                )
            )

        media = images[0] if len(images) > 0 else None

        text_formatted = str(soup.body).replace("<body>", str()).replace("</body>", str())

        return self.result(
            text=text_formatted,
            plain_text=soup.text,
            parse_mode='html',
            media=media,
            reply_markup=kb
        )
