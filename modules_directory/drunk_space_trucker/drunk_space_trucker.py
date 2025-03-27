import os, keyboard, time
import random
from random import randint

from colorama import (Fore, Style, Back, Cursor)
from txt_struct import *
from dst_random_event import *

#Regards info about flashing structures, such as the last state for drawing(drawn or not), the last time it was called
#and the interval on which it should swap the last state
#0 last state for being drawn
#1 last time it was called
#2 interval of between swapping states
flashing_structures_info=[]


game_board=[]
player_x = 32
player_y = 20
horizontal_speed=2
vertical_speed=1
player_alive=True
debug_message="test"

player_missle_coordinates=[]


asteroid_delay=3
asteroid_move_delay=1
last_asteroid_time=0
last_asteroid_move_time=0
asteroid_coordinates=[]

score=0
lastTimeScore=0
lastTimeScoreDelay=3

distance=0

cutscene_active=False

port_coords=[1,0]
port_extends=0




#events are static b/c I can't think of a better way to be able to alter the data
def drift_effect():
        global player_y, player_x,debug_message
        if time.time() - random_event.possible_events[0].get_data()[2]  > 0.2:
            driftX=random_event.possible_events[0].get_data()[0]
            driftY=random_event.possible_events[0].get_data()[1]

            if driftY != 0 and (len(game_board) - 1) > (player_y +driftY) > 0:
                player_y += driftY
            if random_event.possible_events[0].get_data()[0] != 0 and (len(game_board[0]) - 1) > (player_x + random_event.possible_events[0].get_data()[0]) > 0:
                player_x += driftX
            random_event.possible_events[0].get_data()[2]  = time.time()




#TODO System of modularlly adding things to be drawn through an array so that way events can add visual stuff whenever
#def add_text_structure(text_arr):


def draw_text_structure(text_arr, x, y):
    global game_board
    for row in range(len(text_arr)):
        for col in range(len(text_arr[row])):
            if (row+y)<len(game_board) and (row-(len(text_arr)//2))+y>0:
                calculatedY = (row - (len(text_arr) // 2)) + y
                calculatedX = (col - (len(text_arr[row]) // 2)) + x
                game_board[calculatedY][calculatedX]=text_arr[row][col]


def insert_flashing_text_structure(text_arr,x,y,index):
    global game_board,flashing_structures_info
    if( time.time()-flashing_structures_info[index][1])>flashing_structures_info[index][2] :
        flashing_structures_info[index][0]=not flashing_structures_info[index][0]
        flashing_structures_info[index][1]=time.time()

    if flashing_structures_info[index][0]:



        draw_text_structure(text_arr, x, y)


def insert_text(text,x,y):
    global game_board
    for index,letter in enumerate(text):
        game_board[y][x-len(text)//2+index]=letter


def port_cutscene():
    global player_x, player_y,vertical_speed,horizontal_speed,debug_message,game_board,port_coords,port_extends
    cutSceneRunning=True
    moveY=len(game_board)//2-player_y
    moveX=len(game_board[0])//2-player_x

    asteroid_coordinates.clear()
    player_missle_coordinates.clear()
    old_time=time.time()
    old_vertical_speed=vertical_speed
    old_horizonatal_speed=horizontal_speed

    vertical_speed=0
    horizontal_speed=0
    while cutSceneRunning:
        #debug_message = f"Player: ({player_y}, {player_x}), Distance to center: ({moveY}, {moveX})"

        if (time.time()-old_time)>0.2:
            print_game(True)
            old_time=time.time()
            #Moves port to center
            if(port_coords[1])<len(game_board)//2:
                port_coords[1] += 1

            else:
                #occurs when port is centered and player is centered, extends out the tube
                debug_message="X:"+str(moveX)+" Y:"+str(moveY)
                if moveX==0 and moveY==0:
                    if port_extends < player_x-1:
                        port_extends = port_extends + 1

            #moves ship to center
            if moveX>0:
                player_x=player_x+1
                moveX=moveX-1
            if moveX<0:
                player_x=player_x-1
                moveX=moveX+1
            if moveY>0:
                player_y=player_y+1
                moveY=moveY-1
            if moveY<0:
                player_y=player_y-1
                moveY=moveY+1





    vertical_speed=old_vertical_speed
    horizontal_speed=old_horizonatal_speed





def print_game(game_started):
    global game_board,debug_message,wide_laser,score,port_coords,cutscene_active, port_extends

    #base monopoly board is 74 characters wide
    #25 Height



    if game_started :
        for row in range(len(game_board)):
            for col in range(len(game_board[row])):
                if not game_board[row][col] == " ":
                    game_board[row][col] = " "

        if cutscene_active:
            draw_text_structure(port,port_coords[0],port_coords[1])
            if port_extends>0:
                debug_message="aaaa"
                for extend in range(port_extends):

                    draw_text_structure(port_tube,port_coords[0]+1+extend,port_coords[1])
                    draw_text_structure(port_hatch,port_coords[0]+2+extend,port_coords[1])


        draw_text_structure(player_ship, player_x, player_y)




        for index in range(len(player_missle_coordinates)):
            draw_text_structure(player_missle, player_missle_coordinates[index][0], player_missle_coordinates[index][1])

        for index in range(len(asteroid_coordinates)):
            #debug_message="Asteroid x:"+str(asteroid_coordinates[index][0])+"Asteroid Y"+str(asteroid_coordinates[index][1])
            draw_text_structure(asteroid, asteroid_coordinates[index][0], asteroid_coordinates[index][1])
        #TODO add method for events to draw
        #wide_laser_logic=active_events_data[1]
        # for wide_laser_index ,wide_laser_data in enumerate(active_events_data[1][0]):
        #     if time.time()-wide_laser_index[1]>5:
        #         insert_text(wide_laser,wide_laser_index[0],len(game_board)//2)
        #     else:
        #         insert_text(wide_laser,wide_laser_index[0],0)
        #insert_flashing_text_structure(wide_laser,4,0,0)


    print(f"\033[2;0", end="")

    assembled_string=""
    for index,row in enumerate(game_board):
        for col in row:
            assembled_string+=col
        if not index ==len(game_board)-1:
            print(Style.RESET_ALL + f"\033[{index+4};{2}H", assembled_string, end="")
        assembled_string=""

    print(f"\033[4;2H","Score:"+str(score))

    print(f"\033[30;0H","Current Debug Message:"+debug_message)




    print(f"\033[30;0H","Current Debug Message:"+debug_message)
    #TODO FIX JITTER IN ASZTEROIDS WHEN BEING REMOVED

def print_instructions():
    global game_board
    welcome= "WELCOME"
    wel_x=len(game_board[0])//2
    wel_y=len(game_board)//2-10
    insert_text(welcome,wel_x,wel_y)

    insert_text("TO",wel_x,wel_y+1)

    title="DRUNK SPACE TRUCKER"
    insert_text(title,wel_x,wel_y+2)

    explanation1="THE GOAL IS SIMPLE"
    explanation2="YOU HAD ONE TOO MANY FUNNY SPACE DRINKS"
    explanation3="AND NOW YOU MUST SURVIVE"
    insert_text(explanation1,wel_x,wel_y+4)
    insert_text(explanation2,wel_x,wel_y+5)
    insert_text(explanation3,wel_x,wel_y+6)

    controls1="WASD(Normally) to move"
    controls2="Avoid the asteroids and react to the prompts"
    controls3="Tapping WASD works better than holding"
    insert_text(controls1,wel_x,wel_y+8)
    insert_text(controls2,wel_x,wel_y+9)
    insert_text(controls3,wel_x,wel_y+10)

def s_press():
    global player_y,vertical_speed
    random_event.possible_events[0].get_data()[1]=vertical_speed
    random_event.possible_events[0].get_data()[0]=0

    if (player_y+vertical_speed)<(len(game_board)-1):
        player_y=player_y+vertical_speed
def w_press():
    global player_y,vertical_speed,active_events_data
    random_event.possible_events[0].get_data()[1] = -vertical_speed
    random_event.possible_events[0].get_data()[0] = 0

    if (player_y-vertical_speed)>0:
        player_y = player_y -vertical_speed

def a_press():
    global player_x,horizontal_speed,active_events_data
    random_event.possible_events[0].get_data()[1] = 0
    random_event.possible_events[0].get_data()[0] = -horizontal_speed

    if (player_x-horizontal_speed)>0:
        player_x = player_x - horizontal_speed
def d_press():
    global player_x,horizontal_speed,active_events_data
    random_event.possible_events[0].get_data()[1] = 0
    random_event.possible_events[0].get_data()[0] = horizontal_speed

    if (player_x+horizontal_speed)<(len(game_board[0])-horizontal_speed):
        player_x = player_x + horizontal_speed

def wa_press():
    w_press()
    a_press()
def wd_press():
    w_press()
    d_press()

def sa_press():
    s_press()
    a_press()
def sd_press():
    s_press()
    d_press()

def space_press():
    global player_x,player_y
    player_missle_coordinates.append([player_x,player_y-2])
    #insert_text_structure(player_missle,player_x,(player_y+2))
def missle_logic():
    for index,coords in enumerate(player_missle_coordinates):
        coords[1]=coords[1]-1
        if coords[1]<0:
            player_missle_coordinates.pop(index)
#TODO add a loop that goes through events that contain collision logic and then detect if there
#is collision
def collision_logic():
    global player_x,player_y
    for a_index,a_coords in enumerate(asteroid_coordinates):
        asteroid_width_offset = len(asteroid[len(asteroid) // 2]) // 2
        asteroid_height_offset = len(asteroid) // 2
        for m_index,m_coords in enumerate(player_missle_coordinates):
            #gets half the width at the center of the asteroid

            if a_coords[0]-asteroid_width_offset <= m_coords[0] <= a_coords[0]+asteroid_width_offset:
                if a_coords[1] - asteroid_height_offset <= m_coords[1] <= a_coords[1] + asteroid_height_offset:
                    asteroid_coordinates.pop(a_index)
                    player_missle_coordinates.pop(m_index)

        if a_coords[0]-asteroid_width_offset <= player_x <= a_coords[0]+asteroid_width_offset:
            if a_coords[1]-asteroid_height_offset <= player_y <= a_coords[1]+asteroid_height_offset:
                player_alive=False


def asteroid_logic():
    global last_asteroid_time,asteroid_delay,last_asteroid_move_time

    if (time.time()-last_asteroid_time)>asteroid_delay:
        last_asteroid_time=time.time()
        width_asteroid=len(asteroid[len(asteroid) // 2])//2
        randomX=random.randint(width_asteroid,len(game_board[0])-width_asteroid)
        asteroid_coordinates.append([randomX,0])
    if (time.time() - last_asteroid_move_time) > 0.3:
        last_asteroid_move_time=time.time()
        for coords in asteroid_coordinates:
            if coords[1] + 1 > len(game_board) - 1:

                try:
                    asteroid_coordinates.remove(coords)
                except IndexError:
                    waka="waka"
            coords[1]=coords[1]+1





   # debug_message = "Random Event Active" + str(active_events_data[0][0])

def wide_vertical_lasers_event():
    global player_y,player_x,debug_message
    # Index 1 for active_events_data
    # #- Wide Vertical Lasers,[[[x,start_time]]],width of lasers,last laser creation time].

    if time.time()-active_events_data[1][-1]>1:

        active_events_data[1][-1]=time.time()
        width=active_events_data[1][1]

        randomX=random.randint(width,len(game_board[0])-width)
        active_events_data[1][0].append([randomX,time.time()])





def random_events():
    global debug_message

    if (time.time()-random_event.last_event_time)>random_event.delay:

        #TODO Make it so that the duration for each event progressively increases so it gets even MORE CHAOTIC
        randIndex=random.randint(0,len(random_event.possible_events)-1)
        if random_event.possible_events[randIndex].active==False:
            random_event.possible_events[randIndex].active=True
            random_event.last_event_time=time.time()
            random_event.possible_events[randIndex].start_time=time.time()

    for events in random_event.possible_events:

        if events.active==True:
            debug_message = "going through events"

            events.logic()

    #TODO Move drift effect(was a random event) somewhere where it makes more sense
    drift_effect()
        #TODO EVENT IDEAS 1)Go to x side of screen, 2) Laser Beams, Honk?, Honk is Now Missles? Backwards Controls

def score_logic():
    global score, lastTimeScore,distance
    if (time.time()-lastTimeScore)>lastTimeScoreDelay:
        lastTimeScore=time.time()
        score=score+1
        distance=distance+1

def cutscene_logic():
    global cutscene_active
    global distance
    if distance%5==0:
        cutscene_active=True
        port_cutscene()





def game_logic():
    missle_logic()
    asteroid_logic()
    collision_logic()
    random_events()
    score_logic()
    cutscene_logic()







def play():
    global game_board,debug_message
    width=74
    height=25

    os.system('cls' if os.name == 'nt' else 'clear')


    game_board = [[" " for i in range(width)] for j in range(height)]

    keyboard.add_hotkey("s",s_press)
    keyboard.add_hotkey("w",w_press)
    keyboard.add_hotkey("a",a_press)
    keyboard.add_hotkey("d",d_press)

    keyboard.add_hotkey("w+a",wa_press)
    keyboard.add_hotkey("w+d",wd_press)
    keyboard.add_hotkey("s+a",sa_press)
    keyboard.add_hotkey("s+d",sd_press)

    keyboard.add_hotkey("space",space_press)


    #EVENT DATA
    drift= random_event("drift",1000,[0, 0, 0.0],False)
    lasers1= random_event("laser",1000,[],False)
    lasers2= random_event("laser2",1000,[],False)

    #active_events.append([0,0,"drift"])

    # for int in range(active_events_data[1][1]):
    #     wide_laser[0].append("|")
    # for int in range(height):
    #     wide_laser.append(wide_laser[0])

    flashing_structures_info.append([True,time.time(),0.5])


    print("")
    print("")

    print("_"*(len(game_board[0])+4))

    for row in game_board:
        all_cols=""
        for col in row:
            all_cols+=str(col)
        print("|", all_cols,"|")
    print("_"*(len(game_board[0])+4))


    print_game(False)
    game_over=False
    random_event_last_time=time.time()
    old_time=time.time()

    instruction_time=time.time()
    while time.time()-instruction_time<5:
        print_instructions()
        print_game(False)






    while not game_over:
        #input("Please input your move: ")s
        print_game(True)
        if (time.time()-old_time)>0.1:
            old_time=time.time()
            game_logic()




if __name__ == '__main__':
    play()