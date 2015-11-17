"""
Definition of views.
"""
from django.http import HttpResponse
from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
import requests
import dynamodb
from rauth import OAuth2Service

def home(request):


	# Once your user has signed in using the previous step you should redirect
	# them here

	parameters = {
	    'redirect_uri': 'https://uberalexa.azurewebsites.net',
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

	table_name = "user_access_code"
	userId = request.GET.get('user_id')
	dynamodb.add_access_code(table_name, userId, access_token)
	
	return render(request, 'app/base.html', {'final_data':data})


def loginUrl(request):
	uber_api = OAuth2Service(
		client_id='9x5d54-oGBfVr-3zC4wAnYyY9783iF9k',
		client_secret='-iREizzW6dqHtqdCZFIjbWTQYxTwiEUdKQxV7Hta',
		name='Findango',
		authorize_url='https://login.uber.com/oauth/authorize',
		access_token_url='https://login.uber.com/oauth/token',
		base_url='https://api.uber.com/v1/',
	)

	parameters = {
	'response_type': 'code',
	'redirect_uri': 'https://uberalexa.azurewebsites.net' + "?user_id=" + request.GET.get('user_id') + "&source_lat=" + request.GET.get('source_lat') + "&source_lon=" + request.GET.get('source_lon') + "&dest_lat=" + request.GET.get('dest_lat') + "&dest_lon=" + request.GET.get('dest_lon') + "&product_id=" + request.GET.get('product_id'),
	'scope': 'profile history history_lite request request_receipt',
	}

	# Redirect user here to authorize your application
	login_url = uber_api.get_authorize_url(**parameters)
	return HttpResponse(login_url)

def test(request):
	return HttpResponse("Hello World!");

def privacy_policy(request):
	return HttpResponse("Your access code will be used to book a ride for you. This information is kept confidential and isn't shared with any other party")

def insertDb(request):
	userId = request.GET.get('user_id')
	location = request.GET.get('lat') + "_" + request.GET.get('lon')
	table_name = "user_location"
	dynamodb.add_access_code(table_name, userId, location)
	return HttpResponse(userId + " - " + location)
