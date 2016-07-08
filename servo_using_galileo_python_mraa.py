

#####################################################################
#e-ySIP - 2016														#
#author: Sanket R. Bhimani(B.Tech. 2nd year Computer Engineering)	#
#June-2016															#
#####################################################################


import mraa



import time

pwm = mraa.Pwm(10)			#define pin number on Galelio board
pwm.period_us(4640)			
#pwm period it should 20ms, but i have used 4640 microsecond.
# beacuse i am not getting proper result while using 20ms so i
# reach at 4640 microsecond after try and error. I don't know
#why it's working!!! but you try first with 20ms!

pwm.enable(True)				#it's enable pin 10 for generating pwm signle
#param: angle in int
#return: none
#working: turn the servo according tho given angle
#example: turn_servo(90)
def turn_servo(angle):
    pwm_value = float(angle)*((.26+0.070)/180)+0.070 
	#mapping with 0 to 180 degree
	#hear minimum value of pwm is 0.070 and maximum value of pwm is .26 
	print pwm_value
    pwm.write(pwm_value)		#writing generated pwm value to the pin

def main():
	turn_servo(0)
    while (True):
        input = raw_input("enter angle between 0 to 180: ")
        turn_servo(input)

if __name__ == "__main__":
    main()
	
###***I've not copiled this code after adding comments and changing variable name***###

