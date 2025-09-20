import json
import telebot
import os
from datetime import datetime
from datetime import date, timedelta

allowed_usernames = ["notjoshwash"]

bb_members = ["rex", "yaoying", "nigel", "ryan", "joon", "jordan", "hafiz", "josh"]

bot = telebot.TeleBot(
    token = os.environ.get("TELE_API_KEY"),
    threaded = False)

@bot.message_handler(commands=['paid'])
def startCommand(message):
    pass

@bot.message_handler(commands=['payUp'])
def startCommand(message):
    chat_id = message.chat.id
    try:
        arg_str = " ".join(message.text.split(" ")[1:])
        args = arg_str.split(";")
    except Exception as e:
        bot.send_message(chat_id, f"Please use correct format {str(e)}", reply_to_message_id=message.message_id)
        return

    try:
        desc = args[0].replace("\"", "") # Description
        amount = float(args[1]) # Amount
    except Exception as e:
        bot.send_message(chat_id, f"Please use correct format {str(e)}", reply_to_message_id=message.message_id)
        return


    final_str = f" ==== {desc} =====\n"
    final_str += f"Total Cost -> ${amount:.2f}\n"

    member_list_str = ""

    if len(args) < 3:
        bot.send_message(chat_id, f"Please include who is not included in the amount, if all are included please indicate NONE", reply_to_message_id=message.message_id)
        return
    not_included = args[2:] # Not included in amount

    if not_included[0] == "NONE":
        pass
    else:
        for member in bb_members:
            if member in not_included:
                continue
            else:
                member_list_str += f"{member}\n"
    
    cost_pp = float(amount/float(len(bb_members) - len(not_included)))
    final_str += f"Cost per person -> ${cost_pp:.2f}\n\n"
    final_str += member_list_str
    final_str += "\n!! Please remove your name once you've paid !!"
    bot.send_message(chat_id, final_str, reply_to_message_id=message.message_id)
    return

    bot.send_message

@bot.message_handler(commands=['schedulePrac'])
def startCommand(message):
    chat_id = message.chat.id
    username = message.chat.username
    args = message.text.split(" ")[1:]

    try:
        start_date = datetime.strptime(args[1], '%d-%m-%Y').date()
        end_date = datetime.strptime(args[2], '%d-%m-%Y').date()
    except:
        bot.send_message(chat_id, f"Please use correct DD-MM-YYYY format", reply_to_message_id=message.message_id)
        return
    delta = end_date - start_date   # returns timedelta

    day_list = []
    if (delta.days + 1) > 7:
        bot.send_message(chat_id, f"Stop trying to be funny pls", reply_to_message_id=message.message_id)
        return
    for i in range(delta.days + 1):
        day = start_date + timedelta(days=i)
        day_list.append(f"{day.strftime('%d-%m-%Y')} ({day.strftime('%A')})")

    chat_id = message.chat.id
    question = f"Indicate your availability ({args[0]})"
    options = day_list
    bot.send_poll(
        chat_id,
        question,
        options,
        is_anonymous=False,  # Set to True for anonymous voting
        allows_multiple_answers=True, # Set to True for multiple answer selection
        type='regular', # or 'quiz' for a quiz-style poll with a correct answer
        reply_to_message_id=message.message_id
    )

def lambda_handler(event, context):
    body = json.loads(event['body'])

    json_string = json.dumps(body)
    update = telebot.types.Update.de_json(json_string)
    try:
        bot.process_new_updates([update])
    except:
        return {
        'statusCode': 500,
        'body': json.dumps('Internal Server Error')
        }

    return {
        'statusCode': 200,
        'body': json.dumps('Message processed successfully')
    }
