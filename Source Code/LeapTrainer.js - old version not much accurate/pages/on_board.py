
###THIS WILL BE AT GALILEO BOARD SIDE###
###Whole documented code will be soon###

import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.template
import json
import mraa
import time
import binascii

u = mraa.Uart(0) #getting uart object
u.setBaudRate(9600)#setting baudrate

track_hex = bytearray([0x7E,0xFF,0x06,0x03,0x00,0x00,0xFF,0xFF,0xFF,0xEF])
#it is sample hex code for specifying track number. then we need to change chack bits and track number

class WSHandler(tornado.websocket.WebSocketHandler):
#it is websocket listener class


    map_with_filename = [
            ('I FEEL SLEEPY', '9'),
            ('WHAT IS THIS', '16'),
            ('THE INTERNET IS NOT WORKING', '15'),
            ('ALL DONE', '1'),
            ('SORRY', '19'),
            ('I LIKE YOU', '10'),
            ("I DIDN'T UNDERSTAND WHAT YOU SAID", '8'),
            ('WHAT TO DO NEXT', '18'),
            ('GOODBYE, HAVE A NICE DAY', '2'),
            ('WHAT IS YOUR NAME', '17'),
            ('THANK YOU','14'),
            ('I AM HUNGRY', '5'),
            ('PLEASE, TURN ON THE LIGHT', '13'),
            ('I AM TRUSTY, I WANT WATER', '7'),
            ('I AM BUSY', '4'),
            ("IT'S VERY GOOD", '11'),
            ('HOW ARE YOU', '3'),
            ('I AM SO HAPPY', '6'),
            ('PLEASE, TURN ON THE FAN', '12'),
            ('HELLO', '20'),
            ('EAT','21'),
            ('COME','22'),
            ('GIRL','23'),
            ('HOME','24'),
            ('ASK','25'),
            ('MOTHER','26'),
            ('KNOW','27'),
            ('HOW','28'),
            ('DRIVE','29'),
            ('FATHER','30'),
            ('DRINK','31'),
            ('MY','32'),
            ('GIVE','33'),
            ('HELP','34'),
            ('GOOD','35'),
            ('BOY','36'),
            ('WAIT','37'),
            ('WHY','38'),
            ('WHERE','39'),
            ('YES','40'),
            ('SCHOOL','41'),
            ('WHICH','42'),
            ('SEE','43'),
            ('WATER','45'),
            ('TIME','46'),
            ('WHAT','47'),
            ('PLEASE','48'),
            ('WHO','49'),
            ('NO','50'),
            ('NAME','51'),
            ('PLAY','52'),
            ('TOILET','53'),
            ('YOU','44'),
            ('ARE','54'),
            ('IS','55'),
            ('YOUR','56')
         ]
                                                                                                                                                                                            
    play_from_sdcard = bytearray([0x7E,0xFF,0x06,0x09,0x00,0x00,0x02,0xFE,0xF0,0xEF])
    track_hex = bytearray([0x7E,0xFF,0x06,0x03,0x00,0x00,0xFF,0xFF,0xFF,0xEF])
    u = mraa.Uart(0)
    flg = 0
    flag = 0
    name = ""
    u.setBaudRate(9600)
    u.write(play_from_sdcard)
    def open(self):
		#this method is called when new connection is established 
        print 'connection opened...'
        self.write_message("The server says: 'Hello'. Connection was accepted.")
       
    def on_message(self, message):
		#this method is called when new message is arrived
       #there are different flag messages for specifik taks like,
	   #   "#456#"   for retraining
	   #	"#123#" for loading data to json file
	   # "#789#" for whole sentnces
        print message
        if message == "#123#":
            WSHandler.flg = 1
            print message
        elif message == "#789#":
            WSHandler.flag = 1
        elif WSHandler.flag == 1:
            WSHandler.flag = 0
            words = message.split(' ')
            for i in words:
                for j in WSHandler.map_with_filename:
                    if(j[0] == i):
                        self.play_file(int(j[1]))
                        break
                time.sleep(.15)
        elif WSHandler.flg == 1:
            WSHandler.name = message
            WSHandler.flg = 3
            print message,"added"
        elif message == "#456#":
            WSHandler.flg = 2
            print message
        elif WSHandler.flg == 2:
            with open('a.json', 'r') as f:
                data = json.load(f)
                data.pop(message, None)
                f.close()
            with open('a.json', 'w') as f:
                json.dump(data, f)
                f.flush()
                f.close()
            WSHandler.flg = 0
            print message,"deleted"
        elif WSHandler.flg == 3:
            with open('a.json', 'r') as f:
                data = json.load(f)
                data[WSHandler.name] = message
                f.close()
            with open('a.json', 'w') as f:
                json.dump(data, f)
                f.flush()
                f.close()
            WSHandler.flg = 0
            #print message
        else:
            print 'received:', message
            for i in WSHandler.map_with_filename:
                if(i[0] == message):
                    self.play_file(int(i[1]))
                    break;




    def on_close(self):
        print 'connection closed...'

    def check_origin(self, origin):
 		
#param: string (filename)
#return: none
#working: play given filenumver
#example: play_file("3")       return True

    def play_file(self,file_name):
        filename_hex = hex(file_name)#this method create hex code for playing specific file
        WSHandler.track_hex[6] = int(filename_hex,16)		#it stores filename in hex code
        sum_of_data = hex(WSHandler.track_hex[1]+WSHandler.track_hex[2]+WSHandler.track_hex[3]+WSHandler.track_hex[4]+WSHandler.track_hex[5]+WSHandler.track_hex[6])		#now we will find chackbits
        binary_str = bin(int(sum_of_data,16))[2:].zfill(16)	#here hex string is  converted in binary string
        individual_digit = list(binary_str)	#here hex string is  converted in binary string
        count = 0
        for i in individual_digit:
            if i == '0':
			#here we are converting all 0 to 1 and all 1 to 0 to generate chack bits
                individual_digit[count] = '1'
            elif i == '1':
                individual_digit[count] = '0'
            count += 1

        binary_str = "".join(individual_digit)
        final_check_bit = hex(int(binary_str,2) + int('1',2))
		#again convert
		#character array to binary string
        final_check_bit_list = list(final_check_bit)
        first_two_digit = "0x"+final_check_bit_list[2] + final_check_bit_list[3]
        second_two_digit = "0x"+final_check_bit_list[4] + final_check_bit_list[5]
        WSHandler.track_hex[7] = int(first_two_digit,16)#storing generated chackbits to hex code
        WSHandler.track_hex[8] = int(second_two_digit,16)
        u.write(WSHandler.track_hex)

#sending hex data to mp3 module




application = tornado.web.Application([
    (r'/', WSHandler),
	#create object of websocket listener
]) port number 1234

if __name__ == "__main__":
    application.listen(9090)					#set port number 1234
    tornado.ioloop.IOLoop.instance().start()		#start websocket server
    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
        pass
    finally:
        controller.remove_listener(listener)
