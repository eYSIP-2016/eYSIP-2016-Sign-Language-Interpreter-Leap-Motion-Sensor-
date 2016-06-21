import os, sys, inspect, thread, time									#
src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))		#specify the location of librery of leap sdk
arch_dir = '../lib/x64' if sys.maxsize > 2**32 else '../lib/x86'		#
sys.path.insert(0, os.path.abspath(os.path.join(src_dir, arch_dir)))

import Leap
import os

class SampleListener(Leap.Listener):									#listener class
	def on_connect(self, controller):
		print "connected"												#this method calls when sensor is connected
	def on_frame(self, controller):										#this method calls when new frame arrives
		frame = controller.frame()										#get frame object
		hand = frame.hands[0]											#get hand objects means list of all available hands
		os.system("cls")								
		print "\nhands: %d,\nfingers: %d" % (len(frame.hands), len(frame.fingers))
																		#prints number of hands and number of fingures from all hands
def main():
	listener = SampleListener()											#creating the object of listener class
	controller = Leap.Controller()										#obtaing controller object
	controller.add_listener(listener)									#joining listener object with controller
	try:																#
		sys.stdin.readline()											#
	except KeyboardInterrupt:											#keep programe alive this ctrl+c
		pass															#
	finally:															#
		controller.remove_listener(listener)							#

if __name__ == '__main__':
    main()