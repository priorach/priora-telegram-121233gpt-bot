import logging
import requests
from flask import Flask
from threading import Thread
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# === Замените на ваш токен ===
TELEGRAM_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"

# Веб-сервер Flask
app = Flask(__name__)

@app.route('/')
def home():
    return 'Бот работает!'

def run_flask():
    app.run(host='0.0.0.0', port=8080)

# Telegram-бот
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я бесплатный GPT-бот.")

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    try:
        response = requests.post(
            "https://api.aichat.cool/v1/chat/completions",
            headers={"Content-Type": "application/json"},
            json={
                "model": "gpt-3.5-turbo",
                "messages": [{"role": "user", "content": user_message}]
            }
        )
        data = response.json()
        reply = data["choices"][0]["message"]["content"]
        await update.message.reply_text(reply)
    except Exception as e:
        logger.error(f"Ошибка: {e}")
        await update.message.reply_text("Произошла ошибка при обращении к GPT.")

def run_telegram():
    app_tg = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app_tg.add_handler(CommandHandler("start", start))
    app_tg.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))
    app_tg.run_polling()

# Запуск
if __name__ == "__main__":
    Thread(target=run_flask).start()
    run_telegram()
