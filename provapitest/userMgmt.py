#!/usr/bin/python
import ProvRestServiceClient
from ProvRestServiceClient import ProvRestServiceClient
import PMTAUtil
from PMTAUtil import PMTAUtil
import sys
import unittest
import pytest

testUser1 = {
	'email':  'testuser1@test.com',
    'password':'123456',
    'username':'testuser1',
    'firstName':'Test',
    'lastName':'User',
    'api_access_token':'testToken'
}

if len(sys.argv) < 2:
	print "userMgmt.py <email> <password>"
	exit()

newUser = ProvRestServiceClient()	
#create user records
testUser1['email'] = sys.argv[1]
username = sys.argv[1].split('@')[0]
testUser1['password'] = sys.argv[2]
testUser1['username'] = username

success = newUser.createUser(testUser1)
print success 

success, authToken, error = newUser.authenticateUser(sys.argv[1], sys.argv[2])
print authToken

response = newUser.grantAccess(testUser1['email'], username, authToken)    



# class RestClientTestCases(unittest.TestCase, PMTAUtil, ProvRestServiceClient):
    # """Tests for Rest API`."""
    
    # newUser = ProvRestServiceClient()

    # create user records
    # testUser1['email'] = sys.argv[1]
    # username = sys.argv[1].split('@')[0]
    # testUser1['password'] = sys.argv[2]
    # testUser1['username'] = username

    # success = newUser.createUser(testUser1)
    # print success 
    
    
    # success, authToken, error = newUser.authenticateUser(sys.argv[1], sys.argv[2])
    # print authToken
    # response = newUser.grantAccess(testUser1['email'], username, authToken)        

    # print response        



    # def test_PTMA_record(self):
        # """testing a new PMTA Record format for sha22 format"""  
        # self.assertEqual( PMTAUtil().convertEmailToPMTAFormat('testuser1@test.com'), "43f7292759ee1498c856d2ac9a4bf021c1876c5cbcf62c5983d49af3._pmta.test.com")
        
    # def create_new_user(self):
        # """testing a new a user ceation""" 
        # self.assertEqual(success, 201)
    
    # def authenticate_user(self):
        # """testing user authentication valid user""" 
        # self.assertTrue(response, 200)

    # def authenticate_wrong_user(self):
        # """testing user authentication failed"""
        # self.assertFalse(true)
    
    # def authenticate_wrong_user(self):
        # """testing a new a user ceation"""
        # self.assertFalse(true)


# if __name__ == '__main__':
    # unittest.main()

# suite = unittest.TestLoader().loadTestsFromTestCase(RestClientTestCases)
# unittest.TextTestRunner(verbosity=2).run(suite)