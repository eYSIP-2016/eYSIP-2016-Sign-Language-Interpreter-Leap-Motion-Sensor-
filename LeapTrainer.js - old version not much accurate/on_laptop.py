
###THIS WILL RUN AT PC SIDE###


import tornado.websocket
import nltk
from nltk.tokenize import PunktSentenceTokenizer
import sys
import urllib
import urlparse
from urllib2 import HTTPError
from urllib2 import URLError
import json
import websocket
#listener for websocket
class wshandle (tornado.websocket.WebSocketHandler):
	websocket.enableTrace(False)
	ws = websocket.create_connection("ws://169.254.6.158:9090")
		#make websocket connection with Galileo board
	def open(self):							#when some one connects with this system
		print "connection open..."
								
	def on_message(self, m):
		print "msg: "
		wshandle.ws.send("#789#")						
		self.make_sentence(m.lower())			#convert  sentance in lower case
	def on_close(self):
		print 'connection closed...'
	
	def check_origin(self, origin):
		return True
	def make_sentence(self,string):
		pst = PunktSentenceTokenizer(string)			
		t = pst.tokenize(string)
		
		word = nltk.word_tokenize(t[0])	#here we chunking sentance into word
		tagged = nltk.pos_tag(word)
										#here each word is tagged means it is noud, pronoun, etc... is recognized
		print tagged
		chunkGram = r"""WRB:{<WRB.?>*<WP>*<WDT>?}"""
		#REGEXP for detecting wh question
		chunkParser = nltk.RegexpParser(chunkGram)	#differentiate wh question
		chunked = chunkParser.parse(tagged)
		for subtree in chunked.subtrees():	#getting each word this will gives the output in tree form
			if subtree.label() == 'WRB':	# for only wh question
				for j in subtree.leaves():
					f = 0
					final = ""
					final += j[0]
					chunk = r"""VB: {<VBZ>*<VBP>?}"""							#here we are detecting type of wording and arranging it to proper place
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
					final_string = self.grammar(final)				#sending generated sentance to ginger grammer for correcting grammar
					print final_string
					wshandle.ws.send(final_string.upper())				#sending final sentance to board
					return
		chunkGram = r"""NN:{<PRP.?>*<NN.?>?}"""					#same thing like wh question is here for simple present tence sentance
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
					wshandle.ws.send(final_string.upper())
					return
					

				#this is for correcting grammar of generated sentence.
				#this method create url for ginger api					

#param: string
#return: url
#working: generates url with api key, input data and many other param
#example: url = get_ginger_url("what is you name"):		
	def get_ginger_url(self,text):
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

#param: string
#return: json object
#working: get response from generated url
#example: json = get_ginger_result("what is you name"):	


	def get_ginger_result(self,text):
#this method fatchs json result
		url = self.get_ginger_url(text)

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


#param: string
#return: final string
#working: correct grammar of enterd string
#example: string  = grammar("what is you name"):	
	def grammar(self,original_text):			#this method sends request for correcting grammar
		fixed_text = original_text
		results = self.get_ginger_result(original_text)

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


try:
	application = tornado.web.Application([(r'/', wshandle)])
	application.listen(1234)
	tornado.ioloop.IOLoop.instance().start()
	sys.stdin.readline()
except Exception:
	pass
finally:
	controller.remove_listener(listener)