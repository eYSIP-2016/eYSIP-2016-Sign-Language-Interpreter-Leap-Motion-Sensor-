import os, sys, inspect, thread, time
src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
arch_dir = '../lib/x64' if sys.maxsize > 2**32 else '../lib/x86'
sys.path.insert(0, os.path.abspath(os.path.join(src_dir, arch_dir)))

import Leap
import os
import math
import copy
import operator
import time
import gc
import json
from json import JSONEncoder
import websocket
import nltk
from nltk.tokenize import PunktSentenceTokenizer
import sys
import urllib
import urlparse
from urllib2 import HTTPError
from urllib2 import URLError
from getch import getch, pause
import numpy as np
websocket.enableTrace(True)
#ws = websocket.create_connection("ws://169.254.6.158:1234")



class NumPyArangeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist() # or map(int, obj)
        return json.JSONEncoder.default(self, obj)


class listener(Leap.Listener):
	sample = 300
	enable = 0
	main_enable = 0
	count = 0
	no_of_hand = 0
	data = []
	data_dir = []
	data_pos = []
	
					
					
	def on_frame(self, ctrl):
		if listener.enable == 1:
			frm = ctrl.frame()
			hand = frm.hands[0]
			hand_1 = frm.hands[1]
			pntbls = hand.pointables
			pntbls_1 = hand_1.pointables
			fing_data_pos = []
			fing_data_dir = []
			
			for i in xrange(5):
				a1 = float("%.2f" % (math.sqrt((pntbls[i].direction[0]) ** 2 + (pntbls[i].direction[2]) ** 2)))
				a2 = int(math.sqrt((pntbls[i].stabilized_tip_position[0]-hand.stabilized_palm_position[0]) ** 2 + (pntbls[i].stabilized_tip_position[2]-hand.stabilized_palm_position[2]) ** 2))
				fing_data_pos.append(a2)
				fing_data_dir.append(a1)
			if len(frm.hands) == 2:
				for i in xrange(5):
					a1 = float("%.2f" % (math.sqrt((pntbls_1[i].direction[0]) ** 2 + (pntbls_1[i].direction[2]) ** 2)))
					a2 = int((math.sqrt((pntbls_1[i].stabilized_tip_position[0]-hand_1.stabilized_palm_position[0]) ** 2 + (pntbls_1[i].stabilized_tip_position[2]-hand_1.stabilized_palm_position[2]) ** 2)))
					fing_data_pos.append(a2)
					fing_data_dir.append(a1)
			listener.data_dir.append(np.array(fing_data_dir).flatten())
			listener.data_pos.append(np.array(fing_data_pos).flatten())
			
					
			
			if len(frm.hands) == 2:
				listener.no_of_hand = 2
			else:
				listener.no_of_hand = 1
			listener.count += 1
			if listener.count == listener.sample:
				listener.data.append(listener.data_dir)
				listener.data.append(listener.data_pos)
				listener.data_dir = []
				listener.data_pos = []
				
				listener.count = 0
				listener.enable = 0
				listener.main_enable = 1
			
				


class words:
	word = ""
	data = []
	no_of_hand = 0
	def from_JSON(self,j):
		self.__dict__ = json.loads(j)
	def __init__(self, data, word, no_of_hand):
		self.word = word
		self.data = data
		self.no_of_hand = no_of_hand
	def to_JSON(self):
		return json.dumps(self.__dict__, cls=NumPyArangeEncoder)
	def is_this(self,d,n):
		#a = time.time()
		cnt = 0
		
		if (n == self.no_of_hand):
			
			d_dir = np.array(d[0])
			d_pos = np.array(d[1])
			dd_dir = np.array(self.data[0])
			dd_pos = np.array(self.data[1])
			for i in xrange(300):
				d_pos = np.roll(d_pos, 1, axis=0)
				d_dir = np.roll(d_dir, 1, axis=0)
				cnt += len(np.where(((abs(dd_dir-d_dir)<.18)&(abs(dd_pos-d_pos)<18)).all(axis=1))[0])
				
					
			
			
			
			#r1 = abs(self.data[0]-d[0])<.18
			#print abs(self.data[0]-d[0])

			#r2 = abs(self.data[1]-d[1])<18
			#print abs(self.data[1]-d[1])
			#final = r1&r2
			#print final
			#cnt = len(np.where(final.all(axis=1))[0])
			
			
			print self.word,' (',cnt,') ',cnt*100/(300*300),'%'
			#print time.time()-a
			return cnt	
		
			

				
				
def get_ginger_url(text):
	API_KEY = "6ae0c3a0-afdc-4532-a810-82ded0054236"

	scheme = "http"
	netloc = "services.gingersoftware.com"
	path = "/Ginger/correct/json/GingerTheText"
	params = ""
	query = urllib.urlencode([
		("lang", "US"),
		("clientVersion", "2.0"),
		("apiKey", API_KEY),
		("text", text)])
	fragment = ""

	return(urlparse.urlunparse((scheme, netloc, path, params, query, fragment)))


def get_ginger_result(text):

	url = get_ginger_url(text)
	try:
		response = urllib.urlopen(url)
	except HTTPError as e:
			print("HTTP Error:", e.code)
			quit()
	except URLError as e:
			print("URL Error:", e.reason)
			quit()
	except IOError, (errno, strerror):
		print("I/O error (%s): %s" % (errno, strerror))
		quit

	try:
		result = json.loads(response.read().decode('utf-8'))
	except ValueError:
		print("Value Error: Invalid server response.")
		quit()

	return(result)


def grammar(original_text):
	fixed_text = original_text
	results = get_ginger_result(original_text)

	# Correct grammar
	if(not results["LightGingerTheTextResult"]):
		return(original_text)

	# Incorrect grammar
	fixed_gap = 0
	for result in results["LightGingerTheTextResult"]:
		if(result["Suggestions"]):
			from_index = result["From"]
			to_index = result["To"] + 1
			suggest = result["Suggestions"][0]["Text"]
			incorrect = original_text[from_index:to_index]
			original_text = original_text[:from_index] + incorrect + original_text[to_index:]
			fixed_text = fixed_text[:from_index-fixed_gap] + suggest + fixed_text[to_index-fixed_gap:]
			fixed_gap += to_index-from_index-len(suggest)
	return(fixed_text)				
			
			
				

def natural_sentence(string):
	pst = PunktSentenceTokenizer(string)
	t = pst.tokenize(string)

	word = nltk.word_tokenize(t[0])
	tagged = nltk.pos_tag(word)
	print tagged
	chunkGram = r"""WRB:{<WRB.?>*<WP>*<WDT>?}"""
	chunkParser = nltk.RegexpParser(chunkGram)
	chunked = chunkParser.parse(tagged)
	for subtree in chunked.subtrees():
		if subtree.label() == 'WRB':
			for j in subtree.leaves():
				f = 0
				final = ""
				final += j[0]

				chunk = r"""VB: {<VBZ>*<VBP>?}"""
				cp = nltk.RegexpParser(chunk)
				word = nltk.word_tokenize(t[0])
				tagged = nltk.pos_tag(word)
				ch = cp.parse(tagged)
				flg = 0
				for subtree in ch.subtrees():
					if subtree.label() == 'VB':
						for j in subtree.leaves():
							final += " "+j[0]

							flg = 1
						break
				if flg == 0:
					final += " is"

				chunk = r"""PRP: {<PRP.?>?}"""
				cp = nltk.RegexpParser(chunk)
				ch = cp.parse(tagged)
				for subtree in ch.subtrees():
					if subtree.label() == 'PRP':
						for j in subtree.leaves():
							final += " "+j[0]

				chunk = r"""PRP: {<JJ.?>?}"""
				cp = nltk.RegexpParser(chunk)
				ch = cp.parse(tagged)
				for subtree in ch.subtrees():
					if subtree.label() == 'PRP':
						for j in subtree.leaves():
							final += " "+j[0]

				chunk = r"""PRP: {<RB.?>?}"""
				cp = nltk.RegexpParser(chunk)
				ch = cp.parse(tagged)
				for subtree in ch.subtrees():
					if subtree.label() == 'PRP':
						for j in subtree.leaves():
							final += " "+j[0]

				chunk = r"""PRP: {<VB.?>?}"""
				cp = nltk.RegexpParser(chunk)
				ch = cp.parse(tagged)
				for subtree in ch.subtrees():
					if subtree.label() == 'PRP':
						for j in subtree.leaves():
							final += " "+j[0]

				chunk = r"""NN: {<NN.?>?}"""
				cp = nltk.RegexpParser(chunk)
				ch = cp.parse(tagged)
				for subtree in ch.subtrees():
					if subtree.label() == 'NN':
						for j in subtree.leaves():
							if f == 0:
								final += " "+j[0]
								f = 1
							else:
								final += " of "+j[0]
				f = 0
				print final
				final_string = grammar(final)
				print final_string
				#ws.send(final_string.upper())
				return
	chunkGram = r"""NN:{<PRP.?>*<NN.?>?}"""
	chunkParser = nltk.RegexpParser(chunkGram)
	chunked = chunkParser.parse(tagged)
	for subtree in chunked.subtrees():
		if subtree.label() == 'NN':
			for j in subtree.leaves():
				f = 0
				w = nltk.word_tokenize(string)
				w.remove(j[0])
				final = ""
				final += " "+j[0]
				chunk = r"""VB: {<VBP>*<VBZ>*<VB>*<VB.?>*<MD.?>?}"""
				cp = nltk.RegexpParser(chunk)
				word = nltk.word_tokenize(t[0])
				tagged = nltk.pos_tag(word)
				ch = cp.parse(tagged)
				flg = 0
				for subtree in ch.subtrees():
					if subtree.label() == 'VB':
						for j in subtree.leaves():
							w.remove(j[0])
							final += " "+j[0]
							flg = 1
						break
				if flg == 0:
					final += " is"
				chunk = r"""PRP: {<PRP.?>?}"""
				cp = nltk.RegexpParser(chunk)

				ch = cp.parse(nltk.pos_tag(w))
				for subtree in ch.subtrees():
					if subtree.label() == 'PRP':
						for j in subtree.leaves():
							final += " "+j[0]

							w.remove(j[0])
				chunk = r"""NN: {<NN.?>?}"""
				cp = nltk.RegexpParser(chunk)
				ch = cp.parse(nltk.pos_tag(w))
				for subtree in ch.subtrees():
					if subtree.label() == 'NN':
						for j in subtree.leaves():
							if f == 0:
								final += " "+j[0]
								f = 1
							else:
								final += " of "+j[0]
							w.remove(j[0])
				f = 0
				for wrd in w:
					final += " "+wrd
				print final
				final_string = grammar(final)
				print final_string
				#ws.send(final_string.upper())
				return



				
def main():

	flg = 0
	vakya = "what name you"
	l = listener()
	c = Leap.Controller()
	c.add_listener(l)
	os.system('cls')
	wordss = []
	count = 1
	with open('data.json', 'r') as f:
		json_data = json.load(f)
		f.close()
	for i in json_data:
		word = words(**json.loads(json_data[i]))
		wordss.append(word)
		print count,' ',word.word
		count += 1
	while True:
		if flg == 1:
			what = 'r'
			flg = 0
		else:
			print "training, recognizing, send whole sentance or clear sentance? (t/r/s/c) : "
			what = getch()
		if what == '\x03':
			exit()
		if what == 't':
			print "training will start after 3 second"
			for i in xrange(3):
				print i+1
				time.sleep(1)
			print "training started"
			listener.enable = 1
			while True:
				if listener.main_enable == 1:			
					listener.main_enable = 0
					sentance = raw_input("Enter word or sentance: ")
					word = words(copy.deepcopy(np.array(listener.data)), copy.deepcopy(sentance), copy.deepcopy(listener.no_of_hand))
					
					result = []
					wordss.append(word)
					print "chacking..."
					for word in wordss:
						result.append(word.is_this(np.array(listener.data), listener.no_of_hand))
					max_cnt = max(result)
					if max_cnt > 9:
						max_index = result.index(max_cnt)
						listener.no_of_hand = 0
						print wordss[max_index].word
						
					aaa = getch()
					
					if aaa == '\x03':
						wordss.remove(word)
						break
					
					json_data = ""
					with open('data.json', 'r') as f:
						json_data = json.load(f)
						f.close()
					json_data[sentance] = word.to_JSON()
					with open('data.json', 'w') as f:
						json.dump(json_data, f)
						f.flush()
						f.close()
					listener.no_of_hand = 0	
					listener.data = []
					break
		elif what == 'r':
			print "recognizing will start after 3 second"
			for i in xrange(3):
				print i+1
				time.sleep(1)
			print "recognizing started"
			listener.enable = 1
			while True:
				if listener.main_enable == 1:
					listener.main_enable = 0
					result = []
					print "chacking..."
					for word in wordss:
						result.append(word.is_this(np.array(listener.data), listener.no_of_hand))
					max_cnt = max(result)
					if max_cnt > 9:
						max_index = result.index(max_cnt)
						listener.no_of_hand = 0
						print wordss[max_index].word
						vakya += " "+wordss[max_index].word
						print "whole sentance: ",vakya
					else:
						print "try again"
						flg = 1
					listener.data = []
					break
		elif what == 'c':
			vakya = ""
			print "whole sentance is now cleared"
		elif what == 's':
			natural_sentence(copy.deepcopy(vakya))
			vakya = ""
			
						
		
				
				
		else:
			print "Invalid input please try again"
	gc.collect()
main()