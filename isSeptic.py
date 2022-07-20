import requests
import json
import timeit

def sendReq(address):
	"""
	Calls parseAddress to appropriately format address as url params
	Additional address parameters may be added as needed to get correct result from API (e.g. state/country?)
	"""
	addressParts = parseAddress(address)
	reqUrl = "https://api.housecanary.com/v2/property/details?address=%s&zipcode=%s" % tuple(addressParts)
	r = requests.get(reqUrl, headers={'Accept': 'application/json'})
	"""
	Future - check response for error and take appropriate action. Log? Retry? etc. 
	response also includes "api_code" and "api_code_description" which are probably applicable
	If no error, continue:
	"""
	result = r.json()
	return result

def parseAddress(address):
	"""
	Helper function to parse whatever address input we have into pieces ready to give to the API
	Could accept object or string, needs to return a list of pieces
	e.g. ["123+Main+St", "12345"]
	For this demonstration, actual functionality is omitted since we are not actually accessing the API or receiving address input
	Just return dummy values
	"""
	return ["123+Main+St", "12345"]

def getIsSeptic(address=None, debug=False, sampleResponse=None):
	"""
	use debug if you do not have access to the API itself, and pass in a sample response filename in json format
	"""
	
	if debug:
		with open(sampleResponse) as f:
			res =  json.load(f)
	else:
		#API is not public
		#res = sendReq(address)
		pass

	return checkResponse(res)

def checkResponse(res):
	"""
	Update this function as-needed if changing third-party providers
	"""
	try:
		fieldVal = res.get('property/details').get('result').get('property').get('sewer')
	except:
		print("Error parsing API response")
	if fieldVal=="septic":
		return True
	return False


def main():
	start = timeit.default_timer()
	print("Begin program")
	
	sampleResponseMunicipalFile = "sampleResponseMunicipal.json"
	sampleResponseSepticFile = "sampleResponseSeptic.json"  
   
	#Tests
	print ("Test 1 of getIsSeptic, municipal input.")
	print ( getIsSeptic(debug=True, sampleResponse=sampleResponseMunicipalFile) )
	print ("Test 2 of getIsSeptic, septic input.")
	print ( getIsSeptic(debug=True, sampleResponse=sampleResponseSepticFile) )
	

	stop = timeit.default_timer()
	print("Finished in %s" % (stop-start))


if __name__ == '__main__':
    main()
