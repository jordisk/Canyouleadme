from flask import Flask, request, redirect
import os
import twilio.twiml
from googlemaps import GoogleMaps
import urllib, json, yaml

 
app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])

def hello_monkey():
	def chooseSymbol(line):
		if 'head' in line:
			return "head"
		elif 'roundabout' in line:
			return 'roundabout' 
		elif 'right' in line:
			return "right"
		elif 'left' in line:
			return "left"
		elif 'merge' in line:
			return "merge"
		else:
			return 'none'

	body_message = str(request.values.get('Body', None))
	latitude = body_message.split('_')[0]
	longitude = body_message.split('_')[1]
	destination = body_message.split('_')[2]
	mapService = GoogleMaps()
	directions = mapService.directions('RG7 5ND', 'RG7 5NN')
	message = ""
	#for step in directions['Directions']['Routes'][0]['Steps']:
	#	message = message + step['descriptionHtml']
	mapsUrl = 'https://maps.googleapis.com/maps/api/directions/json?origin=' + str(latitude) + ',' + str(longitude) + '&destination=' + str(destination) + '&mode=walking'
	response = urllib.urlopen(mapsUrl)

	data = yaml.load(response.read())
	leg = data.get('routes')[0].get('legs')[0]
	general_data = leg.get('distance').get('text') + '_' + leg.get('duration').get('text')
	stepMessage = ""
	stepsArray = leg.get('steps')
	for step in stepsArray:
		line = step.get('html_instructions')
		stepMessage =  stepMessage + line + '_' + step.get('distance').get('text') + '_' + chooseSymbol(line) + '/n'

	#message = str(directions)[0:100]
	#message = "Latitude: " + str(latitude) + " Longitude: " + str(longitude) + " Destination: " + str(destination)
	message = str(stepMessage)
	resp = twilio.twiml.Response()
	resp.message(message)
	return str(resp)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)



