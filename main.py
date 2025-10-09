import os
import re
import logging
import asyncio
import time
from flask import Flask
from threading import Thread
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
import yt_dlp
from datetime import datetime

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# --- Configuration ---
BOT_TOKEN = os.environ.get("BOT_TOKEN", "8275983870:AAGdsF0apIb57a5Oa3wumdUVLC9tLBIN-jQ")
CREATOR_HASHTAG = "#illusivehacks"
SUPPORTED_PLATFORMS = {
    'instagram': r'(https?://(?:www\.)?instagram\.com/(?:p|reel|stories)/)',
    'tiktok': r'(https?://(?:www\.|vm\.|vt\.)?tiktok\.com/)',
    'youtube': r'(https?://(?:www\.)?(?:youtube\.com/watch\?v=|youtu\.be/|youtube\.com/shorts/))',
    'twitter': r'(https?://(?:twitter\.com|x\.com)/[^/]+/status/\d+)'
}

# Platform emojis for aesthetic display
PLATFORM_EMOJIS = {
    'instagram': '📸',
    'tiktok': '🎵', 
    'youtube': '📺',
    'twitter': '🐦'
}

# Optimized yt-dlp settings for Koyeb
YT_DLP_OPTS = {
    'outtmpl': '/tmp/%(id)s.%(ext)s',
    'format': 'best[height<=720][ext=mp4]/best[ext=mp4]/best',
    'noplaylist': True,
    'no_warnings': True,
    'ignoreerrors': True,
    'quiet': True,
    'socket_timeout': 10,
    'retries': 3,
}

print("🚀 Starting LinkLift Bot on Koyeb...")

# Create Flask app for health checks
app = Flask(__name__)

@app.route('/')
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>LinkLift Bot - Active 🚀</title>
        <style>
            body { 
                font-family: Arial, sans-serif; 
                text-align: center; 
                padding: 50px; 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                color: white; 
            }
            .container { 
                background: rgba(255,255,255,0.1); 
                padding: 30px; 
                border-radius: 15px; 
                backdrop-filter: blur(10px);
            }
            h1 { font-size: 2.5em; margin-bottom: 20px; }
            .status { 
                font-size: 1.5em; 
                color: #00ff00; 
                font-weight: bold;
                animation: pulse 2s infinite;
            }
            @keyframes pulse {
                0% { opacity: 1; }
                50% { opacity: 0.7; }
                100% { opacity: 1; }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🔗 LinkLift Bot</h1>
            <div class="status">🟢 ONLINE & ACTIVE</div>
            <p>Telegram Social Media Downloader</p>
            <p>Powered by <strong>illusivehacks</strong></p>
            <p>🚀 Hosted on Koyeb - 24/7 Service</p>
        </div>
    </body>
    </html>
    """

@app.route('/health')
def health():
    return {"status": "healthy", "service": "LinkLift Bot", "timestamp": time.time()}

@app.route('/ping')
def ping():
    return "pong"

def run_flask():
    """Run Flask server in separate thread"""
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)

# === YOUR BOT FUNCTIONS === 
# [Keep ALL your existing functions exactly as they are - they're perfect!]
# start_command, help_command, button_handler, detect_platform, 
# download_video, handle_message, error_handler

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📸 Instagram", callback_data="help_instagram"),
         InlineKeyboardButton("🎵 TikTok", callback_data="help_tiktok")],
        [InlineKeyboardButton("📺 YouTube", callback_data="help_youtube"),
         InlineKeyboardButton("🐦 Twitter", callback_data="help_twitter")],
        [InlineKeyboardButton("⚡ Quick Start", callback_data="how_to_use")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    welcome_text = f"""
✨ *Welcome to LinkLift - Your Social Downloader!* ✨

*Hosted on Koyeb for 24/7 service* 🚀

⚡ *Lightning Fast Downloads From:*
📸 Instagram Reels/Posts/Stories
🎵 TikTok Videos  
📺 YouTube Videos/Shorts
🐦 Twitter/X Videos

💫 *Powered by* {CREATOR_HASHTAG}

Tap below for platform guides! 👇
    """
    
    await update.message.reply_text(
        welcome_text,
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = f"""
🆘 *Ultra-Fast Help Guide* 🆘

*Supported Platforms:*
• *Instagram*: Reels, Posts, Stories (⚡ Fastest)
• *TikTok*: All video formats (🚀 Instant)
• *YouTube*: Videos, Shorts (📺 HD Ready)
• *Twitter/X*: Video tweets (🐦 Quick)

*How to Download:*
1. Copy video link
2. Paste here
3. Watch magic happen! ✨

*Example Links:*
`https://www.instagram.com/reel/xxx/`
`https://www.tiktok.com/@user/video/xxx`
`https://youtube.com/shorts/xxx`
`https://twitter.com/user/status/xxx`

⚡ *Pro Tip:* I automatically optimize videos for fast delivery!

{CREATOR_HASHTAG} 💻
    """
    await update.message.reply_text(help_text, parse_mode='Markdown')

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    data = query.data
    
    if data == "how_to_use":
        text = """
🎯 *Ultra-Fast Usage:*
1. *Find video* on any supported platform
2. *Copy link* (share → copy)
3. *Paste here* - I'm lightning fast! ⚡
4. *Download* high-quality video instantly
5. *Enjoy* your content! 🎥

⚡ *Speed Optimized:* I use advanced techniques for fastest delivery!

Try me now with any link! 😊
        """
    elif data == "help_instagram":
        text = f"""
📸 *Instagram - Ultra Fast*
        
*Supported Content:*
• Reels (⚡ Optimized)
• Posts with videos
• Stories (public accounts)

*Download Speed:* ⚡⚡⚡⚡
*Quality:* High (auto-optimized)

*Example Links:*
`https://instagram.com/reel/Cxxx.../`
`https://instagram.com/p/Cxxx.../`

*Note:* I automatically handle large files for fast delivery!

{CREATOR_HASHTAG} ✨
        """
    elif data == "help_tiktok":
        text = f"""
🎵 *TikTok - Instant Download*

*Supported Content:*
• All TikTok videos
• With original audio
• High quality available

*Download Speed:* ⚡⚡⚡⚡⚡
*Quality:* Maximum available

*Example Links:*
`https://www.tiktok.com/@username/video/123456...`
`https://vm.tiktok.com/xyz...`

*Feature:* Fastest TikTok downloads in town! 🚀

{CREATOR_HASHTAG} ✨
        """
    elif data == "help_youtube":
        text = f"""
📺 *YouTube - Smart Download*

*Supported Content:*
• Regular videos
• YouTube Shorts (⚡ Fast)
• Music videos
• Smart quality selection

*Download Speed:* ⚡⚡⚡⚡
*Quality:* Optimized 720p for speed

*Example Links:*
`https://youtube.com/shorts/abc123...`
`https://youtu.be/abc123...`
`https://youtube.com/watch?v=abc123...`

*Smart Feature:* Auto-selects best quality for fast delivery!

{CREATOR_HASHTAG} ✨
        """
    elif data == "help_twitter":
        text = f"""
🐦 *Twitter/X - Quick Download*

*Supported Content:*
• Video tweets
• GIFs in tweets
• Multiple videos in single tweet

*Download Speed:* ⚡⚡⚡⚡
*Quality:* Original quality

*Example Links:*
`https://twitter.com/username/status/123456...`
`https://x.com/username/status/123456...`

*Note:* Lightning-fast Twitter video extraction!

{CREATOR_HASHTAG} ✨
        """
    else:
        text = "✨ Select an option from the menu above!"
    
    await query.edit_message_text(text=text, parse_mode='Markdown')

def detect_platform(url: str) -> str:
    for platform, pattern in SUPPORTED_PLATFORMS.items():
        if re.search(pattern, url):
            return platform
    return None

def download_video(url: str, platform: str) -> dict:
    ydl_opts = YT_DLP_OPTS.copy()
    
    if platform == 'youtube':
        ydl_opts['format'] = 'best[height<=720][ext=mp4]/best[ext=mp4]'
    elif platform == 'instagram':
        ydl_opts['format'] = 'best[ext=mp4]/best'
    elif platform == 'tiktok':
        ydl_opts['format'] = 'best[ext=mp4]'
    elif platform == 'twitter':
        ydl_opts['format'] = 'best[ext=mp4]/best'
    
    try:
        logger.info(f"🚀 Starting download from {platform}")
        start_time = datetime.now()
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            
            download_time = (datetime.now() - start_time).total_seconds()
            file_size = os.path.getsize(filename) / (1024 * 1024)
            
            logger.info(f"✅ Download completed in {download_time:.1f}s - {file_size:.1f}MB")
            
            return {
                'success': True,
                'filename': filename,
                'title': info.get('title', 'Social Media Video')[:100],
                'duration': info.get('duration', 0),
                'uploader': info.get('uploader', 'Unknown')[:50],
                'thumbnail': info.get('thumbnail', None),
                'file_size': os.path.getsize(filename),
                'download_time': download_time
            }
            
    except Exception as e:
        logger.error(f"❌ Download failed from {platform}: {e}")
        return {'success': False, 'error': str(e)}

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_text = update.message.text.strip()
    chat_id = update.message.chat_id
    user = update.message.from_user

    logger.info(f"👤 User {user.first_name} requested download")

    if not message_text.startswith('http'):
        await update.message.reply_text(
            f"👋 *Hey {user.first_name}!* ⚡\n\nSend me an Instagram, TikTok, YouTube, or Twitter link for instant download!\n\n{CREATOR_HASHTAG}",
            parse_mode='Markdown'
        )
        return

    platform = detect_platform(message_text)
    if not platform:
        await update.message.reply_text(
            f"❌ *Unsupported Link* ❌\n\nI support: 📸 Instagram • 🎵 TikTok • 📺 YouTube • 🐦 Twitter\n\nSend a valid link! ✨\n\n{CREATOR_HASHTAG}",
            parse_mode='Markdown'
        )
        return

    platform_emoji = PLATFORM_EMOJIS.get(platform, '📹')
    processing_message = await update.message.reply_text(
        f"⚡ *{platform_emoji} Processing {platform.title()}...*\n\n"
        f"🚀 Downloading at lightning speed...\n"
        f"📦 Optimizing for fast delivery...\n"
        f"🎯 Almost ready!\n\n"
        f"{CREATOR_HASHTAG}",
        parse_mode='Markdown'
    )

    try:
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(
            None, download_video, message_text, platform
        )
        
        if result['success']:
            file_size_mb = result['file_size'] / (1024 * 1024)
            
            if result['file_size'] > 50 * 1024 * 1024:
                await context.bot.edit_message_text(
                    chat_id=chat_id,
                    message_id=processing_message.message_id,
                    text=f"❌ *File Too Large* ❌\n\nThis video is {file_size_mb:.1f}MB. Telegram limit is 50MB. 😔\n\n{CREATOR_HASHTAG}",
                    parse_mode='Markdown'
                )
                try: os.remove(result['filename'])
                except: pass
                return
            
            await context.bot.edit_message_text(
                chat_id=chat_id,
                message_id=processing_message.message_id,
                text=f"📤 *Uploading...* ⚡\n\n"
                     f"📦 Size: {file_size_mb:.1f}MB\n"
                     f"⏱️ Download: {result.get('download_time', 0):.1f}s\n"
                     f"🚀 Sending now...\n\n"
                     f"{CREATOR_HASHTAG}",
                parse_mode='Markdown'
            )
            
            try:
                caption = (
                    f"✨ *Download Complete!* 🎉\n\n"
                    f"📝 *Title:* {result['title']}\n"
                    f"👤 *Uploader:* {result['uploader']}\n"
                    f"⏱️ *Duration:* {result['duration']}s\n"
                    f"📦 *Size:* {file_size_mb:.1f}MB\n"
                    f"⚡ *Platform:* {platform.title()} {platform_emoji}\n\n"
                    f"💫 *Powered by* {CREATOR_HASHTAG}\n"
                    f"🎊 *Enjoy your content!*"
                )
                
                await update.message.reply_video(
                    video=open(result['filename'], 'rb'),
                    caption=caption,
                    parse_mode='Markdown',
                    read_timeout=60,
                    write_timeout=60,
                    connect_timeout=30
                )
                
                await context.bot.edit_message_text(
                    chat_id=chat_id,
                    message_id=processing_message.message_id,
                    text=f"✅ *Download Successful!* 🎉\n\n"
                         f"📦 {file_size_mb:.1f}MB delivered in {result.get('download_time', 0):.1f}s\n"
                         f"⚡ Lightning fast service!\n\n"
                         f"{CREATOR_HASHTAG}",
                    parse_mode='Markdown'
                )
                
                logger.info(f"✅ Successfully delivered {platform} video to {user.first_name}")
                
            except asyncio.TimeoutError:
                await context.bot.edit_message_text(
                    chat_id=chat_id,
                    message_id=processing_message.message_id,
                    text=f"⏰ *Upload Timeout* ⚡\n\nFile is large but downloaded successfully! Try a shorter video next time. 😊\n\n{CREATOR_HASHTAG}",
                    parse_mode='Markdown'
                )
            
            try:
                os.remove(result['filename'])
            except Exception as e:
                logger.warning(f"Cleanup failed: {e}")
                
        else:
            await context.bot.edit_message_text(
                chat_id=chat_id,
                message_id=processing_message.message_id,
                text=f"❌ *Download Failed* ❌\n\nSorry {user.first_name}! 😔\n\n*Reason:* {result.get('error', 'Unknown error')}\n\n💡 Try another link!\n\n{CREATOR_HASHTAG}",
                parse_mode='Markdown'
            )

    except Exception as e:
        logger.error(f"💥 Unexpected error: {e}")
        try:
            await context.bot.edit_message_text(
                chat_id=chat_id,
                message_id=processing_message.message_id,
                text=f"⚡ *System Error* ⚡\n\nTemporary issue! Try again in a moment. 😊\n\n{CREATOR_HASHTAG}",
                parse_mode='Markdown'
            )
        except:
            await update.message.reply_text(
                f"⚡ *Temporary Error* ⚡\n\nPlease try again! 😊\n\n{CREATOR_HASHTAG}",
                parse_mode='Markdown'
            )

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.error(f"🚨 Bot error: {context.error}")
    
    if update and update.effective_message:
        await update.effective_message.reply_text(
            f"⚡ *Quick Recovery* ⚡\n\nMinor hiccup! I'm back and ready. Send me a link! 😊\n\n{CREATOR_HASHTAG}",
            parse_mode='Markdown'
        )

def main():
    print("🚀 Starting LinkLift Bot with Web Server...")
    
    # Start Flask server in background thread
    flask_thread = Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()
    print("🌐 Flask server started - Ready for health checks")
    
    # Start Telegram Bot
    try:
        application = Application.builder().token(BOT_TOKEN).build()
        
        application.add_handler(CommandHandler("start", start_command))
        application.add_handler(CommandHandler("help", help_command))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
        application.add_handler(CallbackQueryHandler(button_handler))
        application.add_error_handler(error_handler)
        
        print("🎉 LINKLIFT BOT STARTED SUCCESSFULLY!")
        print("📸 Supporting: Instagram, TikTok, YouTube, Twitter")
        print(f"💫 Creator: {CREATOR_HASHTAG}")
        print("🚀 Hosted on Koyeb - 24/7 Service Active!")
        
        application.run_polling()
        
    except Exception as e:
        logger.error(f"Failed to start bot: {e}")
        print(f"❌ Bot startup failed: {e}")

if __name__ == '__main__':
    main()