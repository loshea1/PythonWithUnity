
def aquisition_rest_position(filename):
    import os, sys, inspect, Leap, time
    import numpy as np
    sys.path.append(os.getcwd())
    import Coordinate_transformation
    # Leap_euler_angles = [2.355,0,0] # radians from Leap To TV ==> Desktop mode
    # Leap_translation = [0, 0.35, 0.55] # meter  y for the height z for the depth
    Leap_transformation = Coordinate_transformation.eulerAnglesToRotationMatrix()
    src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
    arch_dir = '../lib/x64' if sys.maxsize > 2 ** 32 else '../lib/x86'
    sys.path.insert(0, os.path.abspath(os.path.join(src_dir, arch_dir)))

    controller = Leap.Controller()
    ## Enable background apps for the Leap
    controller.set_policy(Leap.Controller.POLICY_BACKGROUND_FRAMES)

    aq_delay=5
    print("Setting Rest Position in %f seconds" %aq_delay)
    for i in xrange(aq_delay,0,-1):
        time.sleep(1)
        sys.stdout.write(str(i)+' ')
        sys.stdout.flush()
        
        
    frame = controller.frame()
    Hands = frame.hands
    
    if len(frame.hands) == 2:
        for hand in Hands:
            if Hands.leftmost==hand:
                hand_left_position = [hand.palm_position.x / 1000, hand.palm_position.y / 1000,
                                                                      hand.palm_position.z / 1000, 1] #hand.palm_position gives the position in millimiters
            else:
                hand_right_position = [hand.palm_position.x / 1000, hand.palm_position.y / 1000,
                                                                    hand.palm_position.z / 1000, 1]
        os.remove(filename)
        f = open(filename, 'a')
        f.write("%s,%s,%s,%s \n %s,%s,%s,%s" % (hand_left_position[0], hand_left_position[1],hand_left_position[2],1,
                                          hand_right_position[0], hand_right_position[1],hand_right_position[2],1))
        f.close()

        message_output = "Left and right hand rest positions have been recorded"
    
    elif len(frame.hands) == 0:
        message_output = "Don't be shy show your hands :) !"
    
    elif len(frame.hands) == 1:
        message_output = "One hand is missing !"
    
    else:
        message_output = "There are too many hands here !"

    return message_output
