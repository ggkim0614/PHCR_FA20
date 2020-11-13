# import necessary modules
from adafruit_circuitplayground import cp
from digitalio import DigitalInOut, Direction, Pull
import time
import board
import neopixel
import adafruit_hcsr04

# variables assigned for sonar sensor
sonar = adafruit_hcsr04.HCSR04(trigger_pin=board.A3, echo_pin=board.A2)

# function to find pattern
def find_array_pattern(data, pattern):
    count = 0
    for i in range(len(data)-len(pattern)+1):
        tmp = [data[i], data [i+1]]

        try:
            for j in range(len(data)-i):
                #print(i, i+j)
                if tmp[-1] != data[i+j+1]:
                    tmp.append(data[i+j+1])

                if len(tmp) == len(pattern):
                    #print(tmp)
                    break
        except:
            pass

        if tmp == pattern:
            count +=1

    return count


# loop this forEVER
while True:

    # variable declarations for the pushup loop
    pushup_counter = 0
    moveRecord = []

    # actual distance loop
    while True:
        print('looping loop')
        #print(moveRecord)

        if find_array_pattern(moveRecord, [1,2,1]) is 1:
            pushup_counter += 1
            moveRecord = []

        print('Number of push-ups: ', pushup_counter)


        # print distance value in cm
        # in push-up posture, the distance from upper body to the ground is approx. 37~40cm
        try:
            sonar_distance = sonar.distance
        # if in runtime error, make neopixel orange
        except RuntimeError:
            print("Runtime Error")
            continue


        # print('the distance is: ', sonar_distance, 'cm')
        # if distance is bigger than 25cm, make neopixel red
        if sonar_distance >= 25:
            cp.pixels[0] = (255, 0, 0)

            passing = True
            print('Going down')
            #time.sleep(1)
            moveRecord.append(1)

        # if in the process of push-up, blink with yellow
        elif sonar_distance < 25 and sonar_distance > 10:
            cp.pixels[0] = (255, 150, 0)

            print('Not there yet')
            #time.sleep(1)


        # if distance is less than 10cm, make neopixel teal
        elif sonar_distance <= 10:
            cp.pixels[0] = (0, 255, 50)

            print('Go up!')
            moveRecord.append(2)

    time.sleep(0.25)
