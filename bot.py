import logging
import sqlite3
import random
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# === LOGGING SISTEM ===
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

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
    layout = [
        [KeyboardButton("🎰 Lotre Kerajaan"), KeyboardButton("🎁 Gaji")],
        [KeyboardButton("⚒️ Jalankan Quest"), KeyboardButton("🏆 Papan Peringkat")],
        [KeyboardButton("❓ Bantuan")]
    ]
    if uid == ADMIN_ID:
        layout.append([KeyboardButton("👑 Kendali Penguasa")])
    return ReplyKeyboardMarkup(layout, resize_keyboard=True)

# === LOGIKA PERINTAH ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    await update.message.reply_text(
        "🏰 **AETHELGARD CLOUD ONLINE**\n\nSelamat datang, Penguasa! Sistem telah berpindah sepenuhnya ke singgasana Cloud.",
        reply_markup=get_menu(uid),
        parse_mode='Markdown'
    )

async def handle_msg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    uid = update.effective_user.id
    
    # Respon cepat tanpa beban database berat
    if "Gaji" in text:
        await update.message.reply_text("💰 +1000 Aether telah masuk ke kas Anda!")
    elif "Lotre" in text:
        res = random.choice(["MENANG! +500", "KALAH! -200"])
        await update.message.reply_text(f"🎰 Hasil: {res}")
    elif "Quest" in text:
        await update.message.reply_text("⚒️ Quest selesai! +200 Aether.")
    elif "Bantuan" in text:
        await update.message.reply_text("📜 Gunakan tombol menu untuk memberikan perintah.")

# === EKSEKUSI UTAMA ===
if __name__ == '__main__':
    init_db()
    
    # Menggunakan ApplicationBuilder (Standar Railway/v20+)
    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_msg))
    
    print("--- ⚡ AETHELGARD SUPREME ONLINE ⚡ ---")
    
    # drop_pending_updates=True untuk membersihkan pesan macet sebelumnya
    app.run_polling(drop_pending_updates=True)
