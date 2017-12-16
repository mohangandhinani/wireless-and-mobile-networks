import nltk
import re
import aiml
import commands
import os
from nltk.corpus import wordnet as wn

cfd={}


#
#def ReadFile():
#	f = open("chatbot.txt")
#	lines = f.readlines()
#	for each in line:
#

#Define a function to learn Make Main Smaller.
	
	

#Mapping from Nltk's Pos tags to Wordnet's Pos tag
morphy_tag = {'NN':wn.NOUN,'JJ':'a','VB':'v','RB':'r'}
for tag, wnTag in morphy_tag.iteritems():
	#A separate dictionary for each part of speech
	cfd[wnTag] = {}


#CFD Dict must be separate for each datatype

def ProcessInp(inpToken):
    posToken = nltk.pos_tag(inpToken)
    wordDict = {}
    for posWord in posToken:
	word = posWord[0]
	try:
	    pos = morphy_tag[posWord[1][0:2]]
	#It is does not come under any of the 4 POS in Wordnet.Discard the word
	except:
	    continue
	if(wn.morphy(word,pos)):
	    #print "POS of "+word +" is " + pos
	    wordDict[pos] = word
    return wordDict


#TO learn more add more sentences to this File
f=open("question.txt","r");
input= f.readlines();
#Increase frequency of the particular word
class frequent:
    sentDict={}
    probSum=0.0
    def __init__(self,sent,prob):
        self.sentDict={}
        self.probSum=0.0
        for i in xrange(0,len(sent)):
            if sent[i] in self.sentDict.keys():
                self.sentDict[sent[i]] = self.sentDict[sent[i]]+prob
            else:
                self.sentDict[sent[i]] = prob
    def appendList(self,sent,prob):
        for i in xrange(0,len(sent)):
            if sent[i] in self.sentDict.keys():
                self.sentDict[sent[i]] = self.sentDict[sent[i]]+prob
            else:
                self.sentDict[sent[i]] = prob
    def getSum(self):
        if self.probSum>0:
            return self.probSum
        for key,val in self.sentDict.iteritems():
            self.probSum = self.probSum+val
        return self.probSum
    def getSentDict(self):
        return self.sentDict

def homework(inp):
    k = aiml.Kernel()
    k.learn("std-startup.xml")
    k.respond("load aiml b")
    os.system("clear")
    k.setBotPredicate("name", "Chatty")
    response = k.respond(inp)
    return response

def BuildCfd():
    File = {}
    for tag, wnTag in morphy_tag.iteritems():
	try:
	    File[wnTag] = open(wnTag+".dat","r")
	except:
	    tempFile = open(wnTag+".dat","w")
	    tempFile.close()
	    File[wnTag] = open(wnTag+".dat","r")
	cfdLines = File[wnTag].readlines()
	for Line in cfdLines:
	    cfdList = Line.split("::")
	    key = cfdList[0]
	    for i in xrange(1,len(cfdList)-1):
		if i%2==0:
		    continue
		if key in cfd[wnTag].keys():
		    cfd[wnTag][key].appendList([cfdList[i]],float(cfdList[i+1]))
		else:
		    cfd[wnTag][key] = frequent([cfdList[i]],float(cfdList[i+1]))

def writeFile():
    File = {}
    for tag, wnTag in morphy_tag.iteritems():
	File[wnTag] = open(wnTag+".dat","w")
    for pos,word in cfd.iteritems():
	for word, freqObj in cfd[pos].iteritems():
	    File[pos].write(word+'::')
	    sentDict = freqObj.getSentDict();
	    for sentence,frequency in sentDict.iteritems():
		File[pos].write(sentence+'::'+str(frequency)+'::')
	    File[pos].write(str(freqObj.getSum())+'\n');
    for tag, wnTag in morphy_tag.iteritems():
        File[wnTag].close()

    #Questions chatbot asks the Trainer
if __name__ == '__main__':
    BuildCfd()
    for inp in input:
	#If Last line and Input is an empty Line
	if not inp:
	    continue
        print 'Chatbot>'+inp+'\n'
        opList=[]
        
        opList.append(raw_input('You >> '))
        inp = re.sub("[^A-Za-z]"," ",inp)
        inp = inp.lower()
        inpToken = nltk.word_tokenize(inp)
        #For each token, append the result sentence and its share in the result
	wordDict = ProcessInp(inpToken)
        probToken =1.0/len(wordDict)
	#Write a function to split input token into Lists based on the Part of Speech
	
	for pos,word in wordDict.iteritems():
	    if word in cfd[pos].keys():
		cfd[pos][word].appendList([op for op in opList],probToken)
	    else:
		cfd[pos][word] = frequent([op for op in opList],probToken)
    writeFile()
def getCfd():
    BuildCfd()
    return cfd
