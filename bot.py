import sqlite3
import random
import os
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# === 👑 IDENTITAS KERAJAAN ===
TOKEN = '8507170484:AAHpgJC0jngZ7h1hDaG5UOyLoIoeQwvdhzI'
ADMIN_ID = 1408120389

def init_db():
    conn = sqlite3.connect('aethelgard.db')
    conn.execute('''CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY, username TEXT, aether INTEGER DEFAULT 1000)''')
    conn.commit()
    conn.close()

def get_menu(uid):
    layout = [[KeyboardButton("🎰 Lotre Kerajaan"), KeyboardButton("🎁 Gaji")],
              [KeyboardButton("⚒️ Jalankan Quest"), KeyboardButton("🏆 Papan Peringkat")],
              [KeyboardButton("❓ Bantuan")]]
    if uid == ADMIN_ID: layout.append([KeyboardButton("👑 Kendali Penguasa")])
    return ReplyKeyboardMarkup(layout, resize_keyboard=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    await update.message.reply_text("🏰 **AETHELGARD CLOUD ONLINE**\nSistem berjalan di server pusat Railway.", 
                                   reply_markup=get_menu(uid), parse_mode='Markdown')

async def handle_msg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    uid = update.effective_user.id
    
    responses = {
        "Gaji": "💰 +1000 Aether telah masuk ke kas Anda!",
        "Lotre": f"🎰 Hasil Lotre: {random.choice(['MENANG! +500', 'KALAH! -200'])}",
        "Quest": "⚒️ Quest diselesaikan oleh pasukan bayaran Cloud. +200 Aether!",
        "Bantuan": "❓ Sistem Cloud aktif 24 jam. Gunakan tombol menu untuk titah.",
        "Peringkat": "🏆 Anda adalah penguasa tertinggi saat ini!",
        "Kendali Penguasa": "👑 Otoritas Gemita diakui oleh sistem."
    }
    
    for key, val in responses.items():
        if key in text:
            await update.message.reply_text(val)
            return

if __name__ == '__main__':
    init_db()
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_msg))
    print("Aethelgard is flying on Cloud!")
    app.run_polling(drop_pending_updates=True)

