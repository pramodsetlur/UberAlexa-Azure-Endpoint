import boto3
from boto3.session import Session

# Get the service resource.
def add_access_code(table_name, user_id, value):
	session = Session(aws_access_key_id='AKIAIJS5T3EGZ7VUVZGA',
                  aws_secret_access_key='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',
                  region_name='us-east-1')
	dynamodb = session.resource('dynamodb')
	table = dynamodb.Table(table_name)
	data = {}
	data["user_id"] = user_id
	
	if table_name == "user_access_code":
		discriminator = "access_code"
	else:
		discriminator = "location"

	data[discriminator] = value
	table.put_item(Item=data)
