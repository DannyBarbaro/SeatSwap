from pymongo import MongoClient
from datetime import datetime

import os, sys
sys.path.append(os.path.join(os.path.dirname(sys.path[0]), 'backend'))
import Model
import Repository as repo

def make_seats(secL, secH, rowL, rowH, seatL, seatH, secI=1, rowI=1, seatI=1):
    seats = []
    for sec in range(secL, secH, secI):
        for row in range(rowL, rowH, rowI):
            for seat in range(seatL, seatH, seatI):
                seats.append(f"sec{sec}row{row}seat{seat}")
    return seats

sb_seats = make_seats(100, 401, 1, 5, 1, 8, secI=100)
pres_seats = make_seats(1, 2, 1, 30, 1, 6)
yesterday_seats = make_seats(1, 2, 1, 2, 1, 2)

suberbowl = Model.Event({'start_time': datetime(2020, 2, 2, 19, 0, 0), 'team1': "Jets", 'team2': "Bengals", 'location': "Miami, FL", 'event_type': "NFL", 'period_count': 4, 'seats': sb_seats, 'event_name': "Suberb Owl"})

my_393_presentation = Model.Event({'start_time': datetime(2019, 12, 6, 11, 40, 0), 'team1': "us", 'team2': "Rohan & Anthony", 'location': "Bingham", 'event_type': "Presentation", 'period_count': 4, 'seats': pres_seats, 'event_name': "My 393 Presentation"})

yesterday = Model.Event({'start_time': datetime(2019, 12, 3, 0, 0, 0), 'team1': "today", 'team2': "tomorrow", 'location': "Yes", 'event_type': "Life", 'period_count': 1, 'seats': yesterday_seats, 'event_name': "Yesterday"})

repo.add_event(suberbowl)
repo.add_event(my_393_presentation)
repo.add_event(yesterday)

#print current events and ID's for convenince
print('Events currently in database:')
for event in repo.get_all_events():
    print(f'Event name: {event.event_name}, ID: {event._id}')