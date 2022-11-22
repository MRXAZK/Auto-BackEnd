from fastapi import APIRouter, Response, status
from resources import boto
import os
import boto3

resources = boto

app = APIRouter()

@app.get("/ec2/create", description="Create EC2 Instance", tags=["AWS"])
async def create(response: Response):
    resources.create_instances(
        ImageId='ami-0af2f764c580cc1f9', 
        MinCount=1, 
        MaxCount=1
        )
    response = {
        "message" : f"Success create ec2 instance"
    }
    return response

@app.get("/ec2/delete", description="Delete EC2 Instance", tags=["AWS"])
async def delete_ec2_instance(response: Response):
    resources.instances.filter(InstanceIds=['i-0a4d3a006e281b33b']).terminate()
    response = {
        "message" : f"Success delete ec2 instance"
    }
    return response
    

@app.get("/ec2/stop", description="Stop EC2 Instance", tags=["AWS"])
async def stop_ec2_instance(response: Response):
    resources.instances.filter(InstanceIds=['i-0a4d3a006e281b33b']).stop()
    response = {
        "message" : f"Success stop ec2 instance"
    }
    return response

@app.get("/ec2/start", description="Start EC2 Instance", tags=["AWS"])
async def start_ec2_instance(response: Response):
    resources.instances.filter(InstanceIds=['i-0a4d3a006e281b33b']).start()
    response = {
        "message" : f"Success start ec2 instance"
    }
    return response

@app.get("/ec2/reboot", description="Reboot EC2 Instance", tags=["AWS"])
async def reboot_ec2_instance(response: Response):
    resources.instances.filter(InstanceIds=['i-0a4d3a006e281b33b']).reboot()
    response = {
        "message" : f"Success reboot ec2 instance"
    }
    return response

@app.get("/ec2/terminate", description="Terminate EC2 Instance", tags=["AWS"])
async def terminate_ec2_instance(response: Response):
    resources.instances.filter(InstanceIds=['i-0a4d3a006e281b33b']).terminate()
    response = {
        "message" : f"Success terminate ec2 instance"
    }
    return response

@app.get("/ec2/attach", description="Attach EC2 Instance", tags=["AWS"])
async def attach_ec2_instance(response: Response):
    resources.instances.filter(InstanceIds=['i-0a4d3a006e281b33b']).attach_volume(VolumeId='vol-0a0a7c2d2d1a8b8a0')
    response = {
        "message" : f"Success attach ec2 instance"
    }
    return response

@app.get("/ec2/detach", description="Detach EC2 Instance", tags=["AWS"])
async def detach_ec2_instance(response: Response):
    resources.instances.filter(InstanceIds=['i-0a4d3a006e281b33b']).detach_volume(VolumeId='vol-0a0a7c2d2d1a8b8a0')
    response = {
        "message" : f"Success detach ec2 instance"
    }
    return response

