import random
import aiohttp
import json
import asyncio
import telebot

doas = None
ttt_data = {}

async def json_animal_api(animal):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://some-random-api.com/animal/{animal}") as resp:
            return await resp.json()

def register():
    @doas.message_handler(commands=["hack", "heck"])
    async def ver(message):
        hacked_entity = str()
        
        args = message.text.split()
        if len(args) < 2:
            hacked_entity = f"@{message.from_user.username}"
        else:
            hacked_entity = args[1]
        
        hack_status = [
                "was successfully hacked!",
                "wasn't hacked. And don't even try to do it again!",
                "wasn't hacked, there is no intenet.",
                "was hacked, now (s)he's an Illuminati"
        ]
        
        await doas.reply_to(message, f"{hacked_entity} {random.choice(hack_status)}")
    
    @doas.message_handler(commands=["ball"])
    async def ball(message):
        args = message.text.split()
        if len(args) < 2:
            await doas.reply_to(message, "Dude, ask a question.")
            return
        
        
        ball_status = [
                "Yes, sure",
                "Maybe",
                "idk bro",
                "No, I don't think that"
        ]
        
        await doas.reply_to(message, random.choice(ball_status))
    
    @doas.message_handler(commands=["cat", "dog", "fox"])
    async def animal(message):
        args = message.text.split()
        
        img = await json_animal_api(args[0].replace("/", ""))
        
        await doas.send_photo(message.chat.id, img["image"])
    
    @doas.message_handler(commands=["tic", "tac", "toe", "tictactoe", "tic_tac_toe", "ttt"])
    async def tic_tac_toe(message):
        args = message.text.split()
        
        if len(args) < 2 or len(args) > 2:
            await doas.reply_to(message, "Dude, you can only play tic-tac-toe with two people.")
            return
        
        ID = int()
        
        for i in range(0, len(message.from_user.username)):
            ID += ord(message.from_user.username[i])
        
        for i in range(0, len(args[1])):
            if args[1][i] != "@":
                ID += ord(args[1][i])
        
        ttt_data[f"{ID}"] = {
            "users": [message.from_user.username, args[1].replace("@", "")],
            "current_player": message.from_user.username,
            "winner": None,
            "index": 0,
            "field": [[" ", " ", " "],
                      [" ", " ", " "],
                      [" ", " ", " "]]
        }
        
        markup = telebot.types.InlineKeyboardMarkup()
        
        for i in range(1, 4):
            btn1 = telebot.types.InlineKeyboardButton(text=" ", callback_data=f"ttt{i}x1i{ID}")
            btn2 = telebot.types.InlineKeyboardButton(text=" ", callback_data=f"ttt{i}x2i{ID}")
            btn3 = telebot.types.InlineKeyboardButton(text=" ", callback_data=f"ttt{i}x3i{ID}")
            markup.row(btn1, btn2, btn3)
        
        await doas.reply_to(message, f"The game has begun.\nCurrent player: {ttt_data[f"{ID}"]["current_player"]}", reply_markup=markup)
    
    @doas.callback_query_handler(func=lambda call: True)
    async def query_handler(call):
        if "ttt" in call.data:
            y, x, ID = map(int, call.data.replace("x", " ").replace("i", " ").replace("ttt", "").split())
            #await doas.reply_to(call.message, f"ID: {ID}, x: {x}, y:{y}")
            
            await doas.answer_callback_query(call.id)

            try:
                ttt_data[f"{ID}"]
            except:
                await doas.reply_to(call.message, "This game is no longer available.\nYou can start a new one: /ttt @username")
                await doas.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
                return

            if call.from_user.username != ttt_data[f"{ID}"]["current_player"]:
                await doas.reply_to(call.message, f"@{call.from_user.username}, go fuck yourself.")
                return

            if (ttt_data[f"{ID}"]["index"] % 2) == 0 and call.from_user.username == ttt_data[f"{ID}"]["users"][0]:
                if ttt_data[f"{ID}"]["field"][y-1][x-1] == " ":
                    ttt_data[f"{ID}"]["field"][y-1][x-1] = "X"
                    ttt_data[f"{ID}"]["current_player"] = ttt_data[f"{ID}"]["users"][1]
                else:
                    await doas.reply_to(call.message, f"@{call.from_user.username}, go fuck yourself.")
                    return
            elif call.from_user.username == ttt_data[f"{ID}"]["users"][1]:
                if ttt_data[f"{ID}"]["field"][y-1][x-1] == " ":
                    ttt_data[f"{ID}"]["field"][y-1][x-1] = "O"
                    ttt_data[f"{ID}"]["current_player"] = ttt_data[f"{ID}"]["users"][0]
                else:
                    await doas.reply_to(call.message, f"@{call.from_user.username}, go fuck yourself.")
                    return
            else:
                await doas.reply_to(call.message, f"{call.from_user.username}, but you can't.")
                return
            
            ttt_data[f"{ID}"]["index"] += 1
            
            markup = telebot.types.InlineKeyboardMarkup()
            for i in range(0, 3):
                btn1 = telebot.types.InlineKeyboardButton(text=f"{ttt_data[f"{ID}"]["field"][i][0]}", callback_data=f"ttt{i+1}x1i{ID}")
                btn2 = telebot.types.InlineKeyboardButton(text=f"{ttt_data[f"{ID}"]["field"][i][1]}", callback_data=f"ttt{i+1}x2i{ID}")
                btn3 = telebot.types.InlineKeyboardButton(text=f"{ttt_data[f"{ID}"]["field"][i][2]}", callback_data=f"ttt{i+1}x3i{ID}")
                markup.row(btn1, btn2, btn3)
            
            if ttt_data[f"{ID}"]["index"] != 9:
                await doas.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                            text=f"{call.from_user.username} strikes the DECISIVE blow!\nCurrent player: {ttt_data[f"{ID}"]["current_player"]}", reply_markup=markup)
                for i in range(3):
                    if ttt_data[f"{ID}"]["field"][i][0] == ttt_data[f"{ID}"]["field"][i][1] == ttt_data[f"{ID}"]["field"][i][2] != " ":
                        if ttt_data[f"{ID}"]["field"][i][0] == "X":
                            ttt_data[f"{ID}"]["winner"] = ttt_data[f"{ID}"]["users"][0]
                        else:
                            ttt_data[f"{ID}"]["winner"] = ttt_data[f"{ID}"]["users"][1]
                        await doas.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                                text=f"@{ttt_data[f"{ID}"]["winner"]} wins!", reply_markup=markup)
                        del ttt_data[f"{ID}"]
                        return
                for i in range(3):
                    if ttt_data[f"{ID}"]["field"][0][i] == ttt_data[f"{ID}"]["field"][1][i] == ttt_data[f"{ID}"]["field"][2][i] != " ":
                        if ttt_data[f"{ID}"]["field"][0][i] == "X":
                            ttt_data[f"{ID}"]["winner"] = ttt_data[f"{ID}"]["users"][0]
                        else:
                            ttt_data[f"{ID}"]["winner"] = ttt_data[f"{ID}"]["users"][1]
                        await doas.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                                text=f"@{ttt_data[f"{ID}"]["winner"]} wins!", reply_markup=markup)
                        del ttt_data[f"{ID}"]
                        return
                if ttt_data[f"{ID}"]["field"][0][0] == ttt_data[f"{ID}"]["field"][1][1] == ttt_data[f"{ID}"]["field"][2][2] != " ":
                        if ttt_data[f"{ID}"]["field"][0][0] == "X":
                            ttt_data[f"{ID}"]["winner"] = ttt_data[f"{ID}"]["users"][0]
                        else:
                            ttt_data[f"{ID}"]["winner"] = ttt_data[f"{ID}"]["users"][1]
                        await doas.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                                text=f"@{ttt_data[f"{ID}"]["winner"]} wins!", reply_markup=markup)
                        del ttt_data[f"{ID}"]
                        return
                if ttt_data[f"{ID}"]["field"][0][2] == ttt_data[f"{ID}"]["field"][1][1] == ttt_data[f"{ID}"]["field"][2][0] != " ":
                        if ttt_data[f"{ID}"]["field"][0][2] == "X":
                            ttt_data[f"{ID}"]["winner"] = ttt_data[f"{ID}"]["users"][0]
                        else:
                            ttt_data[f"{ID}"]["winner"] = ttt_data[f"{ID}"]["users"][1]
                        await doas.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                                text=f"@{ttt_data[f"{ID}"]["winner"]} wins!", reply_markup=markup)
                        del ttt_data[f"{ID}"]
                        return
            else:
                await doas.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                            text="Nobody wins!", reply_markup=markup)
                del ttt_data[f"{ID}"]
