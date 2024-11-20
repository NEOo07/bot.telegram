import telebot
import requests

TOKEN = "8040741265:AAF87QBPmyZ33a181Upjt5sgmjupYHQk_20"
bot = telebot.TeleBot(TOKEN)

def get_html_code(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        html_code = response.text
        return html_code
    except requests.RequestException:
        return None
        
@bot.message_handler(commands=['start'])
def start_command(message):
    chat_id = message.chat.id
    bot.send_message(
        chat_id,
        "لینکی ماڵپەڕەکەم بۆ بنێرە و بە ئاسانی فایلەکەی ماڵپەڕەکە دەهێنم.  .",
        reply_markup=create_inline_button("🗳️", "https://t.me/toolsneo")  # ضع رابط حسابك هنا
    )
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    chat_id = message.chat.id
    url = message.text.strip()
    if url.startswith("http://") or url.startswith("https://"):
        html_code = get_html_code(url)
        if html_code:
            file_path = "site_code.html"
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(html_code)
            with open(file_path, "rb") as file:
                bot.send_document(chat_id, file)
        else:
            bot.send_message(chat_id, "دڵنیابە بەستەرەکە ڕاستە یان سایتێکی دروستە .")
    else:
        bot.send_message(chat_id, "تکایە لینکی دروست بنێرە.   .")

def create_inline_button(text, url):
    markup = telebot.types.InlineKeyboardMarkup()
    button = telebot.types.InlineKeyboardButton(text=text, url=url)
    markup.add(button)
    return markup

bot.infinity_polling()