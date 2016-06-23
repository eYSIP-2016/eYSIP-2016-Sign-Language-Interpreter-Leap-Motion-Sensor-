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

websocket.enableTrace(False)
ws = websocket.create_connection("ws://169.254.6.158:1234")

class listener(Leap.Listener):
	enable = 0
	main_enable = 0
	count = 0
	no_of_hand = 0
	data = []
	for l in xrange(300):							#no of frame
		data.append([])
		for i in xrange(2):							#no of hand
			data[l].append([])
			for j in xrange(5):						#no of fingre
				data[l][i].append([])
				for k in xrange(2):					#no of perameter direction and position
					data[l][i][j].append([])
	def on_frame(self, ctrl):
		if listener.enable == 1:
			frm = ctrl.frame()
			hand = frm.hands[0]
			hand_1 = frm.hands[1]
			pntbls = hand.pointables
			pntbls_1 = hand_1.pointables
			for i in xrange(5):
				listener.data[listener.count][0][i][0] = math.sqrt((pntbls[i].direction[0]) ** 2 + (pntbls[i].direction[2]) ** 2)
				listener.data[listener.count][0][i][1] = math.sqrt((pntbls[i].stabilized_tip_position[0]-hand.stabilized_palm_position[0]) ** 2 + (pntbls[i].stabilized_tip_position[2]-hand.stabilized_palm_position[2]) ** 2)
				if len(frm.hands) == 2:
					listener.data[listener.count][1][i][0] = math.sqrt((pntbls_1[i].direction[0]) ** 2 + (pntbls_1[i].direction[2]) ** 2)
					listener.data[listener.count][1][i][1] = math.sqrt((pntbls_1[i].stabilized_tip_position[0]-hand_1.stabilized_palm_position[0]) ** 2 + (pntbls_1[i].stabilized_tip_position[2]-hand_1.stabilized_palm_position[2]) ** 2)
			if len(frm.hands) == 2:
				listener.no_of_hand = 2
			else:
				listener.no_of_hand = 1
			listener.count += 1
			if listener.count == 300:
				listener.count = 0
				listener.enable = 0
				listener.main_enable = 1
				


class words:
	POSITION_RANGE = 18
	DIRECTION_RANGE = .18
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
		return json.dumps(self.__dict__)	
	def is_this(self,d):
		cnt = 0
		if self.no_of_hand == 1:
			for i in xrange(300):
				for j in xrange(300):
					count = 0
					for k  in xrange(5):
						if (d[j][0][k][0]<self.data[i][0][k][0]+ words.DIRECTION_RANGE and d[j][0][k][0]>self.data[i][0][k][0]-words.DIRECTION_RANGE) and (d[j][0][k][1]<self.data[i][0][k][1]+words.POSITION_RANGE and d[j][0][k][1]>self.data[i][0][k][1]-words.POSITION_RANGE):
							count += 1
					if count == 5:
						cnt += 1
			print '"',self.word,'"',float((cnt*100)/90000),"%",'(',cnt,')'
			if cnt >= 1000:
				return cnt
			else:
				return 0
		elif self.no_of_hand == 2:
			
			for i in xrange(300):
				for j in xrange(300):
					count = 0
					for k  in xrange(5):
						if (d[j][0][k][0] < (self.data[i][0][k][0]+words.DIRECTION_RANGE) and d[j][0][k][0] > (self.data[i][0][k][0]-words.DIRECTION_RANGE)) and (d[j][0][k][1] < (self.data[i][0][k][1]+words.POSITION_RANGE) and d[j][0][k][1] > (self.data[i][0][k][1]-words.POSITION_RANGE)) and (d[j][1][k][0] < (self.data[i][1][k][0]+words.DIRECTION_RANGE) and d[j][1][k][0] > (self.data[i][1][k][0]-words.DIRECTION_RANGE)) and (d[j][1][k][1] < (self.data[i][1][k][1]+words.POSITION_RANGE) and d[j][1][k][1] > (self.data[i][1][k][1]-words.POSITION_RANGE)):
							count += 1
					if count == 5:
						cnt += 1
			print '"',self.word,'"',float((cnt*100)/90000),"%",'(',cnt,')'
			if cnt >= 1000:
				return cnt
			else:
				return 0
				
def main():
	vakya = ""
	l = listener()
	c = Leap.Controller()
	c.add_listener(l)
	os.system('cls')
	wordss = []
	
	with open('a.json', 'r') as f:
		json_data = json.load(f)
		f.close()
	for i in xrange(len(json_data)):
		word = words(**json.loads(json_data["%d" % (i)]))
		wordss.append(word)
		print word.word
	while True:
		what = raw_input("training, recognizing, send whole sentance or clear sentance? (t/r/s/c) : ")
		if what == 't':
			print "training will start after 3 second"
			time.sleep(3)
			print "training started"
			listener.enable = 1
			while True:
				if listener.main_enable == 1:
					listener.main_enable = 0
					sentance = raw_input("Enter word or sentance: ")
					word = words(copy.deepcopy(listener.data), copy.deepcopy(sentance), copy.deepcopy(listener.no_of_hand))
					wordss.append(word)
					json_data = ""
					with open('a.json', 'r') as f:
						json_data = json.load(f)
						f.close()
					json_data["%d" % (len(json_data))] = word.to_JSON()
					with open('a.json', 'w') as f:
						json.dump(json_data, f)
						f.flush()
						f.close()
						
					listener.no_of_hand = 0				
					break
		elif what == 'r':
			print "recognizing will start after 3 second"
			time.sleep(3)
			print "recognizing started"
			listener.enable = 1
			while True:
				if listener.main_enable == 1:
					listener.main_enable = 0
					result = []
					for word in wordss:
						result.append(word.is_this(listener.data))
					max_cnt = max(result)
					max_index = result.index(max_cnt)
					print wordss[max_index].word
					vakya += wordss[max_index].word
					print "whole sentance: ",vakya
					break
		elif what == 'c':
			vakya = ""
			print "whole sentance is now cleared"
		elif what == 's':
			string = copy.deepcopy(vakya)
			vakya = ""
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
						final_string = self.grammar(final)
						print final_string
						ws.send(final_string.upper())
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
						final_string = self.grammar(final)
						print final_string
						ws.send(final_string.upper())
						return
		
				
				
		else:
			print "Invalid input please try again"
	gc.collect()
main()