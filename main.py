import os
import re
import logging
import asyncio
import time
import random
import requests
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

# Focus on platforms that work
SUPPORTED_PLATFORMS = {
    'tiktok': r'(https?://(?:www\.|vm\.|vt\.)?tiktok\.com/)',
    'youtube': r'(https?://(?:www\.)?(?:youtube\.com/watch\?v=|youtu\.be/|youtube\.com/shorts/))',
    'twitter': r'(https?://(?:twitter\.com|x\.com)/[^/]+/status/\d+)'
}

PLATFORM_EMOJIS = {
    'tiktok': '🎵', 
    'youtube': '📺',
    'twitter': '🐦'
}

# UPDATED yt-dlp settings with latest fixes
YT_DLP_OPTS = {
    'outtmpl': '/tmp/%(id)s.%(ext)s',
    'format': 'best[ext=mp4]/best',
    'noplaylist': True,
    'no_warnings': False,
    'ignoreerrors': False,
    'quiet': False,
    'socket_timeout': 30,
    'retries': 10,
    'fragment_retries': 10,
    'skip_unavailable_fragments': True,
    'extractor_retries': 5,
}

print("🚀 Starting ULTRA LinkLift Bot with Advanced IP Protection...")

# Advanced IP Rotation System
class IPProtection:
    def __init__(self):
        self.proxies = self.get_proxy_list()
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/120.0',
        ]
    
    def get_proxy_list(self):
        """Get working proxies"""
        return [
            # Residential proxies (more likely to work)
            {'http': 'http://138.197.157.32:8080', 'https': 'http://138.197.157.32:8080'},
            {'http': 'http://165.227.121.37:80', 'https': 'http://165.227.121.37:80'},
            {'http': 'http://167.71.5.83:8080', 'https': 'http://167.71.5.83:8080'},
            {'http': 'http://68.183.230.184:8080', 'https': 'http://68.183.230.184:8080'},
            {'http': 'http://159.203.61.169:8080', 'https': 'http://159.203.61.169:8080'},
            None,  # Sometimes no proxy works better
        ]
    
    def get_random_proxy(self):
        return random.choice(self.proxies)
    
    def get_random_user_agent(self):
        return random.choice(self.user_agents)
    
    def test_proxy(self, proxy):
        """Test if proxy is working"""
        try:
            if not proxy:
                return True
            response = requests.get('http://httpbin.org/ip', proxies=proxy, timeout=10)
            return response.status_code == 200
        except:
            return False

# Initialize IP protection
ip_protection = IPProtection()

# Flask app
app = Flask(__name__)

@app.route('/')
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>LinkLift Pro - Active</title>
        <style>
            body { font-family: Arial; text-align: center; padding: 50px; 
                   background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; }
            .container { background: rgba(255,255,255,0.1); padding: 30px; border-radius: 15px; }
            .status { color: #00ff00; font-weight: bold; font-size: 1.5em; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🔗 LinkLift Pro</h1>
            <div class="status">🟢 ACTIVE WITH IP PROTECTION</div>
            <p>Advanced Social Media Downloader</p>
            <p>Powered by <strong>illusivehacks</strong></p>
        </div>
    </body>
    </html>
    """

@app.route('/health')
def health():
    return {"status": "healthy", "ip_protection": "active", "timestamp": time.time()}

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)

# === UPDATED BOT FUNCTIONS === 

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🎵 TikTok", callback_data="help_tiktok"),
         InlineKeyboardButton("📺 YouTube", callback_data="help_youtube")],
        [InlineKeyboardButton("🐦 Twitter", callback_data="help_twitter"),
         InlineKeyboardButton("⚡ Quick Start", callback_data="how_to_use")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    welcome_text = f"""
✨ *Welcome to LinkLift Pro!* ✨

*Advanced Social Media Downloader with IP Protection*

🚀 *Reliable Downloads From:*
🎵 **TikTok** - Advanced extraction
📺 **YouTube/Shorts** - HD quality  
🐦 **Twitter/X** - Fast downloads

🔒 *Advanced Features:*
• IP Rotation System
• Anti-Block Technology
• Smart Retry Logic
• Professional Grade

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
🆘 *LinkLift Pro Help Guide* 🆘

*Supported Platforms:*
• *TikTok*: All videos (🎵 Advanced)
• *YouTube*: Videos & Shorts (📺 HD)  
• *Twitter/X*: Video tweets (🐦 Fast)

*How to Download:*
1. Copy TikTok, YouTube, or Twitter link
2. Paste here
3. Get instant download!

*Example Links:*
`https://www.tiktok.com/@user/video/xxx`
`https://youtube.com/shorts/xxx`
`https://twitter.com/user/status/xxx`

🔒 *Advanced Protection:*
• Automatic IP rotation
• Anti-detection technology
• Smart retry system

{CREATOR_HASHTAG} 🚀
    """
    await update.message.reply_text(help_text, parse_mode='Markdown')

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    data = query.data
    
    if data == "how_to_use":
        text = "🎯 Send me any TikTok, YouTube, or Twitter link for instant download!"
    elif data == "help_tiktok":
        text = "🎵 Send TikTok video links - Advanced extraction enabled!"
    elif data == "help_youtube":
        text = "📺 Send YouTube/Shorts links - HD quality guaranteed!"
    elif data == "help_twitter":
        text = "🐦 Send Twitter video links - Fast extraction!"
    else:
        text = "✨ Select an option!"
    
    await query.edit_message_text(text=text, parse_mode='Markdown')

def detect_platform(url: str) -> str:
    for platform, pattern in SUPPORTED_PLATFORMS.items():
        if re.search(pattern, url):
            return platform
    return None

def download_with_protection(url: str, platform: str) -> dict:
    """Download with advanced IP protection and retry logic"""
    max_attempts = 3
    
    for attempt in range(max_attempts):
        try:
            ydl_opts = YT_DLP_OPTS.copy()
            
            # Platform-specific settings
            if platform == 'youtube':
                ydl_opts['format'] = 'best[height<=720][ext=mp4]/best[ext=mp4]'
            elif platform == 'tiktok':
                ydl_opts['format'] = 'best[ext=mp4]'
            elif platform == 'twitter':
                ydl_opts['format'] = 'best[ext=mp4]/best'
            
            # IP Protection for this attempt
            proxy = ip_protection.get_random_proxy()
            user_agent = ip_protection.get_random_user_agent()
            
            if proxy and ip_protection.test_proxy(proxy):
                ydl_opts['proxy'] = proxy['http']
                logger.info(f"🛡️ Attempt {attempt+1}: Using proxy for {platform}")
            else:
                logger.info(f"🛡️ Attempt {attempt+1}: Direct connection for {platform}")
            
            # Enhanced headers
            ydl_opts['http_headers'] = {
                'User-Agent': user_agent,
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                'Cache-Control': 'max-age=0',
            }
            
            logger.info(f"🚀 Attempt {attempt+1} for {platform}")
            start_time = datetime.now()
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                # Force update extractors
                ydl._update_extractors()
                
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)
                
                download_time = (datetime.now() - start_time).total_seconds()
                file_size = os.path.getsize(filename) / (1024 * 1024)
                
                logger.info(f"✅ Success on attempt {attempt+1}: {download_time:.1f}s - {file_size:.1f}MB")
                
                return {
                    'success': True,
                    'filename': filename,
                    'title': info.get('title', 'Video')[:100],
                    'duration': info.get('duration', 0),
                    'uploader': info.get('uploader', 'Unknown'),
                    'file_size': os.path.getsize(filename),
                    'download_time': download_time,
                    'attempt': attempt + 1
                }
                
        except Exception as e:
            logger.warning(f"⚠️ Attempt {attempt+1} failed: {str(e)[:200]}")
            
            if attempt < max_attempts - 1:
                wait_time = random.uniform(2, 5)
                logger.info(f"⏳ Waiting {wait_time:.1f}s before retry...")
                time.sleep(wait_time)
                continue
    
    logger.error(f"❌ All {max_attempts} attempts failed for {platform}")
    return {'success': False, 'error': f'All download attempts failed for {platform}'}

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_text = update.message.text.strip()
    chat_id = update.message.chat_id
    user = update.message.from_user

    logger.info(f"👤 User {user.first_name} requested download")

    if not message_text.startswith('http'):
        await update.message.reply_text(
            f"👋 *Hey {user.first_name}!* 🚀\n\nSend me a TikTok, YouTube, or Twitter link for advanced download!\n\n{CREATOR_HASHTAG}",
            parse_mode='Markdown'
        )
        return

    platform = detect_platform(message_text)
    if not platform:
        await update.message.reply_text(
            f"❌ *Unsupported Platform* ❌\n\nI support: 🎵 TikTok • 📺 YouTube • 🐦 Twitter\n\nSend a valid link! ✨\n\n{CREATOR_HASHTAG}",
            parse_mode='Markdown'
        )
        return

    platform_emoji = PLATFORM_EMOJIS.get(platform, '🎬')
    
    processing_message = await update.message.reply_text(
        f"⚡ *{platform_emoji} Advanced {platform.title()} Processing...*\n\n"
        f"🛡️ Activating IP protection...\n"
        f"🚀 Starting secure download...\n"
        f"🎯 Advanced extraction...\n\n"
        f"{CREATOR_HASHTAG}",
        parse_mode='Markdown'
    )

    try:
        # Add small delay to appear more human-like
        await asyncio.sleep(random.uniform(1, 2))
        
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(
            None, download_with_protection, message_text, platform
        )
        
        if result['success']:
            file_size_mb = result['file_size'] / (1024 * 1024)
            
            if result['file_size'] > 50 * 1024 * 1024:
                await context.bot.edit_message_text(
                    chat_id=chat_id,
                    message_id=processing_message.message_id,
                    text=f"📦 *File Size Limit* 📦\n\nThis video is {file_size_mb:.1f}MB.\nTelegram limit is 50MB.\n\n{CREATOR_HASHTAG}",
                    parse_mode='Markdown'
                )
                try: os.remove(result['filename'])
                except: pass
                return
            
            await context.bot.edit_message_text(
                chat_id=chat_id,
                message_id=processing_message.message_id,
                text=f"📤 *Secure Upload...* 🚀\n\n"
                     f"📦 Size: {file_size_mb:.1f}MB\n"
                     f"⏱️ Download: {result.get('download_time', 0):.1f}s\n"
                     f"🛡️ Attempt: {result.get('attempt', 1)}\n\n"
                     f"{CREATOR_HASHTAG}",
                parse_mode='Markdown'
            )
            
            try:
                caption = (
                    f"✨ *Advanced Download Complete!* 🎉\n\n"
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
                    text=f"✅ *Advanced Download Successful!* 🎉\n\n"
                         f"📦 {file_size_mb:.1f}MB in {result.get('download_time', 0):.1f}s\n"
                         f"🛡️ IP Protection Active!\n\n"
                         f"{CREATOR_HASHTAG}",
                    parse_mode='Markdown'
                )
                
                logger.info(f"✅ Advanced delivery to {user.first_name}")
                
            except asyncio.TimeoutError:
                await context.bot.edit_message_text(
                    chat_id=chat_id,
                    message_id=processing_message.message_id,
                    text=f"⏰ *Upload Timeout* ⚡\n\nFile downloaded successfully!\nTry a shorter video next time.\n\n{CREATOR_HASHTAG}",
                    parse_mode='Markdown'
                )
            
            try:
                os.remove(result['filename'])
            except Exception as e:
                logger.warning(f"Cleanup: {e}")
                
        else:
            await context.bot.edit_message_text(
                chat_id=chat_id,
                message_id=processing_message.message_id,
                text=f"🔄 *Download Challenge* 🔄\n\n"
                     f"Platform is being difficult right now.\n"
                     f"Please try:\n"
                     f"• Different video link\n"
                     f"• Wait a few minutes\n"
                     f"• Try another platform\n\n"
                     f"*Error:* {result.get('error', 'Temporary issue')[:80]}\n\n"
                     f"{CREATOR_HASHTAG}",
                parse_mode='Markdown'
            )

    except Exception as e:
        logger.error(f"💥 System error: {e}")
        await context.bot.edit_message_text(
            chat_id=chat_id,
            message_id=processing_message.message_id,
            text=f"⚡ *System Update* ⚡\n\n"
                 f"Temporary system adjustment.\n"
                 f"Please try again in a moment!\n\n"
                 f"{CREATOR_HASHTAG}",
            parse_mode='Markdown'
        )

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.error(f"🚨 Bot error: {context.error}")

def main():
    print("🚀 Starting Advanced LinkLift Bot...")
    
    # Start Flask server
    flask_thread = Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()
    print("🌐 Web server started")
    
    # Start Telegram Bot
    try:
        application = Application.builder().token(BOT_TOKEN).build()
        
        application.add_handler(CommandHandler("start", start_command))
        application.add_handler(CommandHandler("help", help_command))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
        application.add_handler(CallbackQueryHandler(button_handler))
        application.add_error_handler(error_handler)
        
        print("🎉 ADVANCED LINKLIFT BOT STARTED!")
        print("🎵 TikTok • 📺 YouTube • 🐦 Twitter")
        print(f"💫 {CREATOR_HASHTAG}")
        print("🛡️ IP Protection System: ACTIVE")
        print("🚀 Advanced Extraction: ENABLED")
        print("⚡ Smart Retry Logic: RUNNING")
        
        application.run_polling()
        
    except Exception as e:
        logger.error(f"Startup failed: {e}")
        print(f"❌ Startup failed: {e}")

if __name__ == '__main__':
    main()
