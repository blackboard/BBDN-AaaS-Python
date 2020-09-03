'''
Copyright (C) 2020, Blackboard Inc.
All rights reserved.
Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
Neither the name of Blackboard Inc. nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.
THIS SOFTWARE IS PROVIDED BY BLACKBOARD INC ``AS IS'' AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL BLACKBOARD INC. BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

Created on September 3, 2020

@author: shurrey
'''

import json
import requests
import time
import jwt
import datetime
import ssl
import sys

"""
    This script is meant to show you how to interact with the Ally as a Service APIs. For more information
    about them or to learn how to request your credentials, visit https://docs.blackboard.com/ally
"""
clientId="yourClientId"
secret="yourSharedSecret"
hostname="https://prod.ally.ac"
basepath="/api/v2/clients/" + clientId + "/content"
url=hostname + basepath
    
"""
    getHeaders() creates the JWT assertion required for authorization and then uses it to generate
    the Authorization header
"""
def getHeaders():
    
    # Generate the iat, basically the current number of seconds since the epoch
    iat = str(int(datetime.datetime.now().timestamp()))
    print("iat: " + iat)
    
    # create the JWT headers necessary for building your token
    headers = {
        'typ' : 'JWT',
        'alg': "RS256"     
    }
    print(str(headers))
    
    # Describe your claims. For Ally as a Service, you only need clientId and iat
    claims = {
        "clientId" : clientId ,
        "iat" : iat
    }
    print(str(claims))
    
    # Generate your jwt and then transform into a string using utf-8 encoding
    assertion = jwt.encode(claims, secret).decode("utf-8") 
    print(str(assertion))
    
    # create your auth header to be passed in each API call
    auth = {
        'Authorization' : 'Bearer ' + str(assertion)
    }
    print(str(auth))
    
    return auth


"""
    First step is to upload a file. Using Python requests, we set the files form parameter to the binary file data by opening it.
    We also call getHeaders to generate our JWT and compose our Authorization header with the bearer token
"""
# Ask the user for the path to a file
filename = input("Enter a filename including the path, either absolute or relative to the current directory: ")

# Create a dictionary called files. This will be the multi-part post parameter 'file' with the value being the binary file data
files = {'file': open(filename,'rb')}

# Post to the upload a file endpoint, set files equal to our files dict, and get the auth header
r = requests.post(url, files=files, headers=getHeaders())

# If successful, get the json body of the response, pull out the contentHash, and print out all of our values
if r.status_code == 200:
    res = json.loads(r.text)
    contentHash = res['hash']
    print("File Upload: " + str(r.status_code)) 
    print("response -> headers " + str(r.headers))
    print("body " + str(res))
    print("contentHash: " + contentHash)
# If not successful, print out the body of our response and exit
else:
    res = r.text
    print("Error in File Upload: " + str(r.status_code) + ": response -> headers {" + str(r.headers) + "} body {" + str(res) + "}")
    sys.exit()

# Append the contentHash to the base url
url += '/' + contentHash
print("url: " + url)


"""
    The next step is the check the progress of file processing by Ally. Depending on the size and complexity of the file, this make take a bit.
    Because of this, we are entering into a loop in order to keep checking until the status equals success. If it doesn't, then we sleep for 1
    second and try again. If you are using this script with large or complex files, you might want to adjust the time.sleep(1) to a larger number.
"""
while True:
    # Call the status endpoint and set the authorization header
    r = requests.get(url + '/status', headers=getHeaders())
    
    # If successful, get the JSON body, extract the status, and print out our values
    if r.status_code == 200:
        res = json.loads(r.text)
        status = res['status']
        print("GET Status: " + str(r.status_code)) 
        print("response -> headers " + str(r.headers))
        print("body " + str(res))
        print("status: " + status)
        # If the status is "success" exit the loop
        if(status == "success"):
            break
        #  If the status is not success, sleep for 1 second and try again
        else:
            time.sleep(1)
    # If the call fails, print out the error and exit
    else:
        res = r.text
        print("Error in Get Status: " + str(r.status_code) + ": response -> headers {" + str(r.headers) + "} body {" + str(res) + "}")
        sys.exit()

"""
    We have now successfully uploaded and processed our file through Ally as a Service. Now we want to get the feedback from Ally.
"""
# Ask the user if they want the full report. If y, set the query parameter 'feedback' to true, otherwise false
if(input("Get Full Report? ") == "y"):
    params = {
        'feedback' : 'true'
    }
else:
    params = {
        'feedback' : 'false'
    }

# Call the status endpoint, attach our query parameters, and set our authorization header
r = requests.get(url, headers=getHeaders(), params=params) 

# If successful, grab the JSON body, extract the visibility level (low, medium, high, or perfect) and display the data
if r.status_code == 200:
    res = json.loads(r.text)
    visibility = res['feedback']['visibility']
    print("Get Feedback: " + str(r.status_code)) 
    print("response -> headers " + str(r.headers))
    print("body " + str(res))
    print("visibility: " + visibility)
# If not successful, print out the error
else:
    res = r.text
    print("Error in Get Feedback: " + str(r.status_code) + ": response -> headers {" + str(r.headers) + "} body {" + str(res) + "}")

# Done!