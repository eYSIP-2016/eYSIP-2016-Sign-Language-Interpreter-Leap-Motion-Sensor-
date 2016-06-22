
###THIS WILL BE RUN ON PC###


import os, math, inspect, sys
src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
arch_dir = '../lib/x64' if sys.maxsize > 2**32 else '../lib/x86'
sys.path.insert(0, os.path.abspath(os.path.join(src_dir, arch_dir)))

import Leap
import websocket

class listener(Leap.Listener):
	cnt = 0														#counter to send every 12th frame so at slow rate angle is loaded in servo
	ws = websocket.create_connection("ws://169.254.6.158:1234")	#web socket connection with script running on board
	def on_connect(self,controller):				
		print "connected"
	def on_frame(self,controller):
		listener.cnt += 1			
		frame = controller.frame()	
		hand = frame.hands[0]
		palm_pos_y = hand.palm_position[1]						#y axie of palm_position
		finger_index_pos_y = hand.pointables[1].tip_position[1]	#y axie of tip_position of index finger
		delta_pos = palm_pos_y - finger_index_pos_y				#relative position of index finge's y axie with palm position's y axie
		angle = int(delta_pos * 180 / 50)						#mapping with 0 to 180 here minimum delta_pos is 0 and maximum delta_pos is 50
		if angle < 0:											#verify angle whether it is in between of 0 to 180
			angle = 0
		elif angle > 180:
			angle = 180
		if listener.cnt == 12:									#verify count is 12 for sending every 12th frame
			os.system("cls")
			print "%d" % (angle)								#print and send angle to board through websocket
			listener.ws.send("%d" % (angle))
			listener.cnt = 0
l = listener()
c = Leap.Controller()
c.add_listener(l)
try:
	sys.stdin.readline()
except KeyboardInterrupt:
	pass
finally:
	c.remove_listener(l)
	

		