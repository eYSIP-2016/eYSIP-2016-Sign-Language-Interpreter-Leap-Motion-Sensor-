import os, sys, inspect, thread, time
src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
arch_dir = '../lib/x64' if sys.maxsize > 2**32 else '../lib/x86'
sys.path.insert(0, os.path.abspath(os.path.join(src_dir, arch_dir)))

import Leap
import os
import math
import copy

class SampleListener(Leap.Listener):
    cnt = 0                                                                                         #this counter will use to take avg of 300 reading
    count = 0
    flg_main = 0
    flg = 0
    fr1 = [0, 0, 0, 0, 0]                                                                           #avg of direction will be stored
    fr2 = [0, 0, 0, 0, 0]                                                                           #avg of position with respect to center of palm
    def on_frame(self, controller):
        if SampleListener.flg == 1:                                                                 #this will enable to start taking reading
            if SampleListener.cnt == 300:
                for i in range(0, 5):
                    SampleListener.fr1[i] /= 300                                                    #take avg
                    SampleListener.fr2[i] /= 300
                    #print SampleListener.fr1[i]
                print("-------------------------------------------------------------------")
                SampleListener.cnt = 0                                                              #reset cnt anf all flg
                SampleListener.flg = 0
                SampleListener.flg_main = 1
            else:
                frame = controller.frame()
                hand = frame.hands[0]
                pointables = hand.pointables
                i = -1
                for pointable in pointables:
                    i = i + 1
                    SampleListener.fr1[i] += math.sqrt((pointable.direction[0]) ** 2 + (pointable.direction[2]) ** 2)
                    SampleListener.fr2[i] += math.sqrt((pointable.stabilized_tip_position[0]-hand.stabilized_palm_position[0]) ** 2 + (pointable.stabilized_tip_position[2]-hand.stabilized_palm_position[2]) ** 2)
                SampleListener.cnt = SampleListener.cnt + 1                                         #tip position - palm position so we get postion of tip with respect to palm centr

class letters:                                                              #letter class in which letter data is stored
    def _init(self):
        self.letter
        self.fing1                                                          #is mean of x & z direction like (x^2 + z^2)^.5
        self.fing2                                                          #is mean of x & z position like (x^2 + z^2)^.5

    def isthis(self,f1,f2):
        cnt =0
        for i in f1:
            if i>(self.fing1[cnt]+.12) or i<(self.fing1[cnt]-.12):
                return False
            cnt+=1
        cnt = 0
        for i in f2:
            if i>(self.fing2[cnt]+9) or i<(self.fing2[cnt]-9):
                return False
            cnt+=1
        return True

def main():
    listener = SampleListener()
    controller = Leap.Controller()                              #creating the object of controller
    controller.add_listener(listener)                           #load listenr object to controller object to start reciving data from controller
    obj = []                                                    #it's a object list in which all object data will be saved. this object have info releted what is the direction and position for perticuler letter
    os.system('cls')                                            #clear screen to make program good looking
    while 1==1:                                                 #infinite for loop to ask choice again and again
        what_to_do = raw_input("Enter your choice 'c' or 'l':")
        if what_to_do == "l":
            SampleListener.flg = 1                                                     #this flg enables the storing of data recived from sensor
            while 1==1:                                                                #this because we want to wait until flg_main in enabled
                if SampleListener.flg_main == 1:                                       #this flg is enabed from listener, this is because we want to know that the grabbing of data is completed in listener class so that we can use that data stored object and let program move forword
                    letter = letters()
                    letter.letter = raw_input("Enter letter:")
                    letter.fing1 = copy.deepcopy(SampleListener.fr1)                   #copis both direction and position vector megnitude in to particuler letter's object
                    letter.fing2 = copy.deepcopy(SampleListener.fr2)
                    obj.append(letter)
                    SampleListener.flg_main = 0                                        #this disable this part of code when it will be reused for next choice because we want to wait until data grabbing is completed
                    break                                                              #this will break inner for loop
        elif what_to_do == "c":
            SampleListener.flg = 1

            while 1==1:                                                                #same as above we want to wait until data grabing is completed
                #print obj[0].fing
                if SampleListener.flg_main == 1:

                    #print "###"
                    for o in obj:                                                       #will compare each object of obj list with currant value of position and direction
                        #print o.fing
                        #print SampleListener.fr1
                        asdf = SampleListener.fr1
                        abcd = SampleListener.fr2
                        a = o.isthis(asdf,abcd)
                        if a == True:                                                   #if value found, it will print that letter
                            print o.letter
                            break
                    SampleListener.flg_main = 0
                    break

    try:
        sys.stdin.readline()                                    #to keep program running until key is pressed  because we are using listener so to recive data from listener this will be helpful
    except KeyboardInterrupt:                                   #because we are using infinity while loop but still it should be here
        pass
    finally:
        controller.remove_listener(listener)
if __name__ == '__main__':
    main()