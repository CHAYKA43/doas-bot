doas = None


def register():
    # Adding a user to the users monitoring list
    @doas.message_handler(commands=['add_user'])
    async def add_user(message):
        chat_id = message.chat.id
        user_id = message.from_user.id
        result = await is_user_admin(chat_id, user_id)
    
        # Checking a user for administrator rights
        if result == 0:
            await doas.reply_to(message, "You do not have permission to run this command.")
            return
        # Checking a command for an argument
        args = message.text.split()
        if len(args) < 2:
            await doas.reply_to(message, "Please enter a user ID. \nExample: /add_user 123123123")
            return
    
        user_to_add = args[1]
        print(f"Attempting to add user: {user_to_add}") # Debugging to the console
    
        # Handling errors and adding a user to the list
        try:
            with open('config/users.txt', 'r') as file:
                existing_users = file.read().splitlines()
    
            # Sending an error message that the user is already on the list
            if user_to_add in (user.lower() for user in existing_users):
                await doas.reply_to(message, f"The user ID '{user_to_add}' already exists in the list.")
                return
    
            # Adding a user to the list
            with open('config/users.txt', 'a') as file:
                file.write(f'\n{user_to_add}')
    
            # Sending a message that the user has been successfully added to the list
            await doas.reply_to(message, f"User ID '{user_to_add}' added.")
        # Sending an error message
        except Exception as e:
            await doas.reply_to(message, f"An error occurred: {str(e)}")
    
    
    # Removing a user from the users monitoring list
    @doas.message_handler(commands=['remove_user'])
    async def remove_user(message):
        chat_id = message.chat.id
        user_id = message.from_user.id
        result = await is_user_admin(chat_id, user_id)
    
        # Checking a user for administrator rights
        if result == 0:
            await doas.reply_to(message, "You do not have permission to run this command.")
            return
        # Checking a command for an argument
        args = message.text.split()
        if len(args) < 2:
            await doas.reply_to(message, "Please enter user ID. \nExample: /remove_user 123123123")
            return
    
        user_id_to_remove = args[1]
        print(f"Removing a user: ID = {user_id_to_remove}")  # Debugging to the console
    
        # Handling errors and removing a user from the list
        try:
            with open('config/users.txt', 'r') as file:
                users = file.readlines()
                
            # Removing a user from the list
            with open('config/users.txt', 'w') as file:
                for user in users:
                    if user.strip() != user_id_to_remove:
                        file.write(user)
    
            # Sending a message that the user has been successfully removed from the list
            await doas.reply_to(message, f"User ID: {user_id_to_remove} has been removed.")
        # Sending an error message that the file with the list of users was not found
        except FileNotFoundError:
            await doas.reply_to(message, "User list not found.")
        # Sending an error message
        except Exception as e:
            await doas.reply_to(message, f"An error occurred: {str(e)}")
