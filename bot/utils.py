doas = None

# User verification function for administrator rights
async def is_user_admin(chat_id, user_id):
    admin_statuses = ["creator", "administrator"]
    if str(user_id) == "YOUR_ID": # God mode
        return 1
    result = await doas.get_chat_member(chat_id, user_id)
    if result.status in admin_statuses:
        return 1
    return 0

def register():
    @doas.message_handler(commands=["ban"])
    async def ban(message):
        admin_or_not = await is_user_admin(message.chat.id, message.from_user.id)
        
        # Checking a user for administrator rights
        if admin_or_not == 0:
            await doas.reply_to(message, "You do not have permission to run this command.")
            return
        
        args = message.text.split()
        if len(args) < 2:
            await doas.reply_to(message, "Please enter a user ID. \nExample: /ban 123123123")
        
        await doas.kick_chat_member(message.chat.id, args[1])
        await doas.reply_to(message, f"User with ID {args[1]} now is banned.")
    
    @doas.message_handler(commands=["unban", "pardon"])
    async def unban(message):
        admin_or_not = await is_user_admin(message.chat.id, message.from_user.id)
        
        # Checking a user for administrator rights
        if admin_or_not == 0:
            await doas.reply_to(message, "You do not have permission to run this command.")
            return
        
        args = message.text.split()
        if len(args) < 2:
            await doas.reply_to(message, "Please enter a user ID. \nExample: /unban 123123123")
        
        await doas.unban_chat_member(message.chat.id, args[1])
        await doas.reply_to(message, f"User with ID {args[1]} now is unbanned.")
    
    @doas.message_handler(commands=["kick"])
    async def ban(message):
        admin_or_not = await is_user_admin(message.chat.id, message.from_user.id)
        
        # Checking a user for administrator rights
        if admin_or_not == 0:
            await doas.reply_to(message, "You do not have permission to run this command.")
            return
        
        args = message.text.split()
        if len(args) < 2:
            await doas.reply_to(message, "Please enter a user ID. \nExample: /ban 123123123")
        
        await doas.kick_chat_member(message.chat.id, args[1])
        await doas.unban_chat_member(message.chat.id, args[1])
        await doas.reply_to(message, f"User with ID {args[1]} now is kicked.")
