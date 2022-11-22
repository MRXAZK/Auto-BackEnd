import boto3
import os
from dotenv import load_dotenv

load_dotenv()

boto = boto3.resource('ec2', region_name=os.environ.get('region_name'), aws_access_key_id=os.environ.get('aws_access_key_id'), aws_secret_access_key=os.environ.get('aws_secret_access_key'))