import sys, time, math

import pynput.keyboard as kb

from . import Leap


keyboard = kb.Controller()

class LeapMotionListener(Leap.Listener):
    NEW_GESTURE_DELAY = 0.5 # seconds
    last_time = None

    def on_init(self, controller):
        print('on init')
    
    def on_connect(self, controller):
        controller.set_policy(Leap.Controller.POLICY_BACKGROUND_FRAMES)
        controller.enable_gesture(Leap.Gesture.TYPE_SWIPE)
        
        controller.config.set("Gesture.Swipe.MinLength", 100.0)
        controller.config.set("Gesture.Swipe.MinVelocity", 750)
        
        print("Connected")
    
    def on_disconnect(self, controller):
        # Note: not dispatched when running in a debugger.
        print("Disconnected")

    def on_frame(self, controller):
        frame = controller.frame()
        
        for gesture in frame.gestures():
            if gesture.type == Leap.Gesture.TYPE_SWIPE:
                swipe = Leap.SwipeGesture(gesture)
                
                swipe_direction=swipe.direction
                
                gesture_direction = None
                if swipe_direction.z > 0.8 or swipe_direction.z < -0.8:
                    gesture_direction = 'Hit'
                elif(swipe_direction.x > 0 and math.fabs(swipe_direction.x) > math.fabs(swipe_direction.y)):
                    gesture_direction = 'Right'
                elif(swipe_direction.x < 0 and math.fabs(swipe_direction.x) > math.fabs(swipe_direction.y)):
                    gesture_direction = 'Left'
                elif(swipe_direction.y > 0 and math.fabs(swipe_direction.x) < math.fabs(swipe_direction.y)):
                    gesture_direction = 'Up'
                elif(swipe_direction.y < 0 and math.fabs(swipe_direction.x) < math.fabs(swipe_direction.y)):
                    gesture_direction = 'Down'
                
                if gesture_direction:
                    current_time = time.time()
                    if self.last_time is None or ((current_time - self.last_time) > self.NEW_GESTURE_DELAY):
                        print('new gesture:', gesture_direction)
                        self.last_time = current_time
                        keyboard.press('n')

def main():
    listener=LeapMotionListener()
    controller=Leap.Controller()
    controller.add_listener(listener)
    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
        pass
    finally:
        controller.remove_listener(listener)

if __name__ == "__main__":
    main()