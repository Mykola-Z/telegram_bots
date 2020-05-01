# -*- coding: utf-8 -*-
"""
Created on Wed Apr 29 16:07:22 2020

@author: mzly903
"""

import telebot
import flightconfig
from telebot import types
import random
import flight
import csv
import pandas as pd



# add a new row in csv file 
def append_list_as_row(file_name, list_of_elem):
    # Open file in append mode
    with open(file_name, 'a+', newline='') as write_obj:
        # Create a writer object from csv module
        csv_writer = csv.writer(write_obj)
        # Add contents of list as last row in the csv file
        csv_writer.writerow(list_of_elem)   

def get_users_flight(user, flightnumber, file='databaseMFM.csv'):
    csv_file_name = str(file)
    database = pd.read_csv(csv_file_name)
    return database[database["user_id"] == user].T.values.tolist()[flightnumber+4] 


def users_flights(user, file='databaseMFMv1.1.csv'):
    csv_file_name = str(file)
    database = pd.read_csv(csv_file_name)
    flight_list = database[database["user_id"] == user].T.values.tolist()[4:]
    all_users_flights = []
    for i in range(len(flight_list)):
        if isinstance(flight_list[i][0], float) == False:
            all_users_flights.append(flight_list[i][0])
    return all_users_flights

def add_flight(user, flight, file='databaseMFMv1.1.csv'):
    csv_file_name = str(file)
    database = pd.read_csv(csv_file_name)
    flight_number = len(users_flights(user))+1
    database.loc[database["user_id"] == user, str(flight_number)] = flight
    database.to_csv(file, index=False)
    
def add_date(user, date, file='databaseMFMv1.1.csv'):
    csv_file_name = str(file)
    database = pd.read_csv(csv_file_name)
    flight_number = len(users_flights(user))
    database.loc[database["user_id"] == user, str(flight_number)] += " on " + date
    database.to_csv(file, index=False)

# user = 232935725 #my id
# add_flight(user, "Test_Flight")


    
# Check if str is a number
        
def isfloat(x):
    try:
        a = float(x)
    except ValueError:
        return False
    else:
        return True

# list of default messages

funny_start = ['Give me 1 sec to find a pen', "Ok, I'm ready",
               "Wow, a new journey! I am jealous of you!",
               "I'm so excited to record your new flight!"]

# Token from FatherBot
bot = telebot.TeleBot(flightconfig.TOKEN)

# Buttons
buttons = ['Add a Flight', 'View my flights', 'Edit a Flight']
def keyboard():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True,
                                       resize_keyboard=True)
    for item in buttons:
        btn1 = types.KeyboardButton(item)
        markup.add(btn1)
    return markup

# Welcome message and Record User

@bot.message_handler(commands=['start', 'help'])

def send_welcome(message):
    
    #users database
    csv_file_name = str('databaseMFMv1.1.csv')
    database = pd.read_csv(csv_file_name)
    user_id = message.from_user.id
    print(message.from_user)

    #welcome text
    welcome_text = 'Hi! Ready to record your flight /n Enter your flight number or where are you flying from?'

    #check if there is a user
    users = database['user_id'].T.values.tolist()   #questionable solution

    if user_id not in users:
        bot.send_message(message.chat.id, welcome_text, reply_markup=keyboard())
        user_nickname = message.from_user.username
        user_name = message.from_user.first_name
        user_surname = message.from_user.last_name
        new_user = [user_id, user_nickname, user_name, user_surname]
        append_list_as_row(csv_file_name, new_user)
        
    else:
        bot.send_message(message.chat.id, welcome_text, reply_markup=keyboard())


@bot.message_handler(content_types=['text'])

def react(message):
    
    if message.text.lower()[:4] == 'add ' :
        funny_text = random.choice(funny_start)
        bot.send_message(message.chat.id, funny_text)
        text = "Enter your flight number (for example, AA100)"
        bot.send_message(message.chat.id, text)
        
    elif isfloat(message.text[:2]) == False and isfloat(message.text[-2:]) == True and len(message.text) < 7:
        route = flight.checkNumber(message.text)
        if len(route[0][0]) > 4: 
            text = 'Wow, I have never been to ' + route[1][0]
            bot.send_message(message.chat.id, text)
            text1 = 'When do you fly from ' + route[0][0] + " ("+ route[0][1] + ") to " + route[1][0] + " (" + route[1][1] +")? (e.g. 06.04.2021)"
            bot.send_message(message.chat.id, text1)
            add_this_flight = text1[21:-19]
            add_flight(message.from_user.id, add_this_flight)

        else:
            text = "Sorry, I did not find flight " + str(message.text)
            bot.send_message(message.chat.id, text)
     
    elif message.text.lower()[:4] == 'view':
        text = 'List of your flights:\n'
        flights = users_flights(message.from_user.id)
        for i in range(len(flights)):
            text += flights[i] + '\n' 
        bot.send_message(message.chat.id, text)
    # elif message.text in outcomes:
    #     text = "Sorry, it's not ready yet"
    #     bot.send_message(message.chat.id, text)
    elif isfloat(message.text[-2:]):
        text = "ok, I recorded your flight on " + message.text
        bot.send_message(message.chat.id, text)
        add_date(message.from_user.id, message.text)
        
    else:
        text = "Sorry, I have no idea what are you talking about "
        bot.send_message(message.chat.id, text)
        text_to_me = message.from_user.username +' ' + str(message.from_user.id) + ' : ' + message.text
        bot.send_message(232935725, text_to_me)


bot.polling()