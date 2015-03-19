import urllib3
import requests
import json
import re
import sys
sys.path.append('..')
from qtdialogs import PMTAUtil


class ProvRestServiceClient(object):
    
    def __init__(self, parent=None, main=None):
      # super(ProvRestServiceClient, self).__init__(parent, main)      
      self.apiPath= self.ConfigSectionMap("settings")['apipath']   
      
    
    def ConfigSectionMap(self, section):
     import ConfigParser
     Config = ConfigParser.ConfigParser()
     Config.read("config.ini")     
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


    def grantAccess(self, email, userName, accessToken):

     import urllib3   
     from urllib3 import PoolManager        
     manager = PoolManager(1)

     self.userAuthUrl = self.apiPath + "azn/EXPERIMENTAL/65337/" +str(PMTAUtil().convertEmailToPMTAFormat(email)) +"/"+ str(userName) + "?access_token=" + str(accessToken) 
     print self.userAuthUrl
     userRecord = {
      "domain":"4468473c8ee7c20f1df21d2aa173364c5a96c22efc1381f5a196cc5d._pmta.test.com", 
      "exact":"true",
      "priv_grant_record":"true",
      "priv_grant_user":"true"
     }
     userRecord['domain'] = PMTAUtil().convertEmailToPMTAFormat(email)
     headers = {'Content-Type':'application/json'}         
     data_json = json.dumps(userRecord)
     response = manager.urlopen('POST', self.userAuthUrl, headers={'Content-Type':'application/json'}, body=data_json)
     print response.status

    def authenticateUser(self, userName, passWord): 

     import urllib3     
     http = urllib3.PoolManager()           
     self.userAuthUrl = self.apiPath + "USERRecord/" + str(userName) + "?password=" + str(passWord)

     #Rest call to authenticate User Name and password     
     response = http.request('GET', self.userAuthUrl)
     userAuthData = json.loads(response.data)
     print response.data

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
        from socket import timeout

        manager = PoolManager(1)
        pmtaUtil = PMTAUtil()
        
        self.PMTAPostUrl = self.apiPath + "zoneRecord/" + str(pmtaUtil.convertEmailToPMTAFormat(userName)) +"?access_token="+str(accessToken)
        headers = {'Content-Type':'application/json'}         
        data_json = pmtaUtil.createPMTARecord(userName, walletaddr)               
        
        response = manager.urlopen('POST', self.PMTAPostUrl, headers={'Content-Type':'application/json'}, body=data_json)


        try:
            response = urllib.request.urlopen(url, timeout=10).read().decode('utf-8')
        except (HTTPError, URLError) as error:
            logging.error('Data of %s not retrieved because %s\nURL: %s', name, error, url)
        except timeout:
            logging.error('socket timed out - URL %s', url)
        else:
            logging.info('Access successful.')
             
            
        
        pmtaSuccessStatus = False
        pmtaErrorMessage = ""
        print response.status
        if response.status == 201:
          pmtaSuccessStatus = True
        elif response.status == 401:          
          pmtaErrorMessage = "Unauthorized. Please contact your administrator"    
        else:
          pmtaErrorMessage = "Service seems to unavailable now. Please try again later or contact your administrator"
        return pmtaSuccessStatus, pmtaErrorMessage
 
    def createUser(self, newUserRecord):
       import urllib3   
       from urllib3 import PoolManager, Timeout        
       manager = PoolManager(1)
       if newUserRecord is not None:
        newUserRecord=newUserRecord
       else:
        newUserRecord = {
        'email':  'testuser1@test.com',
        'password':'123456',
        'username':'testuser1',
        'firstName':'Test',
        'lastName':'User',
        'api_access_token':'testToken'
       }
       headers = {'Content-Type':'application/json'}   
       self.createUserPath = self.apiPath + "USERRecord?"
       #postUrl =  'http://10.175.169.11:3000/api/v1/USERRecord'
       # postUrl = self.PMTAPostUrl+'/USERRecord'
       data_json = json.dumps(newUserRecord)
       response = manager.urlopen('POST', self.createUserPath, headers={'Content-Type':'application/json'}, body=data_json)
       if response.status == 201:
        return response.status
       else :
        return response.status
       

    # print authenticateUser("testuser1@test.com", "123456")   
  
    
    def execPublishAddress(self):  
      
      import re 
       
      userName = self.userName.text()
      password = self.passWord.text()             
      
      if not userName:       
       QMessageBox.warning(self, 'Login Error', \
        ' User Name is required', QMessageBox.Ok)
       return  
     
      elif not password:
       QMessageBox.warning(self, 'Login Error', \
        'Password is required', QMessageBox.Ok)
       return       
   
      elif not re.match(r"[^@]+@[^@]+\.[^@]+", userName):        
       QMessageBox.warning(self, 'Invalid Email Address', \
        ' Please enter a valid email address', QMessageBox.Ok)
       return      
   
      else:   
        restServiceInit = ProvRestServiceClient()
        
        QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
        success, accessToken, message = restServiceInit.authenticateUser(userName, password)
        QApplication.restoreOverrideCursor()
        
        if not success:
          QMessageBox.warning(self, 'Login Failed', \
          'The email or password you entered is incorrect', QMessageBox.Ok)
        else:          
          QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
          pmtaSuccessStatus, pmtaErrorMessage = restServiceInit.postPMTARecord(accessToken, userName, self.walletAddress)
          QApplication.restoreOverrideCursor()
          print pmtaSuccessStatus
          if not pmtaSuccessStatus:
           QMessageBox.information(self, 'Failed', \
           pmtaErrorMessage, QMessageBox.Ok)
          else:
           QMessageBox.information(self, 'Success', \
           'PMTA Record has been successfully created', QMessageBox.Ok)           
           super(DlgLogin, self).accept() 
