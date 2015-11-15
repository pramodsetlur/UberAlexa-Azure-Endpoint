"""
Definition of views.
"""

from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime

def home(request):


	# Once your user has signed in using the previous step you should redirect
	# them here

	parameters = {
	    'redirect_uri': 'https://alexauber.azurewebsites.net',
	    'code': request.GET.get('code'),
	    'grant_type': 'authorization_code',
	}

	response = requests.post(
	    'https://login.uber.com/oauth/token',
	    auth=(
		'9x5d54-oGBfVr-3zC4wAnYyY9783iF9k',
		'-iREizzW6dqHtqdCZFIjbWTQYxTwiEUdKQxV7Hta',
	    ),
	    data=parameters,
	)

	# This access_token is what we'll use to make requests in the following
	# steps
	access_token = response.json().get('access_token')
	

	"""
	# Fetch details of user
	url = 'https://api.uber.com/v1/me'
	response = requests.get(
	    url,
	    headers={
		'Authorization': 'Bearer %s' % access_token
	    }
	)
	data = response.json()
	"""

	# Request ride
	url = 'https://api.uber.com/v1/requests'
	response = requests.post(
	    url,
	    headers={
		'Authorization': 'Bearer %s' % access_token,
	    	'Content-Type': 'application/json'
	    },
	    json={
		"start_latitude": request.GET.get('source_lat'),
		"start_longitude": request.GET.get('source_lon'),
		"end_latitude": request.GET.get('dest_lat'),
		"end_longitude": request.GET.get('dest_lon'),
		"product_id": request.GET.get('product_id')
		}
	)
	data = response.json()

	userId = request.GET.get('user_id')
	dynamodb.add_access_code(userId,access_token)
	
	return render(request, 'check/status.html', {'final_data':data})
