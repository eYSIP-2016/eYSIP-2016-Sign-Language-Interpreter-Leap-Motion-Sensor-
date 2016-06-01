import os, sys, inspect, thread, time
src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
arch_dir = '../lib/x64' if sys.maxsize > 2**32 else '../lib/x86'
sys.path.insert(0, os.path.abspath(os.path.join(src_dir, arch_dir)))

import Leap
import os

class SampleListener(Leap.Listener):
	cnt = 0
	def on_connect(self, controller):
		print "connected"
	def on_frame(self, controller):
		SampleListener.cnt = SampleListener.cnt+1
		#if SampleListener.cnt==9:
		frame = controller.frame()
		hand = frame.hands[0]
		cnt=0
		os.system("cls")
		#print hand.palm_position
		#print hand.basis.x_basis
		#print hand.basis.y_basis
		#print hand.basis.z_basis
		#print hand.palm_position
		#hand_transform = Leap.Matrix(hand.basis.x_basis, hand.basis.y_basis, hand.basis.z_basis, hand.palm_position)
		#hand_transform = hand_transform.rigid_inverse()
		#for finger in hand.fingers:
			#print hand_transform.transform_point(finger.tip_position)
			#print hand_transform.transform_direction(finger.direction)
		#print hand.direction.pitch
		print hand.direction
		print "\nhands: %d,\nfingers: %d" % (len(frame.hands), len(frame.fingers))
def main():
	listener = SampleListener()
	controller = Leap.Controller()

	controller.add_listener(listener)
	try:
		sys.stdin.readline()
	except KeyboardInterrupt:
		pass
	finally:
		controller.remove_listener(listener)

if __name__ == '__main__':
    main()