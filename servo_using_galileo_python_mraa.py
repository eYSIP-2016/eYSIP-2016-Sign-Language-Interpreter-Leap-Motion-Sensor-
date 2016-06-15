#it's a raw copy well documented copy will be uploaded soon
import mraa
import time

x = mraa.Pwm(10)
x.period_us(4640)
x.enable(True)
#a(0)
def a(abcd):
#while True:
    init=0.13
    abcd = float(abcd)*0.0023888
    print abcd
    val = init+abcd
    x.write(val)
#    time.sleep(1)
#    while i<=.56:
#        x.write(i)
#        print i
#        time.sleep()
#        i += 0.001
    #break
#    time.sleep(1)
a(0)
def main():
    #i=0
    #while i<=180:
    #    a(i)
    #    i+=.1
    #    time.sleep(.1)
    while (True):
        input = raw_input("enter angle between 0 to 180: ")
        a(input)

if __name__ == "__main__":
    main()

