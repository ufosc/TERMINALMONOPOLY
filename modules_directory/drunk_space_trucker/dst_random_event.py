import os, keyboard, time
import random
from random import randint

from colorama import (Fore, Style, Back, Cursor)



#this will be the template for events
class random_event:
    # Index 0- Wide Vertical Lasers,[[[x,start_time]]],width of lasers,last laser creation time].
    # Adds the visual aspect to flashing structures
    possible_events=[]

    #certain events need to be called for their collision logic to be detected,adding to this
    #means the collision logic will be checked for the corresponding event
    #happens in collision logic
    collision_events=[]

    delay = 15
    last_event_time = 5000
    # TODO turn these old tuple data data into actual events
   #  active_events_data = [[0, 0, 0.0], [[[0]], 4, -1]]

    def __init__(self, name, dur, input_event_data,hasCollisionObjects):
        self.name=name
        if hasCollisionObjects:
            self.collision_events.append(self.name)
        self.duration=dur
        self.event_data=input_event_data
        self.start_time=-1
        self.active=False
        random_event.possible_events.append(self)



    def logic(self):
        global debug_message
        #events are forced to be called by static methods
        #because they interact with so much of the players data
        if self.active:
            if self.name=="laser":
                debug_message="event 1"
            else:
                None




        if (time.time()-self.start_time)>self.duration:
            self.active=False

    def start_event(self,newStartTime):
        self.start_time=newStartTime
        self.active=True



    def set_duration(self, new_dur):
        self.duration=new_dur
    def get_data(self):
        return self.event_data







