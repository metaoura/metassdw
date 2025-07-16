import telebot
import requests
import time
import json
from datetime import datetime, timedelta
import logging
from telebot import TeleBot, types
import threading

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Bot initialization
bot = telebot.TeleBot("7598892728:AAG0Mhwh4a7iN-gjqH6QWd48wHxpcTTKVt0")
ALLOWED_GROUP_ID = -1002600647691
API_BASE = "http://168.231.113.96:9803"
PLAYER_INFO_API = "https://projects-fox-apis.vercel.app/player_info"
API_KEY = "Fox-7CdxP"
CHANNEL_LINK = "https://t.me/+mB9TONYndBdhMTQ0"
CHANNEL_ID = "-1002600647691"
OWNER_ID = 7673746248

# Databases
user_usage = {}
vip_users = set()
used_player_ids = set()
fr_locked = False  # حالة قفل البوت الجديدة

# Load data from files
def load_data():
    global vip_users, used_player_ids
    try:
        with open('vip_users.txt', 'r') as f:
            vip_users = set(json.load(f))
    except (FileNotFoundError, json.JSONDecodeError):
        vip_users = set()
    
    try:
        with open('used_player_ids.txt', 'r') as f:
            used_player_ids = set(json.load(f))
    except (FileNotFoundError, json.JSONDecodeError):
        used_player_ids = set()

def save_data():
    """Save data to files"""
    with open('vip_users.txt', 'w') as f:
        json.dump(list(vip_users), f)
    with open('used_player_ids.txt', 'w') as f:
        json.dump(list(used_player_ids), f)

def is_owner(user_id):
    """Check if user is owner"""
    return user_id == OWNER_ID

def is_vip(user_id):
    """Check if user is VIP"""
    return user_id in vip_users or is_owner(user_id)

def is_member(user_id):
    """Check if user is channel member"""
    try:
        member = bot.get_chat_member(CHANNEL_ID, user_id)
        return member.status in ['member', 'administrator', 'creator']
    except Exception as e:
        logger.error(f"Error checking membership for {user_id}: {e}")
        return False

def can_user_request(user_id):
    """Check if user can make a request"""
    if is_owner(user_id):
        return True
        
    now = datetime.now()
    
    if user_id not in user_usage:
        user_usage[user_id] = {
            'count': 0,
            'last_reset': now
        }
    
    if now - user_usage[user_id]['last_reset'] > timedelta(days=1):
        user_usage[user_id]['count'] = 0
        user_usage[user_id]['last_reset'] = now
    
    max_requests = 10 if is_vip(user_id) else 3
    return user_usage[user_id]['count'] < max_requests

def increment_user_count(user_id):
    """Increment user request count"""
    if user_id in user_usage and not is_owner(user_id):
        user_usage[user_id]['count'] += 1
        logger.info(f"Incremented count for user {user_id}. New count: {user_usage[user_id]['count']}")

def player_id_used_today(player_id):
    """Check if player ID was used today"""
    return player_id in used_player_ids

def add_player_id_to_used(player_id):
    """Add player ID to used list"""
    used_player_ids.add(player_id)
    save_data()
    logger.info(f"Added player ID {player_id} to used list")

def clear_daily_data():
    """Clear daily data every day"""
    while True:
        global used_player_ids
        used_player_ids = set()
        save_data()
        logger.info("Cleared daily used player IDs")
        time.sleep(86400)  # Wait 24 hours

def check_api_health():
    """Check if API is reachable"""
    try:
        url = f"{API_BASE}/get_time/10414593349"
        res = requests.get(url, timeout=5)
        return res.status_code < 500
    except Exception as e:
        logger.error(f"API health check failed: {e}")
        return False

def add_player(player_id):
    """Add player to system"""
    url = f"{API_BASE}/add_uid?uid={player_id}&time=86400&type=seconds"
    try:
        res = requests.get(url, timeout=30)
        if res.status_code == 200:
            logger.info(f"Successfully added player {player_id}")
            return True
        logger.error(f"Failed to add player {player_id}. Status code: {res.status_code}")
        return False
    except Exception as e:
        logger.error(f"Error adding player {player_id}: {e}")
        return False

def get_player_info(player_id):
    """Get player information"""
    url = f"{PLAYER_INFO_API}?uid={player_id}&key={API_KEY}"
    try:
        res = requests.get(url, timeout=30)
        if res.status_code == 200:
            return res.json()
        logger.error(f"Failed to get player info for {player_id}. Status code: {res.status_code}")
        return None
    except Exception as e:
        logger.error(f"Error getting player info for {player_id}: {e}")
        return None

# ===== الأوامر الجديدة للتحكم في قفل البوت =====
@bot.message_handler(commands=['frlock'])
def handle_frlock(message):
    """Lock the bot for non-VIP users"""
    user_id = message.from_user.id
    if not is_owner(user_id):
        return
    
    global fr_locked
    fr_locked = True
    bot.reply_to(message, "🔒 تم قفل البوت بنجاح، الآن لن يستجيب إلا لأعضاء VIP والمطور.")

@bot.message_handler(commands=['funlock'])
def handle_funlock(message):
    """Unlock the bot for all users"""
    user_id = message.from_user.id
    if not is_owner(user_id):
        return
    
    global fr_locked
    fr_locked = False
    bot.reply_to(message, "🔓 تم فتح البوت بنجاح، الآن يستجيب للجميع.")

# ===== الميزات الأصلية للبوت مع تعديلات لدعم FRlock =====
@bot.message_handler(commands=['status'])
def handle_status(message):
    """Check bot status"""
    if fr_locked and not (is_vip(message.from_user.id) or is_owner(message.from_user.id)):
        return
    
    api_status = "🟢 Online" if check_api_health() else "🔴 Offline"
    status_text = (
        f"⚙️ <b>Bot Status</b>\n\n"
        f"API Status: {api_status}\n"
        f"VIP Users: {len(vip_users)}\n"
        f"Today's Players: {len(used_player_ids)}\n"
        f"Channel: @{CHANNEL_ID}\n"
        f"Bot Lock Status: {'🔒 Locked (VIP only)' if fr_locked else '🔓 Unlocked'}"
    )
    bot.reply_to(message, status_text, parse_mode='HTML')

@bot.message_handler(commands=['add'])
def handle_add(message):
    """Handle add command"""
    try:
        user_id = message.from_user.id
        
        # التحقق من حالة القفل أولاً
        if fr_locked and not (is_vip(user_id) or is_owner(user_id)):
            return
            
        logger.info(f"Received /add command from {user_id} in chat {message.chat.id}")
        
        if message.chat.id != ALLOWED_GROUP_ID:
            logger.warning(f"Message from unauthorized chat: {message.chat.id}")
            return
    
        if not is_owner(user_id) and not is_member(user_id):
            logger.info(f"User {user_id} is not member")
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("Join Channel", url=CHANNEL_LINK))
            bot.reply_to(message, "❌ You must join our channel to use this command. Please join the channel and try again.", reply_markup=markup)
            return
    
        if not can_user_request(user_id):
            logger.info(f"User {user_id} exceeded limit")
            return
    
        try:
            player_id = message.text.split()[1]
            logger.info(f"Processing player ID: {player_id}")
            
            if player_id_used_today(player_id):
                logger.info(f"Player {player_id} already used today")
                return
                
            player_info = get_player_info(player_id)
            logger.info(f"Player info received: {json.dumps(player_info, indent=2)}")
            
            if not player_info:
                logger.error(f"Failed to get info for player {player_id}")
                return
                
            if add_player(player_id):
                response = (
                    f"✅ Sending bot to {player_info.get('player_name', 'Unknown')} ({player_id}) for 24h\n"
                    f"🔗 {CHANNEL_LINK}"
                )
                increment_user_count(user_id)
                add_player_id_to_used(player_id)
                bot.reply_to(message, response, parse_mode='HTML')
            
        except IndexError:
            logger.warning("Invalid /add command format")
            
    except Exception as e:
        logger.error(f"Error in handle_add: {e}")

@bot.message_handler(commands=['vip'])
def handle_vip(message):
    """Manage VIP users"""
    try:
        user_id = message.from_user.id
    
        if not is_owner(user_id):
            logger.warning(f"Unauthorized VIP access attempt by {user_id}")
            return
    
        try:
            parts = message.text.split()
            if len(parts) == 3:
                action = parts[1].lower()
                target = int(parts[2])
                
                if action == 'add':
                    vip_users.add(target)
                    bot.reply_to(message, f"✅ User {target} added to VIP list", parse_mode='HTML')
                elif action == 'remove':
                    vip_users.discard(target)
                    bot.reply_to(message, f"✅ User {target} removed from VIP list", parse_mode='HTML')
                
                save_data()
            else:
                # Show VIP list if no parameters provided
                vip_list = "\n".join(str(uid) for uid in vip_users)
                response = f"<b>VIP Users List:</b>\n<code>{vip_list if vip_list else 'No VIP users'}</code>"
                bot.reply_to(message, response, parse_mode='HTML')
                
        except ValueError:
            logger.warning("Invalid VIP command format")
            
    except Exception as e:
        logger.error(f"Error in handle_vip: {e}")

# Main execution
if __name__ == '__main__':
    # Load data on startup
    load_data()
    logger.info("Data loaded successfully")
    
    # Start daily clear thread
    threading.Thread(target=clear_daily_data, daemon=True).start()
    
    # Check API health on startup
    if check_api_health():
        logger.info("API is reachable")
    else:
        logger.warning("API is not reachable")
    
    # Start bot
    logger.info("Starting bot...")
    while True:
        try:
            bot.polling(none_stop=True, interval=2, timeout=30)
        except Exception as e:
            logger.error(f"Bot polling error: {e}")
            time.sleep(10)