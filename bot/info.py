from datetime import datetime, timezone
import telebot

doas = None
start_time = None

def register():
    # Command that prints the version and other useful (or not?) information
    @doas.message_handler(commands=["ver", "info"])
    async def ver(message):
        # spaghetti string
        await doas.reply_to(message, "<b>Version:</b> 0.6.6 M2\n<b>Telegram library:</b> Telebot\n<b>Language:</b> Python", parse_mode='HTML')
        
    # Command to find out how long the bot has been running
    @doas.message_handler(commands=["uptime"])
    async def send_uptime(message):
        current_time = datetime.now(timezone.utc)
        uptime_duration = current_time - start_time
    
        # Getting days hours and minutes from bot running time
        days = uptime_duration.days
        hours, remainder = divmod(uptime_duration.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
    
        # Formatting and sending a message to a user
        uptime_str = f"{days} days, {hours} hours, {minutes} minutes."
        await doas.send_message(message.chat.id, f'The bot has been running for: \n{uptime_str}')
