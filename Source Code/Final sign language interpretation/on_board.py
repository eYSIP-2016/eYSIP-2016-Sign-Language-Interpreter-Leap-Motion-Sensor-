

#####################################################################
#e-ySIP - 2016														#
#author: Sanket R. Bhimani(B.Tech. 2nd year Computer Engineering)	#
#June-2016															#
#####################################################################

###THIS WILL BE RUN ON GALILEO BOARD###


import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.template
import json
import mraa
import time
import binascii

	


class WSHandler(tornado.websocket.WebSocketHandler):				#it is websocket listener class
#map for words to file number
    map_with_filename = [
			('THANK YOU','14'),
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
            ('YOUR','56'),
            ('TOILET','57'),
            ('FATHER','58'),
            ('FRIEND','59'),
            ('SORRY','60'),
            ('DONE','61'),
            ('HAVE', '62'),
            ('SLOW','63'),
            ('WRITE','64'),
            ('ALSO','65'),
            ('DIFFERENT','67'),
            ('SORRY','68'),
            ('UNDERSTAND','69'),
            ('OK','70'),
            ('EXCUSE ME','71'),
            ('WORK','72'),
            ('FRIEND','66')
         ]
                                                                                                                                                                                            
    play_from_sdcard = bytearray([0x7E,0xFF,0x06,0x09,0x00,0x00,0x02,0xFE,0xF0,0xEF])			#this is code for playing file from sdcard
    track_hex = bytearray([0x7E,0xFF,0x06,0x03,0x00,0x00,0xFF,0xFF,0xFF,0xEF])	#it is sample hex code for specifying track number. then we need to change chack bits and track number
    u = mraa.Uart(0)					#getting uart object
    u.setBaudRate(9600)					#setting baudrate
    u.write(play_from_sdcard)			#it is says mp3 module to play from sdcard
    def open(self):						#this method is called when new connection is established 
        print 'connection opened...'

    def on_message(self, message):		#this method is called when new message is arrived
        print message
	
		words = message.split(' ')		#split message with 'space' so each word from sentance can be differentiated 
		for i in words:
			for j in WSHandler.map_with_filename:
				if(j[0] == i):
					self.play_file(int(j[1]))
					break
			time.sleep(.4)
        




    def on_close(self):
        print 'connection closed...'

    def check_origin(self, origin):
        return True

		
		
#param: string (filename)
#return: none
#working: play given filenumver
#example: play_file("3")		
    def play_file(self,file_name):							#this method create hex code for playing specific file
        filename_hex = hex(file_name)
        WSHandler.track_hex[6] = int(filename_hex,16)		#it stores filename in hex code
        sum_of_data = hex(WSHandler.track_hex[1]+WSHandler.track_hex[2]+WSHandler.track_hex[3]+WSHandler.track_hex[4]+WSHandler.track_hex[5]+WSHandler.track_hex[6])		#now we will find chackbits
        binary_str = bin(int(sum_of_data,16))[2:].zfill(16)	#here hex string is  converted in binary string
        individual_digit = list(binary_str)				#converting binary string in character array
        count = 0						
        for i in individual_digit:
            if i == '0':								#here we are converting all 0 to 1 and all 1 to 0 to generate chack bits
                individual_digit[count] = '1'
            elif i == '1':
                individual_digit[count] = '0'
            count += 1

        binary_str = "".join(individual_digit)			#again convert character array to binary string
        final_check_bit = hex(int(binary_str,2) + int('1',2))				#converting it into hex code
        final_check_bit_list = list(final_check_bit)			
        first_two_digit = "0x"+final_check_bit_list[2] + final_check_bit_list[3]		
        second_two_digit = "0x"+final_check_bit_list[4] + final_check_bit_list[5]
        WSHandler.track_hex[7] = int(first_two_digit,16)			#storing generated chackbits to hex code
        WSHandler.track_hex[8] = int(second_two_digit,16)
        WSHandler.u.write(WSHandler.track_hex)						#sending hex data to mp3 module





application = tornado.web.Application([			#create object of websocket listener
    (r'/', WSHandler),
])

if __name__ == "__main__":
    application.listen(1234)						#set port number 1234
    tornado.ioloop.IOLoop.instance().start()		#start websocket server
    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
        pass
    finally:
        controller.remove_listener(listener)
