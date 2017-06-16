#usr/bin/python

import sys
import json
import boto3

def getInstance(instanceID):
	'''
	gets a specified instance from the cloud
	'''
	
	response = client.describe_instances(
    	 InstanceIds=[
        	str(instanceID),
    	],
    		DryRun = False
    	  	)
	print(response['Reservations'][0]['Instances'])


def stopInstances(instanceList):
	'''
	Takes in an array of AWS instances and stops them
	'''
	print("stopping specified instances")
	results = []

	for i in instanceList:
		response = client.stop_instances(
    			InstanceIds=[
        			i,
    			],
    				DryRun = True
			)	
		results.append("Status of instance: " + str(i) +": " + str(response["StoppingInstances"][0]["CurrentState"]["Name"]))  
	print("The resulting Statuses: " + str(results))	

def startInstances(instanceList):
	'''
	Takes in an array of AWS instances and starts them
	'''
	print("starting specified instances")
	results = []
	
	for i in instanceList:
		response = client.start_instances(
			InstanceIds=[
				i,
			],
				DryRun = True
			)
		results.append("Status of the instance: " + str(i) + ": " + str(response["StartingInstances"][0]["CurrentState"]["Name"]))
 
	print("The resulting Statuses: " + str(results))



#####BODY#####

print("Please make sure that your instance IDs are space delimited")
print("EX: python <scriptName.py> 'Start/Stop' instance1 instance2 instance3")
with open('credentials.json') as data_file:
	data = json.load(data_file)



####Authentication to AWS####
ACCESS_KEY = data["ACCESS_KEY"]
SECRET_KEY = data["SECRET_KEY"]
client = boto3.client(
    'ec2',
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY,
)
print("successfully connected to AWS ec2 instance")


#####Check to see what the operation is#####
if str(sys.argv[1].lower()) != "stop" and str(sys.argv[1].lower()) != "start":
	print(sys.argv[1])
	print("Must specify a start or stop operation")
	exit()
else:
	print("Beginning to " + str(sys.argv[1]) + " instances")


#####Build the list of instances#####
instances = []
i = 2
while(len(sys.argv) > i):
	instances.append(str(sys.argv[i]))
	i += 1
print(instances)


#####Function Calls#####
if str(sys.argv[1].lower()) == "stop":
	stopInstances(instances)
else:
	startInstances(instances)

