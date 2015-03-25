import re
import hashlib
import json
import os
from armoryengine.ALL import *
from armoryengine.ConstructedScript import PublicKeySource

####################################################################################################################
class PMTAUtil(object): 
    
    def convertEmailToPMTAFormat(self, email):
     pmtaFormattedString = None
     if re.match(r"[^@]+@[^@]+\.[^@]+", email):
       userid, domain = email.split('@')
       pmtaFormattedString = hashlib.sha224(userid).hexdigest()+"._pmta."+domain        
     return pmtaFormattedString
      
    def createPMTARecord(self, email, bitCoinAddress):
       pks1ChksumPres = PublicKeySource()
       pks1ChksumPres.initialize(False, False, False, False, False,addrStr_to_hash160(bitCoinAddress)[1], False)
       return json.dumps({
         "domain" : str(self.convertEmailToPMTAFormat(email)), 
         "rrtype": "65337", 
         "rrdata": binary_to_hex(pks1ChksumPres.serialize())
    }) 

####################################################################################################################
class ProvRestServiceClient(PMTAUtil):
    
    def __init__(self):
      super(ProvRestServiceClient, self).__init__()      
      self.apiPath= self.ConfigSectionMap("settings")['apipath']
      
    
    def ConfigSectionMap(self, section):
     import ConfigParser
     
     script_dir = os.path.dirname(__file__) 
     configFileName = "config.ini"
     apiConfigFile = os.path.join(script_dir, configFileName)

     Config = ConfigParser.ConfigParser()
     Config.read(apiConfigFile)     
     dict1 = {}
     options = Config.options(section)
     for option in options:
        try:
                dict1[option] = Config.get(section, option)
                if dict1[option] == -1:
                    logging.debug("skip: %s" % option)
        except:
                print("exception on %s!" % option)
                dict1[option] = None
        return dict1

    
 
    def authenticateUser(self, userName, passWord): 

     import urllib3     
     http = urllib3.PoolManager()
           
     self.userAuthUrl = self.apiPath + "USERRecord/" + str(userName) + "?password=" + str(passWord)

     response = http.request('GET', self.userAuthUrl)
     userAuthData = json.loads(response.data)

     success = False
     errorMessage = ""
     accessToken = ""
     if response.status == 200:
         accessToken = userAuthData['daneRecord']['api_access_token'] 
         success = True         
     elif response.status == 404 and userAuthData['result'] == "record not found":        
        message = "The email or password you entered is incorrect"     
     else:        
        message = "Service seems to unavailable now. Please try again later or contact your administrator"
     return success, accessToken, errorMessage

     
    def postPMTARecord(self, accessToken, userName, walletaddr): 
        
        import urllib3   
        from urllib3 import PoolManager, Timeout        
        manager = PoolManager(1)
        pmtaUtil = PMTAUtil()
            
        self.PMTAPostUrl = self.apiPath + "zoneRecord/" + str(pmtaUtil.convertEmailToPMTAFormat(userName)) +"?access_token="+str(accessToken)
        data_json = pmtaUtil.createPMTARecord(userName, walletaddr)                
        
        response = manager.urlopen('POST', self.PMTAPostUrl, headers={'Content-Type':'application/json'}, body=data_json)
      
        pmtaSuccessStatus = False
        pmtaErrorMessage = ""
        print response.status
        if response.status == 201:
          pmtaSuccessStatus = True
        elif response.status == 401:          
          pmtaErrorMessage = "Unauthorized. Please contact your administrator"    
        else:
          pmtaErrorMessage = "Service seems to be unavailable now. Please try again later or contact your administrator"
        return pmtaSuccessStatus, pmtaErrorMessage
  

