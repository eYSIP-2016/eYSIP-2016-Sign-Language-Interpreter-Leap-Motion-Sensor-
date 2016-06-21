
###THIS WILL BE RUN ON GALILEO BOARD###


import mraa
import time
import tornado.websocket

class ws(tornado.websocket.WebSocketHandler):					#websocket listener class
	x = mraa.Pwm(11)											#defining pwm pin it's 11
	x.period_us(4640)											#defining pwm period. as i've said earlier it should be 20ms but it better to work with 4640 micro second for me. but you try with 20 ms first
	x.enable(True)												#enable 11 pin for pwm
	def open(self):
		print "connection open..."
	
	def on_message(self, m):
		angle = int(m)											#m is message recived and it's angle and here it is convertingin to integer from string because message is recived in form of string
		ws.turn_servo(angle)									
	def turn_servo(angle):
		pwm_value = float(angle)*((.26+0.070)/180)+0.070		#mapping value with 0 to 180
		print pwm_value
		ws.x.write(pwm_value)


def main():
	ws.turn_servo(0)											#turn servo at initial position
	try:
		application = tornado.web.Application([(r'/', wshandle)])			#setup websocket at 1234 port
		application.listen(1234)
		tornado.ioloop.IOLoop.instance().start()
		sys.stdin.readline()
	except Exception:
		pass
	finally:
		controller.remove_listener(listener)
if __name__ == "__main__":
    main()

