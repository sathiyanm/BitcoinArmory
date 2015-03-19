import hashlib
import json
import re

class PMTAUtil: 
    
    def convertEmailToPMTAFormat(self, email):
     pmtaFormattedString = None
     if re.match(r"[^@]+@[^@]+\.[^@]+", email):
       userid, domain = email.split('@')
       pmtaFormattedString = hashlib.sha224(userid).hexdigest()+"._pmta."+domain    
     return pmtaFormattedString
	  
    def createPMTARecord(self, email, bitCoinAddress):
	  return json.dumps({
       "domain" : str(self.convertEmailToPMTAFormat(email)), 
       "rrtype": "65337", 
       "rrdata" : "2 1 0 0 "+bitCoinAddress    
    }) 
