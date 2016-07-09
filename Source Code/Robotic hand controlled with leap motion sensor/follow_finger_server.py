import mraa
import time
import tornado.websocket

class ws(tornado.websocket.WebSocketHandler):
	x1 = mraa.Pwm(10)	#selecting pin for each fingure from thumb to pinky
        x2 = mraa.Pwm(9)
        x3 = mraa.Pwm(6)
        x4 = mraa.Pwm(5)
        x5 = mraa.Pwm(3)

	x1.period_us(4640)	#defining pwm period. as i've said earlier it should be 20ms but it better to work with 4640 micro second for me. but you try with 20 ms first
	x2.period_us(4640)
        x3.period_us(4640)
        x4.period_us(4640)
        x5.period_us(4640)

        x1.enable(True)	#enable all pins
        x2.enable(True)
        x3.enable(True)
        x4.enable(True)
        x5.enable(True)

	def open(self):
		print "connection open..."
	
	def on_message(self, m):
	#separate angle from message.
		angles = m.split('|')
                print self.angle_to_val(angles[0])
#write value on pwm pins
		ws.x1.write(self.angle_to_val(angles[0]))
                print self.angle_to_val(angles[1])
                ws.x2.write(self.angle_to_val(angles[1]))
                print self.angle_to_val(angles[2])
                ws.x3.write(self.angle_to_val(angles[2]))
                print self.angle_to_val(angles[3])
                ws.x4.write(self.angle_to_val(angles[3]))
                print self.angle_to_val(angles[4])
                ws.x5.write(self.angle_to_val(angles[4]))
	#map angle on pwm value
	def angle_to_val(self,angle):
		val = float(angle)*0.0023888
		return val+0.13


def main():
        application = tornado.web.Application([(r'/', ws)])
	application.listen(1234)			#starting websocket server
	tornado.ioloop.IOLoop.instance().start()
        try:
	    sys.stdin.readline()
	except KeyboardException:
	    pass
        finally:
            print "Thank you :)"
            ws.x.enable(False)
	
if __name__ == "__main__":
    main()

