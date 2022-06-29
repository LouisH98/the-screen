from sense_hat import SenseHat

sense = SenseHat()
sense.set_imu_config(False, True, False)

# Gets the rotation of The Screen, snapped to the closest 90 degree angle

def get_rotation():
    accel = sense.get_accelerometer_raw()
    x, y = round(accel['x']), round(accel['y'])

    direction = 99
    if x == -1:
        direction = 180
    elif y == 1:
        direction = 270
    elif y == -1:
        direction = 90
    else:  
        direction = 0
    
    return direction 

