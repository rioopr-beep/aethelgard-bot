import logging
import sqlite3
import random
import asyncio
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# === 1. PENGATURAN LOGGING (PENTING UNTUK MONITOR RAILWAY) ===
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# === 2. IDENTITAS BOT ===
TOKEN = '8507170484:AAHpgJC0jngZ7h1hDaG5UOyLoIoeQwvdhzI'
ADMIN_ID = 1408120389

# === 3. SISTEM DATABASE ===
def init_db():
    try:
        conn = sqlite3.connect('aethelgard.db')
        conn.execute('''CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY, 
            username TEXT, 
            aether INTEGER DEFAULT 1000)''')
        conn.commit()
        conn.close()
        logger.info("Database Aethelgard berhasil diinisialisasi.")
    except Exception as e:
        logger.error(f"Gagal inisialisasi database: {e}")

# === 4. MENU NAVIGASI ===
def get_menu(uid):
    buttons = [
        [KeyboardButton("🎰 Lotre Kerajaan"), KeyboardButton("🎁 Gaji")],
        [KeyboardButton("⚒️ Jalankan Quest"), KeyboardButton("🏆 Papan Peringkat")],
        [KeyboardButton("❓ Bantuan")]
    ]
    if uid == ADMIN_ID:
        buttons.append([KeyboardButton("👑 Kendali Penguasa")])
    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)

# === 5. LOGIKA PERINTAH ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    username = update.effective_user.first_name
    await update.message.reply_text(
        f"🏰 **ISTANA AETHELGARD ONLINE**\n\nSelamat datang kembali, **{username}**!\nSistem Cloud Railway telah aktif sepenuhnya.",
        reply_markup=get_menu(uid),
        parse_mode='Markdown'
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    uid = update.effective_user.id
    
    if "Gaji" in text:
        await update.message.reply_text("💰 **+1000 Aether** telah ditambahkan ke pundi-pundi Anda!")
    
    elif "Lotre" in text:
        hasil = random.choice(["MENANG! 🏆 (+500 Aether)", "KALAH! 💀 (-200 Aether)"])
        await update.message.reply_text(f"🎰 **Hasil Lotre:** {hasil}")
        
    elif "Quest" in text:
        await update.message.reply_text("⚒️ **Quest Selesai!** Pasukan Anda membawa pulang 200 Aether.")
        
    elif "Bantuan" in text:
        await update.message.reply_text("❓ **Butuh Titah?** Gunakan tombol menu di bawah untuk mengelola kerajaan.")

# === 6. EKSEKUSI SERVER (PUNCAK FINAL) ===
if __name__ == '__main__':
    # Inisialisasi Database
    init_db()
    
    try:
        # Membangun aplikasi dengan standar Railway/v20+
        application = ApplicationBuilder().token(TOKEN).build()
        
        # Menambahkan Handler
        application.add_handler(CommandHandler("start", start))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
        
        print("--- ⚡ AETHELGARD SUPREME ONLINE ⚡ ---")
        
        # Menjalankan Polling (drop_pending_updates=True sangat krusial di Cloud)
        application.run_polling(drop_pending_updates=True)
        
    except Exception as e:
        logger.error(f"Bot berhenti karena kesalahan: {e}")
