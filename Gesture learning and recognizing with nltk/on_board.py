import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.template
import json
import mraa
import time
import binascii

u = mraa.Uart(0)
u.setBaudRate(9600)

track_hex = bytearray([0x7E,0xFF,0x06,0x03,0x00,0x00,0xFF,0xFF,0xFF,0xEF])


class WSHandler(tornado.websocket.WebSocketHandler):

    map_with_filename = [
            ('I FEEL SLEEP', '9'),
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
            ('HELLO', '20')
         ]
                                                                                                                                                                                            
    play_from_sdcard = bytearray([0x7E,0xFF,0x06,0x09,0x00,0x00,0x02,0xFE,0xF0,0xEF])
    track_hex = bytearray([0x7E,0xFF,0x06,0x03,0x00,0x00,0xFF,0xFF,0xFF,0xEF])
    u = mraa.Uart(0)
    flg = 0
    name = ""
    u.setBaudRate(9600)
    u.write(play_from_sdcard)
    def open(self):
        print 'connection opened...'
       #self.play_file(2)

    def on_message(self, message):
		if message == "#123#":
			WSHandler.flg = 1
		elif WSHandler.flg == 1:
			WSHandler.flg = 0
			for i in WSHandler.map_with_filename:
				if(i[0] == message):
					self.play_file(int(i[1]))
					break;
		else:
			words = message.split(' ')
            for i in words:
                for j in WSHandler.map_with_filename:
                    if(j[0] == i):
                        self.play_file(int(j[1]))
                        break
                time.sleep(.15)
        




    def on_close(self):
        print 'connection closed...'

    def check_origin(self, origin):
        return True

    def play_file(self,file_name):
        filename_hex = hex(file_name)
        WSHandler.track_hex[6] = int(filename_hex,16)
        sum_of_data = hex(WSHandler.track_hex[1]+WSHandler.track_hex[2]+WSHandler.track_hex[3]+WSHandler.track_hex[4]+WSHandler.track_hex[5]+WSHandler.track_hex[6])
        binary_str = bin(int(sum_of_data,16))[2:].zfill(16)
        individual_digit = list(binary_str)
        count = 0
        for i in individual_digit:
            if i == '0':
                individual_digit[count] = '1'
            elif i == '1':
                individual_digit[count] = '0'
            count += 1

        binary_str = "".join(individual_digit)
        final_check_bit = hex(int(binary_str,2) + int('1',2))
        final_check_bit_list = list(final_check_bit)
        first_two_digit = "0x"+final_check_bit_list[2] + final_check_bit_list[3]
        second_two_digit = "0x"+final_check_bit_list[4] + final_check_bit_list[5]
        WSHandler.track_hex[7] = int(first_two_digit,16)
        WSHandler.track_hex[8] = int(second_two_digit,16)
        u.write(WSHandler.track_hex)





application = tornado.web.Application([
    (r'/', WSHandler),
])

if __name__ == "__main__":
    application.listen(9090)
    tornado.ioloop.IOLoop.instance().start()
    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
        pass
    finally:
        controller.remove_listener(listener)
