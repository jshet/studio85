
from time import sleep
import evdev
from select import select
from motion import *
from camera import *

gamepad = evdev.InputDevice('/dev/input/event0')
print(gamepad)

camera.start_preview()

motion_btns = {
    "UP":{"value":0, "steps": 10}, 
    "DOWN":{"value":0, "steps": -10},
    "BTN_A":{"value":0, "steps": 50}, 
    "BTN_B":{"value":0, "steps": -50}
    }
memory_btns = {
    "BTN_NORTH":{"value":0,"memory":100},
    "BTN_WEST":{"value":0,"memory":200},
    "BTN_TL":{"value":0,"memory":0},
    "BTN_TR":{"value":0,"memory":1199}
    }
setting_btns = {
    "BTN_SELECT":{"value":0},
    "BTN_MODE":{"value":0}
    }
camera_btns = {
    "BTN_START":{"value":0}
    }

configured_btns = [motion_btns, memory_btns, setting_btns, camera_btns]

def update_btn_value(btn_with_event, event):
    for btns in configured_btns:
        for b in btns:
           if b == btn_with_event:
                btns[b]['value'] = event.value
                return f"{b} in {btns} set to {event.value}"
    else:
        print(btn_with_event, event)

def set_memory_btn(position):
    for btn in memory_btns:
        btn = memory_btns[btn]
        if btn['value'] == 1:
            (btn['memory'], btn['value']) = (position, 0)
            print(f"{btn} set to {position}")                
    return position

def do(position):
    for btn in motion_btns:
        btn = motion_btns[btn]
        if btn['value'] == 1:                    
            end_position = move(btn['steps'], position)
            return end_position
    for btn in memory_btns:
        btn = memory_btns[btn]
        if btn['value'] == 1:
            if btn['memory'] == position:
                return position
            else:
                end_position = move(btn['memory'] - position, position)
            return end_position
    for btn in camera_btns:
        btn = camera_btns[btn]
        if btn['value'] == 1:
            take_pictures(memory_btns["BTN_NORTH"]["memory"], memory_btns["BTN_WEST"]["memory"])
            btn['value'] = 0
            return position
    else:
        return position

def main():
    position = 0
    first_move = True
    start_position = position
    print(f"Starting position: {position}")
    while True:
        r,w,x = select([gamepad.fd],[],[],0.01)
        if r:
            for event in gamepad.read():
                if event.type == evdev.ecodes.EV_KEY:
                    btn_with_event = evdev.categorize(event).keycode[0] if (len(evdev.categorize(event).keycode[0]) > 1) else evdev.categorize(event).keycode                    
                    changes = update_btn_value(btn_with_event,event)
                    print(changes)
                elif event.type == evdev.ecodes.EV_ABS:
                    abs_event = evdev.categorize(event).event
                    btn_with_event = evdev.ecodes.bytype[abs_event.type][abs_event.code]
                    if btn_with_event == "ABS_HAT0Y":
                        if abs_event.value == 1:
                            update_btn_value("UP", abs_event)
                        elif abs_event.value == -1:
                            abs_event.value = 1
                            update_btn_value("DOWN", abs_event)
                        elif abs_event.value == 0:
                            update_btn_value("UP", abs_event)
                            update_btn_value("DOWN", abs_event)
                else:
                    print(event)
                    print(evdev.categorize(event))
        
        if setting_btns['BTN_MODE']['value'] == 1:
            camera.start_preview()
            sleep(2)
            camera.stop_preview()

        if setting_btns['BTN_SELECT']['value'] == 1:
            position = set_memory_btn(position)
        else:
            end_position = do(start_position)
            if start_position != end_position:
                if first_move == True:
                    compensate_backlash("backward") if position < end_position else compensate_backlash()
                    first_move = False
                start_position = end_position
            elif (start_position == end_position) and end_position != position:
                compensate_backlash() if position < end_position else compensate_backlash("backward")
                position = end_position
                first_move = True

main()