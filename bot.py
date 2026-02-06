import logging
import sqlite3
import random
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# === KONFIGURASI LOGGING ===
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

TOKEN = '8507170484:AAHpgJC0jngZ7h1hDaG5UOyLoIoeQwvdhzI'
ADMIN_ID = 1408120389

# === DATABASE ===
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

# === COMMANDS ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    await update.message.reply_text(
        "🏰 **AETHELGARD CLOUD ONLINE**\nSistem berhasil bertakhta di Railway!", 
        reply_markup=get_menu(uid), 
        parse_mode='Markdown'
    )

async def handle_msg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    uid = update.effective_user.id
    
    responses = {
        "Gaji": "💰 +1000 Aether telah masuk ke kas Anda!",
        "Lotre": f"🎰 Hasil Lotre: {random.choice(['MENANG! +500', 'KALAH! -200'])}",
        "Quest": "⚒️ Quest berhasil! +200 Aether.",
        "Bantuan": "❓ Sistem Cloud aktif 24 jam.",
        "Peringkat": "🏆 Memuat data peringkat...",
        "Kendali Penguasa": "👑 Akses Penguasa Gemita Diterima."
    }
    
    for key, val in responses.items():
        if key in text:
            await update.message.reply_text(val)
            return

# === MAIN RUNNER ===
if __name__ == '__main__':
    init_db()
    
    # Membangun aplikasi dengan cara terbaru (v20+)
    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_msg))
    
    print("--- SERVER AETHELGARD DIAKTIFKAN ---")
    
    # Menjalankan bot
    app.run_polling(drop_pending_updates=True)
