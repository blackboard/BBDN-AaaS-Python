# BBDN-AaaS-Python
This commandline application is meant to demonstrate the Ally as a Service API. It was built with Python 3, and so before you start, you must have Python 3 installed and available in your command line path. 

Once Python is installed, you will need to install a few dependencies:

```bash
pip install pyjwt requests
```

Once this is done, you will then need to configure the app.py file with your Ally client Id and your Ally secret. At this time, the best way to obtain this information is to engage your Account Executive to discuss pricing and request credentials.

Add these values to the appropriate place in the app.py file:
```python
"""
    This script is meant to show you how to interact with the Ally as a Service APIs. For more information
    about them or to learn how to request your credentials, visit https://docs.blackboard.com/ally
"""
clientId="yourClientId"
secret="yourSharedSecret"
hostname="https://prod.ally.ac"
basepath="/api/v2/clients/" + clientId + "/content"
url=hostname + basepath
```

You are now ready to go. You will need a file to upload available on the commandline. Now simply run `python app.py` and follow the prompts. 

You will first be prompted with `Enter a filename including the path, either absolute or relative to the current directory:`. Type in this information and press ENTER. At this time, the script will open the file and **POST** to the `/api/v2/clients/:clientId/content` endpoint. If this upload fails, the script will print an error and exit. If successful, the script will print the HTTP status code, the response headers and body, and the contentHash. The contentHash is the unique identifier for your file, and how you will refer to that file in subsequent API calls.

Next, the script will **GET** the `/api/v2/clients/:clientId/content/:contentHash/status` endpoint. This will return the status of processing on our file. This processing time will vary based on the complexity and the size of your file, and so the script will loop until the status returned equals 'success'. The loop uses a sleep(1) to pause between checks. If the call fails, we will print out the error code, body, and headers of the response and exit. If it succeeds, you will be prompted with `Get Full Report?`. Entering y and pressing ENTER will get you the full report. Anything else will only return the metadata. For more information on what this actually means, check out the [Retrieve the feedback for a file](https://docs.blackboard.com/ally/getfeedback.html) page in the [Developer docs](https://docs.blackboard.com/ally).

Whichever you choose, the script will then **GET** the `/api/v2/clients/:clientId/content/:contentHash` endpoint to request your data. If you selected the full report, the query parameter `?feedback=true` will be appended, otherwise `?feedback=false` will be appended. False is the default state, so in practice, you could simply omit this paramater if you only want the files metadata. On failure, we will print out the error, otherwise, we will print out the visibility indicator, which will either be low, medium, high, or perfect.

This is the end of the script! Congratulations, you just successfully checked your file for accessibility using the Ally as a Service API!

For more information on this API, visit our [Ally as a Service Developer Documentation](https://docs.blackboard.com/ally).
