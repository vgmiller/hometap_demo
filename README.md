Project setup:
You will need a python3 environment, django, djangorestframework:
sudo apt install python3-venv
python3 -m venv ./venv
source venv/bin/activate
sudo apt install python3-django
pip3 install djangorestframework

Place project folder in same directory as venv, cd project directory, and then run locally with:
python3 manage.py runserver

The main entry should now be on your local:
http://127.0.0.1:8000/

This will give a true/false response that tells the consuming entity whether or not we think the given house is on septic. However, since the given API is not publicly accessible, this main entry root path is expected to fail.

For testing/demonstration, I've included two sample responses (pulled from the HouseCanary documentation) inside json files in the project's static folder, and you can trigger calls to these using the following:

http://127.0.0.1:8000/?debug=True&sampleResponse=sampleResponseMunicipal.json
this should return false 
http://127.0.0.1:8000/?debug=True&sampleResponse=sampleResponseSeptic.json
this should return true

############################################
If for whatever reason the django project is not working, a minified version of this logic can be found in the base directory in the file isSeptic.py, which can be run on the command line and will execute the test cases.
############################################


Some thoughts:

If this is part of a bigger API, then we wouldn't be using the main entry point, but some helpfully-named entrypoint agreed upon by both ends

sendReq, parseAddress, and checkResponse are all dependent on the 3rd party vendor - what their call is, what format they're expecting input data in, and what their response looks like - so all would need to be modified to fit a different vendor in the event of a change.

General thought - We might want a broader-use API endpoint, one that isn't just returning true/false isSeptic, but one that just returns the value of that field (e.g. municipal/septic/storm/etc) and lets the caller decide what to do with it. This decision would depend on how important it is to the home classification that there's a distinction between [septic vs everything else] as opposed to the distinctions between all the various sewer types.

For parseAddress:
This needs more work, but would entirely depend on what the incoming data looked like in real life.
The incoming address data - are they uniform structure?, what to do with missing values e.g. an address with a province instead of a state, or multi-line street address?
Could also handle address parsing before hitting this api, and pass it in IN parts, depending on code/db structure

