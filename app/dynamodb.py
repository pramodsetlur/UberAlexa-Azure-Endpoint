import boto3
from boto3.session import Session

# Get the service resource.
def add_access_code(user_id,access_code):
	session = Session(aws_access_key_id='AKIAIP7TPCBBGPWD3SZQ',
                  aws_secret_access_key='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',
                  region_name='us-west-2')
	dynamodb = session.resource('dynamodb')
	table = dynamodb.Table('user_access_code')
	data = {}
	data["user_id"] = user_id
	data["access_code"] = access_code
	table.put_item(Item=data)
