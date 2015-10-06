class Questions:
    
    def __init__(self,question,topic,tags):
        
        self.topic  = topic
        self.question = question
        self.tags = tags
    
    def __getattr__(self, name):
        if name in self.tags.keys():
            if name == "result":
                if self.tags[name] == None:
                    return None
                else:
                    return int(self.tags[name])
            else:
                return self.tags[name]
        else:
            # Default behaviour
            raise AttributeError
        
    def __str__(self):
        
        str = "---=== T:%s ===---\nQ:%s\n" % (self.topic,self.question)
        
        for tag in self.tags:
            
            if self.tags[tag] != None:
                
                if tag == "result":
                    
                    str = str + "%s %s\n" % (tag,self.tags[tag])
                    
                else:
                
                    str = str + "%s %s\n" % (tag,self.tags[tag])
                
        return str.replace("L_BREAK", "\n")

def printSummary(qList):
    
    print "Summary of results" 
    
    from operator import attrgetter
    qList = sorted(qList, key=attrgetter('result'), reverse=False)
    
    for q in qList:
        
        print "R:%d\tQ:%s" % (q.result,q.question)
        
    #printQuestions(qList)

def printQuestions(qList):
    for q in qList:
        
        print q

def getQuestionBase():
    
    import os
    return os.getcwd()[:-4] +"questions\\"

def addResult(topic,question,incDec):
    
    print "Add result %d to topic %s Q %s" % (incDec,topic,question)

    import xml.etree.ElementTree as ET
    tree = ET.parse(getQuestionBase() + topic)
    root = tree.getroot()    
    
    for q in root.iter('question'):
        
        if q.get('value') == question:
            
            print "Match!!!!!!!!!!!!"
            if q.find('result') == None:
                
                ET.SubElement(q,'result')
                
            for res in q.iter("result"):
                
                if res.get("value") == None:
                    new_rank = incDec
                else:
                    new_rank = int(res.get("value")) + incDec

                res.set("value",str(new_rank))
    
    print "Write new tree"            
    tree.write(getQuestionBase() + topic)

    # reload list from topic?

def testTopic(qList):
    
    for q in qList:
        
        print
        print q.question
        
        if q.writtenAnswer <> None:
            
            print "(type)>"
            
            myAnswer = raw_input()
            
            # print "Compare %s %s" % (myAnswer,q.writtenAnswer)
            
            if(myAnswer == q.writtenAnswer):
                
                print "Correct!"
                addResult(topic,q.question,1)
                
            else:
                print "Improve answer!"
                addResult(topic,q.question,-1)
            
        
        elif 'answer' in q.tags.keys():
            
            print "(recall)"
            
            raw_input()
            
            print q.tags['answer']
            
            print "Where you correct?"
            
            if(raw_input() == "y"):
                
                addResult(topic,q.question,1)
                
            else:
                
                addResult(topic,q.question,-1)

def loadTopic(topic):
    
    path = getQuestionBase()
    
    #open xml topic
    import xml.etree.ElementTree as ET
    tree = ET.parse(path+topic)
    root = tree.getroot()
    
    qList = []
    
    
    for q in root.iter('question'):        
        tags = {'answer': None, 'movie' : None, 'image' : None, 'writtenAnswer' : None, 'result' : None}
        
        for tag in tags:
        
            for a in q.iter(tag):
                tags[tag] =  str(a.get("value")).replace("L_BREAK", "\n")
            
        qList.append(Questions(q.get("value"),topic,tags))
    
    return (qList)

if __name__ == "__main__":
        
    topic = 'fariaguard.xml'
    
    qList = loadTopic(topic)
    
    printQuestions(qList)
    
    testTopic(qList)
    
    qList = loadTopic(topic)
    
    printSummary(qList)
    
    """
    Add git repo outside workspace
    Add date for las correct answer
    Create material for course bash scripts etc
    Create material for git
    Create material for domain knowledge
<<<<<<< HEAD
    Create motor for levels of gamification
=======
    Skapa olika nivåer för gamification
>>>>>>> 1bf54d14333a2e0f4a080c40eda66342651aa408
    """