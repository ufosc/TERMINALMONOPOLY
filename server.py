import socket
import threading
import boto3
import os
import time

# AWS Configuration
AWS_REGION = 'us-east-1'
AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET']

# ECS Configuration
CLUSTER_NAME = os.environ['CLUSTER_NAME']
TASK_DEFINITION = os.environ['TASK_DEFINITION']
SUBNET_IDS = os.environ['SUBNET_IDS'].split(',')
SECURITY_GROUP_IDS = os.environ['SECURITY_GROUP_IDS'].split(',')

def handle_client(client_socket):
    # Initialize ECS client
    ecs_client = boto3.client('ecs', region_name=AWS_REGION, aws_access_key=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

    # Run ECS task
    response = ecs_client.run_task(
        cluster=CLUSTER_NAME,
        taskDefinition=TASK_DEFINITION,
        launchType='FARGATE',
        networkConfiguration={
            'awsvpcConfiguration': {
                'subnets': SUBNET_IDS,
                'securityGroups': SECURITY_GROUP_IDS,
                'assignPublicIp': 'ENABLED'
            }
        },
    )

    # Extract task ARN
    task_arn = response['tasks'][0]['taskArn']
    print(f"Task {task_arn} started.")

    # Wait for the task to be in RUNNING state
    task_running = False
    while not task_running:
        tasks = ecs_client.describe_tasks(cluster=CLUSTER_NAME, tasks=[task_arn])
        task = tasks['tasks'][0]
        last_status = task['lastStatus']
        if last_status == 'RUNNING':
            task_running = True
        else:
            time.sleep(1)

    # Retrieve the ENI ID attached to the task
    eni_id = None
    for attachment in task['attachments']:
        for detail in attachment['details']:
            if detail['name'] == 'networkInterfaceId':
                eni_id = detail['value']
                break

    # Get the public IP address from the ENI
    ec2_client = boto3.client('ec2', region_name=AWS_REGION)
    network_interface = ec2_client.describe_network_interfaces(NetworkInterfaceIds=[eni_id])
    public_ip = network_interface['NetworkInterfaces'][0]['Association']['PublicIp']
    print(f"Task is running at IP {public_ip}")

    # Send the IP address to the client
    client_socket.send(public_ip.encode())

    # Close the client socket
    client_socket.close()

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_host = '0.0.0.0'
    server_port = 3131
    server_socket.bind((server_host, server_port))
    server_socket.listen(5)
    print(f"Server listening on port {server_port}")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connection from {addr}")
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == '__main__':
    start_server()
