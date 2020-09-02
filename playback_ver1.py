import pyautogui
import pydirectinput
import autoit #need install pyautoit & autoit
from time import sleep, time
import os
import json

DELAY_BETWEEN_COMMANDS = 1.00

def main():
    
    initializepydirectinput()
    countdownTimer()

    buff()
    sleep(0.50)

    count = 0
    counts = 0
    while count <= 500:
        reLogIn()
        sleep(0.50)
        clickCamp()
        sleep(1.00)
        playActions("ride_pet.json")
        sleep(0.50)
        clickCamp()
        sleep(0.50)
        buff2()
        sleep(0.50)
        playActions("farm.json")
        sleep(2.00)
        clickCamp()
        sleep(5.00)  # Allow time for the teleport to camp and avoid server delay
        
        while counts <= 1000:
            
            counts += 1 
            print(counts)

            if (counts %11 == 0):
                buff()
                sleep(1.00)
                clickCamp()
                sleep(0.50)
            
            elif (counts %19 == 0):
                repair()
                sleep(1.00)
            
            elif (counts %161 == 0):
                cleanBag()
                sleep(1.00)         

            else:
                counts >= 1001
                break

    print("Done")


def initializepydirectinput():
    # Initialized pydirectinput
    pydirectinput.FAILSAFE = True


def countdownTimer():
    # Countdown timer
    print("Starting", end="", flush=True)
    for _ in range(0, 10):
        print(".", end="", flush=True)
        sleep(1)
    print("Go")


def playActions(filename):
    script_dir = os.path.dirname(__file__)
    filepath = os.path.join(
        script_dir, 
        'recordings', 
        filename
    )
    with open(filepath, 'r') as jsonfile:
        # parse the json
        data = json.load(jsonfile)
    
        # loop over each action
        for index, action in enumerate(data):
            action_start_time = time()

            # look for escape input to exit
            if action['button'] == 'Key.esc':
                break

            # perform the action
            if action['type'] == 'keyDown':
                key = convertKey(action['button'])
                pydirectinput.keyDown(key)
                print("keyDown on {}".format(key))
            elif action['type'] == 'keyUp':
                key = convertKey(action['button'])
                pydirectinput.keyUp(key)
                print("keyUp on {}".format(key))
            elif action['type'] == 'click':
                pydirectinput.click(action['pos'][0], action['pos'][1], duration=0.25)
                print("click on {}".format(action['pos']))

            # then sleep until next action should occur
            try:
                next_action = data[index + 1]
            except IndexError:
                # this was the last action in the list
                break
            elapsed_time = next_action['time'] - action['time']

            # if elapsed_time is negative, that means our actions are not ordered correctly. throw an error
            if elapsed_time < 0:
                raise Exception('Unexpected action ordering.')

            # adjust elapsed_time to account for our code taking time to run
            elapsed_time -= (time() - action_start_time)
            if elapsed_time < 0:
                elapsed_time = 0
            print('sleeping for {}'.format(elapsed_time))
            sleep(elapsed_time)


# convert pynput button keys into pydirectinput keys
# https://pynput.readthedocs.io/en/latest/_modules/pynput/keyboard/_base.html#Key
# https://pydirectinput.readthedocs.io/en/latest/keyboard.html
def convertKey(button):
    PYNPUT_SPECIAL_CASE_MAP = {
        'alt_l': 'altleft',
        'alt_r': 'altright',
        'alt_gr': 'altright',
        'caps_lock': 'capslock',
        'ctrl_l': 'ctrlleft',
        'ctrl_r': 'ctrlright',
        'page_down': 'pagedown',
        'page_up': 'pageup',
        'shift_l': 'shiftleft',
        'shift_r': 'shiftright',
        'num_lock': 'numlock',
        'print_screen': 'printscreen',
        'scroll_lock': 'scrolllock',
    }

    # example: 'Key.F9' should return 'F9', 'w' should return as 'w'
    cleaned_key = button.replace('Key.', '')

    if cleaned_key in PYNPUT_SPECIAL_CASE_MAP:
        return PYNPUT_SPECIAL_CASE_MAP[cleaned_key]

    return cleaned_key

def holdKey(key, seconds=1.00):
    pydirectinput.keyDown(key)
    sleep(seconds)
    pydirectinput.keyUp(key)
    sleep(DELAY_BETWEEN_COMMANDS)

def buff():
    holdKey('a', 0.50)
    holdKey('s', 0.50)
    holdKey('d', 0.50)
    holdKey('f', 1.00)
    holdKey('g', 1.00)


def buff2():
    holdKey('a', 0.50)
    holdKey('s', 0.50)
    holdKey('d', 0.50)

def clickCamp():
    autoit.mouse_click("left",27,105,3)
    sleep(2.00)
    autoit.mouse_click("left",152,153,3)
    sleep(4.00)

def reLogIn():
    autoit.mouse_click("left",973,944,3)
    sleep(4.00)
    autoit.mouse_click("left",958,999,2)
    sleep(9.00)


def avoidDeathChecker():
    clickCamp()
    sleep(0.5)
    playActions("clearOutMonster.json")
    sleep(1)
    clickCamp()
    sleep(1)
    reLogIn()
    sleep(1)
    playActions("ride_pet.json")
    sleep(1)
    clickCamp()
    sleep(1)

def repair():
    autoit.mouse_click("left",976,341,3)
    sleep(4.00)
    autoit.mouse_click("left",275,246,2)
    sleep(1.50)
    autoit.mouse_click("left",140,980,3)
    sleep(1.50)
    autoit.mouse_click("left",872,600,3)
    sleep(1.50)
    autoit.mouse_click("left",421,34,2)
    sleep(1.50)
    autoit.mouse_click("left",1459,38,2)
    sleep(1.50)
    holdKey('esc', 1.00)
    sleep(1.00)

def cleanBag():

    holdKey('q', 0.50)
    sleep(15.00)
    autoit.mouse_click("left",1863,48,10) #change server5 step1
    sleep(1.00)
    autoit.mouse_click("left",1717,165,10) #change server5 step2
    sleep(1.00)
    autoit.mouse_click("left",871,587,10) #change server5 step3
    sleep(15.00)
    playActions("goToBlackSmith.json") #walk to blacksmith
    sleep(1.00)
    holdKey('space', 1.00) #talk to balcksmith
    holdKey('space', 1.00) #talk to balcksmith2
    holdKey('space', 1.00) #talk to balcksmith(open table)
    sleep(1.00)
    autoit.mouse_click("left",968,629,1) #select item dismantle
    sleep(1.00) 
    autoit.mouse_click("left",1384,738,2) #see processed equ.
    sleep(1.00)
    autoit.mouse_click("left",1391,135,2) #click normal
    sleep(1.00)
    autoit.mouse_click("left",1494,135,2) #click magic
    sleep(1.00)
    autoit.mouse_click("left",1590,135,3) #click rare
    sleep(1.00)
    autoit.mouse_click("left",1691,135,2) #click unique
    sleep(1.00)
    autoit.mouse_click("left",1861,135,4) #click clear all
    sleep(1.00)
    autoit.mouse_click("left",1637,979,5) #dismantle item
    sleep(1.00)
    autoit.mouse_click("left",865,700,3) #say yes to dismantle item
    sleep(1.00)
    holdKey('esc', 0.50)
    sleep(1.00)
    autoit.mouse_click("left",619,106,2) #open dodo's portal shop
    sleep(1.00)
    autoit.mouse_click("left",351,244,2) #use outer15 portal
    sleep(1.00)
    autoit.mouse_click("left",872,597,3) #say yes to use outer15 portal
    sleep(10.00)
    autoit.mouse_click("left",1863,48,10) #change server3 step1
    sleep(2.00)
    autoit.mouse_click("left",1665,124,10) #change server3 step2
    sleep(2.00)
    autoit.mouse_click("left",882,589,10) #change server3 step3
    clickCamp()
    sleep(10.00)


if __name__ == "__main__":
    main()