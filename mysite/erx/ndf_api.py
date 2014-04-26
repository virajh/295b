import json, urllib2

#URL_NUI = 'http://rxnav.nlm.nih.gov/REST/Ndfrt/search?conceptName=%s'
#URL_CHECK = 'http://rxnav.nlm.nih.gov/REST/Ndfrt/interaction/nui1=%s&nui2=%s&scope=3'

def getNui(drug):
    print 'getNui'
    req = urllib2.Request("http://rxnav.nlm.nih.gov/REST/Ndfrt/search?conceptName=%s" % (drug))
    req.add_header('Accept', 'application/json')
    try:
        resp = urllib2.urlopen(req, timeout=1)
        content = json.loads(resp.read())
        try:
            print content['groupConcepts'][0]['concept'][0]['conceptNui']
            return content['groupConcepts'][0]['concept'][0]['conceptNui']
        except:
            return None
    except:
        return None

def checkDrugs(drug1, drug2):
    print 'checkDrugs'
    if drug1 == None or drug2 == None:
        return None

    req = urllib2.Request("http://rxnav.nlm.nih.gov/REST/Ndfrt/interaction/nui1=%s&nui2=%s&scope=3" % (drug1, drug2))
    print req, '$$$'

    req.add_header('Accept', 'application/json')
    try:
        resp = urllib2.urlopen(req, timeout=1)
        content = json.loads(resp.read())
        try:
            if content['fullInteractionGroup']['fullInteraction'][0]['interactionCount'] > 0:
                try:
                    return content['fullInteractionGroup']['fullInteraction'][0]['interactionTripleGroup'][0]['interactionTriple'][0]['severity']
                except:
                    return True
            else:
                return None
        except:
            return None
    except:
        return None

"""
#a= getNui('morphine')
#b= getNui('rasagiline')
#print a, b
#print checkDrugs(a,b)

c= getNUI('aspirin')
d= getNUI('isoniazid')
print a,b

"""
