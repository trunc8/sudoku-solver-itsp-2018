YStepsPerBlock = 225
XStepsPerBlock = 227
Delay = 0.0008

def cam_stepper_y():
    YStepCount = YStepsPerBlock * 10
    return YStepCount

def move_stepper_x(prev_x, cur_x):
    XStepCount = XStepsPerBlock * (cur_x - prev_x)
    return XStepCount
    

def move_stepper_y(prev_y, cur_y):
    YStepCount = YStepsPerBlock * (cur_y - prev_y)
    return YStepCount
    
def move_numwheel(pos):
    if pos==1:
        return 9.15
    elif pos==2:
        return 7.93
    elif pos==3:
        return 6.9
    elif pos==4:
        return 6.05
    elif pos==5:
        return 5.15
    elif pos==6:
        return 4.425
    elif pos==7:
        return 3.75
    elif pos==8:
        return 10.2
    elif pos==9:
        return 12.2
    else:
        return 9.2