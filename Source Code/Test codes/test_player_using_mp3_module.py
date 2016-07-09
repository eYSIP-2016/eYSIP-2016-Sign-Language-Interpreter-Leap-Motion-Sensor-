#####################################################################
#e-ySIP - 2016														#
#author: Sanket R. Bhimani(B.Tech. 2nd year Computer Engineering)	#
#June-2016															#
#####################################################################


###THIS WILL BE RUN ON GALILEO BOARD###


import mraa
import time
import binascii

u = mraa.Uart(0)			#get object of uart
u.setBaudRate(9600)				#set baudrate

play_pause_flag = 1
current_volume = 6
#some predefine commands
play_first_track = bytearray([0x7E,0xFF,0x06,0x03,0x00,0x00,0x01,0xFE,0xF7,0xEF])
play_from_sdcard = bytearray([0x7E,0xFF,0x06,0x09,0x00,0x00,0x02,0xFE,0xF0,0xEF])
play = bytearray([0x7E,0xFF,0x06,0x0D,0x00,0x00,0x00,0xFE,0xEE,0xEF])
pause = bytearray([0x7E,0xFF,0x06,0x0E,0x00,0x00,0x00,0xFE,0xED,0xEF])
next_track = bytearray([0x7E,0xFF,0x06,0x01,0x00,0x00,0x00,0xFE,0xFA,0xEF])
previous_track = bytearray([0x7E,0xFF,0x06,0x02,0x00,0x00,0x00,0xFE,0xF9,0xEF])
volume = bytearray([0x7E,0xFF,0x06,0x06,0x00,0x00,0xff,0xff,0xff,0xEF])


#param: volume hex array, value of volume in int
#return: new volume hex array
#working: generate hex array for volume
#example: hex_vol = make_volume(hex_vol, 10)
def make_volume(new_volume,value):
        print value
	if(value <= 30):
		if(value >= 0):
			volume_in_hex = hex(value)
                        print volume_in_hex
		else:
			volume_in_hex = hex(0)
	else:
		volume_in_hex = hex(30) 
	new_volume[6] = int(volume_in_hex,16)
	sum_of_data = hex(new_volume[1]+new_volume[2]+new_volume[3]+new_volume[4]+new_volume[5]+new_volume[6])
	
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
	final_check_bit = hex(int(binary_str,2)+int('1',2))
        print final_check_bit
        print int(final_check_bit,16)

        final_check_bit_list = list(final_check_bit)
        first_two_digit = "0x"+final_check_bit_list[2]+final_check_bit_list[3]
        second_two_digit = "0x"+final_check_bit_list[4]+final_check_bit_list[5]
        print first_two_digit
        print second_two_digit

        new_volume[7] = int(first_two_digit,16)
        new_volume[8] = int(second_two_digit,16)
        print binascii.hexlify(new_volume)
        return new_volume
	
def main():
	print "---wait for some seconds---"
	u.write(play_from_sdcard)
	time.sleep(12)
        u.write(make_volume(volume,current_volume))
        u.write(play_first_track)
        print "5: for play/pause"
        print "4: for previous track"
        print "5: for next track"
        print "8: for volume up"
        print "2: for volume down"

        while(True):
		choice = raw_input("Enter your choice: ")
		if(choice == 5):
			if(play_pause_flag == 0):
				u.write(play)
			elif(play_pause_flag == 1):
				u.write(pause)
		elif(choice == 4):
			u.write(previous_track)
		elif(choice == 6):
			u.write(next_track)		
		elif(choice == 8):
			u.write(make_volume(volume,current_volume+1))
		elif(choice == 2):
			u.write(make_volume(volume,current_volume-1))
			
if __name__ == "__main__":
    main()
