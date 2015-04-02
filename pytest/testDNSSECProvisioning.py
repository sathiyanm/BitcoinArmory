#!/usr/bin/python
import unittest
import sys
import re
import json

sys.path.append('..')
from dnssec_dane.ProvRestServiceClient import PMTAUtil
from dnssec_dane.ProvRestServiceClient import ProvRestServiceClient

class UserMgmt():
    
    def __init__(self):
       self.apiPath= ProvRestServiceClient().ConfigSectionMap("settings")['apipath']

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
       data_json = json.dumps(newUserRecord)
       response = manager.urlopen('POST', self.createUserPath, headers={'Content-Type':'application/json'}, body=data_json)
       return response.status

    def grantAccess(self, email, userName, accessToken):

     import urllib3   
     from urllib3 import PoolManager        
     manager = PoolManager(1)

     self.userAuthUrl = self.apiPath + "azn/EXPERIMENTAL/65337/" +str(PMTAUtil().convertEmailToPMTAFormat(email)) +"/"+ str(userName) + "?access_token=" + str(accessToken) 
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

#===============================================================================
# Test Case for Provisioning Rest API 
#===============================================================================
################################################################################
class RestClientTestCases(unittest.TestCase):
    """Tests for Rest API`."""
        
    if len(sys.argv) < 2:
     print "userMgmt.py <email> <password>"
     exit()
     
    def createUser1(self):    
        testUser1 = {
         'email':  'testuser1@test.com',
         'password':'123456',
         'username':'testuser1',
         'firstName':'Test',
         'lastName':'User',
         'api_access_token':'testToken'
        }
        
        testUser1['email'] = sys.argv[1]
        username = sys.argv[1].split('@')[0]    
        testUser1['password'] = sys.argv[2]  
        testUser1['username'] = username

        return testUser1
         
    def test_PTMA_record(self):
          
        """testing a new PMTA Record format for sha22 format"""  
        self.assertEqual( PMTAUtil().convertEmailToPMTAFormat('testuser1@test.com'), "43f7292759ee1498c856d2ac9a4bf021c1876c5cbcf62c5983d49af3._pmta.test.com")   
    
       
    def test_Create_New_User(self):  
        """create a user record """
        userMgmt = UserMgmt()       
        userCreationStatusCode   = userMgmt.createUser(self.createUser1()) 
        self.assertEqual(userCreationStatusCode, 201)        
                   
       
    def test_Authenticate_User(self):
        
        """testing user authentication"""        
        userMgmt = UserMgmt() 
        authUser = ProvRestServiceClient() 
        testUser1 = self.createUser1()  
        validUserAuthenticationStatus, accessToken, message = authUser.authenticateUser(testUser1['email'], testUser1['password'])
        self.assertTrue(validUserAuthenticationStatus)
           
   
    def test_Authenticate_Not_Valid_User(self):
        
        """testing user authentication invalid user Name"""
        authUser = ProvRestServiceClient() 
        wrongUserStatusCode, accessToken, message = authUser.authenticateUser("johndoe@example.com", "12123123")
        self.assertFalse(wrongUserStatusCode)
           
       
    def test_Grant_Access_To_User(self):
        
        """Granting access to the user"""
        testUser1 = self.createUser1()
        userMgmt = UserMgmt() 
        authUser = ProvRestServiceClient() 
        validUserAuthenticationStatus, accessToken, message = authUser.authenticateUser(testUser1['email'], testUser1['password'])
        grantAccessStatus = userMgmt.grantAccess(testUser1['email'], testUser1['username'], accessToken)    
        self.assertFalse(grantAccessStatus, 201)
     
    
suite = unittest.TestLoader().loadTestsFromTestCase(RestClientTestCases)
unittest.TextTestRunner(verbosity=2).run(suite)
