
###THIS WILL BE RUN ON PC###


import os, math, inspect, sys
src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
arch_dir = 'lib/x64' if sys.maxsize > 2**32 else 'lib/x86'
sys.path.insert(0, os.path.abspath(os.path.join(src_dir, arch_dir)))

import Leap
import websocket

class listener(Leap.Listener):
	cnt = 0														#counter to send every 12th frame so at slow rate angle is loaded in servo
	ws = websocket.create_connection("ws://169.254.6.158:1234")	#web socket connection with script running on board
	def on_connect(self,controller):				
		print "connected"
	def on_frame(self,controller):
		final_angle = ""
		listener.cnt += 1			
		frame = controller.frame()	
		hand = frame.hands[0]
		palm_pos_y = hand.palm_position[1]						#y axie of palm_position
		finger_index_pos_y = hand.pointables[0].tip_position[1]	#y axie of tip_position of index finger
		delta_pos = palm_pos_y - finger_index_pos_y	+ 12			#relative position of index finge's y axie with palm position's y axie
		angle = int(((delta_pos - 24) * (120-50) / (50 - 24)) + 50)						#mapping with 10 to 110 here minimum delta_pos is 0 and maximum delta_pos is 50
		if angle < 50:											#verify angle whether it is in between of 10 to 110
			angle = 50
		elif angle > 120:
			angle = 120
		final_angle = "%d" % (angle)
		
		palm_pos_y = hand.palm_position[1]						#y axie of palm_position
		finger_index_pos_y = hand.pointables[1].tip_position[1]	#y axie of tip_position of index finger
		delta_pos = palm_pos_y - finger_index_pos_y	+ 6			#relative position of index finge's y axie with palm position's y axie
		angle = int(((delta_pos - 24) * (175-90) / (50 - 24)) + 90)						#mapping with 10 to 110 here minimum delta_pos is 0 and maximum delta_pos is 50
		if angle < 90:											#verify angle whether it is in between of 10 to 110
			angle = 90
		elif angle > 175:
			angle = 175
		final_angle += "|%d" % (180-angle)
		
		
		palm_pos_y = hand.palm_position[1]						#y axie of palm_position
		finger_index_pos_y = hand.pointables[2].tip_position[1]	#y axie of tip_position of index finger
		delta_pos = palm_pos_y - finger_index_pos_y	+42			#relative position of index finge's y axie with palm position's y axie
		angle = int(((delta_pos - 24) * (185-85) / (50 - 24)) - 85)						#mapping with 10 to 110 here minimum delta_pos is 0 and maximum delta_pos is 50
		if angle < 85:											#verify angle whether it is in between of 10 to 110
			angle = 85
		elif angle > 185:
			angle = 185
		final_angle += "|%d" % (angle)
		
		
		palm_pos_y = hand.palm_position[1]						#y axie of palm_position
		finger_index_pos_y = hand.pointables[3].tip_position[1]	#y axie of tip_position of index finger
		delta_pos = palm_pos_y - finger_index_pos_y	+ 6			#relative position of index finge's y axie with palm position's y axie
		angle = int(((delta_pos - 24) * (170-90) / (50 - 24)) + 90)						#mapping with 10 to 110 here minimum delta_pos is 0 and maximum delta_pos is 50
		if angle < 95:											#verify angle whether it is in between of 10 to 110
			angle = 95
		elif angle > 170:
			angle = 170
		final_angle += "|%d" % (180-angle)
		
		palm_pos_y = hand.palm_position[1]						#y axie of palm_position
		finger_index_pos_y = hand.pointables[4].tip_position[1]	#y axie of tip_position of index finger
		delta_pos = palm_pos_y - finger_index_pos_y	+ 15		#relative position of index finge's y axie with palm position's y axie
		angle = int(((delta_pos - 24) * (175-115) / (50 - 24)) + 115)						#mapping with 10 to 110 here minimum delta_pos is 0 and maximum delta_pos is 50
		if angle < 115:											#verify angle whether it is in between of 10 to 110
			angle = 115
		elif angle > 175:
			angle = 175
		final_angle += "|%d" % (180-angle)
		
		
		if listener.cnt == 6:									#verify count is 12 for sending every 12th frame
			os.system("cls")
			print final_angle								#print and send angle to board through websocket
			listener.ws.send(final_angle)
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
	

		