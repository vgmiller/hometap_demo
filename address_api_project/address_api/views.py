from django.shortcuts import render
import requests
import json
from django.http import JsonResponse

####
# Main Entry
####
def getIsSeptic(request):
    """
    Use debug if you do not have actually access to the API itself, and pass in a sample response filename in json format
    """
    address=request.GET.get('address', None)
    debug=request.GET.get('debug', None)
    sampleResponse=request.GET.get('sampleResponse', None)
    
    if debug:
        result, msg = doTestRunInstead(sampleResponse)
        responseCode = None
    else:
        #API is not public, so this will fail
        result, responseCode = sendReq(address)
        msg = "API is not actually public, so this is expected to fail: %s. Try with debug=True instead" % responseCode

    answer = checkResponse(result)
    return JsonResponse([answer, msg], safe=False)


####
# Helpers
####
def sendReq(address):
    """
    Calls parseAddress to appropriately format address as url params
    Additional address parameters may be added as needed to get correct result from API (e.g. state/country?)
    """
    addressParts = parseAddress(address)
    responseCode = None

    reqUrl = "https://api.housecanary.com/v2/property/details?address=%s&zipcode=%s" % tuple(addressParts)
    r = requests.get(reqUrl, headers={'Accept': 'application/json'})
    if r.status_code!=200:
        responseCode = r.status_code
    """
    Future - when we actually expect this to work(i.e. we've autheticated with the 3rd party)
    check response for error and take appropriate action. Log? Retry? etc. 
    HouseCanary's ok response also includes "api_code" and "api_code_description" which may also require attention
    """
    result = r.json()
    return result, responseCode

def parseAddress(address):
    """
    Helper function to parse whatever address input we have into pieces ready to give to the API
    Could accept object or string, needs to return a list of pieces
    e.g. ["123+Main+St", "12345"]
    For this demonstration, actual functionality is omitted since we are not actually accessing the API or receiving address input
    Just return dummy values
    """
    return ["123+Main+St", "12345"]

def checkResponse(res):
    """
    Update this function as-needed if changing third-party providers
    """
    fieldVal=None
    try:
        fieldVal = res.get('property/details').get('result').get('property').get('sewer')
    except:
        print("Error parsing API response")
    if fieldVal=="septic":
        return True
    return False

def doTestRunInstead(sampleResponse):
    result = None
    msg = "Using debug mode"
    if not sampleResponse:
        msg+=", missing sampleResponse parameter, please check README"
    else:
        import os
        from django.conf import settings
        try:
            fullpath = os.path.join( settings.STATIC_ROOT, sampleResponse )
            with open(fullpath) as f:
                result =  json.load(f)
        except:
            msg+=", possibly mangled sampleResponse parameter"
    return result, msg
