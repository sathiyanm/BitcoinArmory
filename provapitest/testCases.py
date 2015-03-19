#!/usr/bin/python
import ProvRestServiceClient
from ProvRestServiceClient import ProvRestServiceClient
import PMTAUtil
from PMTAUtil import PMTAUtil
import unittest
import pytest
import sys
import re
#===============================================================================
# Test Case for Provisioning Rest API 
#===============================================================================
class RestClientTestCases(unittest.TestCase, PMTAUtil, ProvRestServiceClient):
    """Tests for Rest API`."""

    global userCreationStatusCode                 
    global userAuthenticationStatus
    global wrongUserStatusCode
    global grantAccessStatus
    
    if len(sys.argv) < 2:
     print "userMgmt.py <email> <password>"
     exit()
        
    testUser1 = {
     'email':  'testuser1@test.com',
     'password':'123456',
     'username':'testuser1',
     'firstName':'Test',
     'lastName':'User',
     'api_access_token':'testToken'
    }
            
    newUser = ProvRestServiceClient() 
    #create user records
    testUser1['email'] = sys.argv[1]
    username = sys.argv[1].split('@')[0]    
    testUser1['password'] = sys.argv[2]  
    testUser1['username'] = username
    
    userCreationStatusCode   = newUser.createUser(testUser1) 
    
    print userCreationStatusCode #201
        
    userAuthenticationStatus, accessToken, message = newUser.authenticateUser(testUser1['email'], testUser1['password'])
    
    print userAuthenticationStatus # True
    
    wrongUserStatusCode, accessToken, message = newUser.authenticateUser("johndoe@example.com", "12123123")
    
    print wrongUserStatusCode #False
    
    grantAccessStatus = newUser.grantAccess(testUser1['email'], username, accessToken)
    
    print grantAccessStatus # 201        
        
    #===========================================================================
    # Test Functions
    #===========================================================================    
         
    def test_PTMA_record(self):
          
        """testing a new PMTA Record format for sha22 format"""  
        self.assertEqual( PMTAUtil().convertEmailToPMTAFormat('testuser1@test.com'), "43f7292759ee1498c856d2ac9a4bf021c1876c5cbcf62c5983d49af3._pmta.test.com")   
    
       
    def test_Create_New_User(self):  
        """create a user record """       
        self.assertEqual(userCreationStatusCode, 201)        
                   
       
    def test_Authenticate_User(self):
        """testing user authentication"""        
#        self.assertTrue(restServiceInit.authenticateUser(userName, password), "success")
        self.assertFalse(userAuthenticationStatus, True)
           
   
    def test_Authenticate_Not_Valid_User(self):
        """testing user authentication invalid user Name"""
        self.assertFalse(wrongUserStatusCode, False)
           
       
    def test_Grant_Access_To_User(self):
        """Granting access to the user"""
        self.assertFalse(grantAccessStatus, 201)
  
     
# if __name__ == '__main__':
#     unittest.main()
    
suite = unittest.TestLoader().loadTestsFromTestCase(RestClientTestCases)
unittest.TextTestRunner(verbosity=2).run(suite)
