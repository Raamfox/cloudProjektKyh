import os

import boto3
from boto3.dynamodb.conditions import Attr


def get_resource():
    return boto3.resource('dynamodb',
                          aws_access_key_id=os.environ['AWS_KEY'],
                          aws_secret_access_key=os.environ['AWS_SECRET_KEY'],
                          region_name='eu-north-1')


def get_all_readings():
    client = get_resource()
    table = client.Table('temp_reading')
    response = table.scan()
    return response['Items']

def get_item_by_id(item_id):
    client = get_resource()
    table = client.Table('temp_reading')
    response = table.get_item(Key={'id': item_id})
    return response['Item']


def get_item_by_attribute(attribute, value):
    client = get_resource()
    table = client.Table('temp_reading')
    response = table.scan(FilterExpression=Attr(attribute).eq(value))
    return response['Items']


def get_item_by_attribute_gt(attribute, value):
    client = get_resource()
    table = client.Table('temp_reading')
    response = table.scan(FilterExpression=Attr(attribute).gt(value))
    return response['Items']