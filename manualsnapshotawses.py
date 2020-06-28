# imported required python libraries
import sys
import boto3
import time
import json
import requests
from requests_aws4auth import AWS4Auth

client = boto3.client('iam')  # boto client

# manual_snapshot_registort_code_inputs
es_host = raw_input("Enter the endpoint of ES domain of which you want to take the manual snapshot: ")  # AWS ES domain endpoint
es_region = raw_input("Enter the region of ES domain of which you want to take the manual snapshot: ")  # region of AWS ES domain
region = es_region
name_of_snapshot_repo = raw_input("Enter a name for manual snapshot repository: ")  # snaphot repository name
flag = 0

# defining variable for global reference later in the local function
account_id = ""
s3bucket_name = ""
snapshot_rolename = ""

# Signing Requests
service = 'es'
credentials = boto3.Session().get_credentials()
awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)
headers = {"Content-Type": "application/json"}


# Manual Snapshot of whole cluster function:
def snapshot_of_whole_cluster():
    global flag
    name_of_the_snapshot = raw_input(
        "Enter name of the manual snapshot to be taken (Manual snapshot of whole cluster): ")  # snapshot_name
    r2 = requests.put(es_host + '/_snapshot/' + name_of_snapshot_repo + '/' + name_of_the_snapshot, auth=awsauth,
                      headers=headers)
    print("Manual Snapshot Creation Processing...")
    time.sleep(10)
    print(r2.text)
    if r2.text == "{\"accepted\":true}":
        print(name_of_the_snapshot + ": manual snapshot successfully taken!")
        restore_choice = raw_input(
            "Do you want to restore the snapshot taken into another ES cluster? Press 'Y' to continue and 'N' to terminate the program:")
        if (restore_choice == 'Y' or restore_choice == 'y') and flag == 0:
            restore_es_host = raw_input(
                "Enter the host endpoint of ES domain where you want to restore the snapshot taken: ")
            print("Creating the same snapshot repository named - " + name_of_snapshot_repo + "- for above ES domain")
            time.sleep(6)
            creating_snap_repo_for_restoreES(restore_es_host)
            print("Restoring in Process...")
            time.sleep(5)
            delete_response = requests.delete(restore_es_host + '/_all')
            print(delete_response)
            restore_response = requests.post(
                restore_es_host + '/_snapshot/' + name_of_snapshot_repo + '/' + name_of_the_snapshot + '/_restore',
                auth=awsauth,
                headers=headers)
            print(restore_response.text)
            if restore_response.text == "{\"accepted\":true}":
                print("Snapshot successfully restored into ES domain: " + restore_es_host)
            else:
                print(restore_response.text)
                print("Restoring failed due to some error")
        elif (restore_choice == 'Y' or restore_choice == 'y') and flag == 1:
            print("Success!")
            restore_es_host = raw_input(
                "Enter the host endpoint of ES domain where you want to restore the snapshot taken: ")
            # Checking if snapshot repository entered already exists for above domain
            s1 = requests.get(restore_es_host + '/_snapshot', auth=awsauth, headers=headers)
            if name_of_snapshot_repo in s1.text:
                print("Restoring in Process...")
                time.sleep(5)
                delete_response = requests.delete(restore_es_host + '/_all')
                print(delete_response)
                restore_response = requests.post(
                    restore_es_host + '/_snapshot/' + name_of_snapshot_repo + '/' + name_of_the_snapshot + '/_restore',
                    auth=awsauth,
                    headers=headers)
                print(restore_response.text)
                if restore_response.text == "{\"accepted\":true}":
                    print("Snapshot successfully restored into ES domain: " + restore_es_host)
                else:
                    print(restore_response.text)
                    print("Restoring failed due to some error")
            else:
                flag = 2
                print("Creating the same snapshot repository named - " + name_of_snapshot_repo + " -for above ES domain")
                time.sleep(6)
                creating_snap_repo_for_restoreES(restore_es_host)
                print("Restoring in Process...")
                time.sleep(5)
                delete_response = requests.delete(restore_es_host + '/_all')
                print(delete_response)
                restore_response = requests.post(
                    restore_es_host + '/_snapshot/' + name_of_snapshot_repo + '/' + name_of_the_snapshot + '/_restore',
                    auth=awsauth,
                    headers=headers)
                print(restore_response.text)
                if restore_response.text == "{\"accepted\":true}":
                    print("Snapshot successfully restored into ES domain: " + restore_es_host)
                else:
                    print(restore_response.text)
                    print("Restoring failed due to some error")
        else:
            print("Terminating Program!")
            sys.exit()
    else:
        print("Failure occurred during manual snapshot")


def creating_snapshot_repo():
    global account_id
    global s3bucket_name
    global snapshot_rolename

    account_id = raw_input("Enter your AWS Account ID: ")  # IAM user account ID
    iam_role = raw_input("Enter your IAM role name (which you have attached your EC2 instance; just name, not full ARN): ")  # IAM Role
    policyformanualsnapshottoiamuser = raw_input(
        "Enter a name for the policy that you would like to add to given IAM role for manual snapshot: ")  # policy_for_manual_snapshot_to_iamrole
    es_domain_arn = raw_input("Enter ES domain ARN of which you are going to take manual snapshot:")  # AWS ES domain ARN
    s3bucket_name = raw_input("Enter your S3 bucket name where you want to register the snapshot repository: ")  # S3 Bucket Input
    snapshot_rolename = raw_input("Enter a name for snapshot role that you would like to create: ")  # Rolname needs to be created for snapshot

    # Creation of trust relationship policy for given snapshot role
    assume_role_policy_document = json.dumps({
        "Version": "2012-10-17",
        "Statement": [{
            "Sid": "",
            "Effect": "Allow",
            "Principal": {
                "Service": "es.amazonaws.com"
            },
            "Action": "sts:AssumeRole"
        }]
    })

    # Given snapshot role created and above trust policy attached
    response1 = client.create_role(
        RoleName=snapshot_rolename,
        AssumeRolePolicyDocument=assume_role_policy_document
    )

    # sleep
    print("Repository registration processing...")
    time.sleep(15)
    print("33% Completed!")

    # creation of given 's3 bucket' policy
    s3bucket_policy_document = json.dumps({
        "Version": "2012-10-17",
        "Statement": [{
            "Action": [
                "s3:ListBucket"
            ],
            "Effect": "Allow",
            "Resource": [
                "arn:aws:s3:::" + s3bucket_name
            ]
        },
            {
                "Action": [
                    "s3:GetObject",
                    "s3:PutObject",
                    "s3:DeleteObject"
                ],
                "Effect": "Allow",
                "Resource": [
                    "arn:aws:s3:::" + s3bucket_name + "/*"
                ]
            }
        ]
    })

    time.sleep(5)

    # attaching above policy to the given snapshot role
    response2 = client.put_role_policy(
        RoleName=snapshot_rolename,
        PolicyName='testdellatest',
        PolicyDocument=s3bucket_policy_document)

    # sleep
    time.sleep(15)
    print("66% Completed!")

    # Creation of policy that needs to be attached to IAM user by passing given snapshot role
    iampolicy_document_manual_snapshot = json.dumps({
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": "iam:PassRole",
                "Resource": "arn:aws:iam::" + str(account_id) + ":role/" + snapshot_rolename
            },
            {
                "Effect": "Allow",
                "Action": "es:ESHttpPut",
                "Resource": es_domain_arn + "/*"
            }
        ]
    })

    # sleep
    time.sleep(3)

    # Above Policy has been attached to given IAM user
    response3 = client.put_role_policy(
        RoleName=iam_role,
        PolicyName=policyformanualsnapshottoiamuser,
        PolicyDocument=iampolicy_document_manual_snapshot)

    time.sleep(25)
    print("100% Completed!")

    ###################
    # Python Module to register manual snapshot registory (Avaialble in AWS Manual Snapshpot registory document)

    host = es_host

    # Register repository
    path = '/_snapshot/' + name_of_snapshot_repo
    url = host + path

    payload = {
        "type": "s3",
        "settings": {
            "bucket": s3bucket_name,
            "region": es_region,
            "role_arn": "arn:aws:iam::" + str(account_id) + ":role/" + snapshot_rolename

        }
    }

    r = requests.put(url, auth=awsauth, json=payload, headers=headers)

    # Validating Snapshot repository creation result

    if r.status_code == 200:
        print(name_of_snapshot_repo + " - snapshot repository has been registered successfully!")

        # Checking if there are any snapshots in process
        r1 = requests.get(es_host + '/_snapshot/_status', auth=awsauth, headers=headers)

        if r1.text == "{\"snapshots\":[]}":
            snapshot_of_whole_cluster()
        else:
            print(
                "May be due to ongoing snapshots running program got terminated. The" + name_of_snapshot_repo + " snapshot repository has been created succefully. Hence, run the script once again after some time to take the manual snapshot.")
            sys.exit()  # terminating program
    else:
        print("Failure occurred in snapshot repository registration")


def creating_snap_repo_for_restoreES(host):
    global flag
    global account_id
    global s3bucket_name
    global snapshot_rolename

    # Register repository
    path = '/_snapshot/' + name_of_snapshot_repo
    url = host + path

    if flag == 2:
        p = requests.get(es_host + '/_snapshot/' + name_of_snapshot_repo, auth=awsauth, headers=headers)
        dict_data = json.loads(str(p.text))
        s3bucket_name = dict_data[name_of_snapshot_repo]["settings"]["bucket"]
        role_arn = dict_data[name_of_snapshot_repo]["settings"]["role_arn"]
        snapshot_rolename=role_arn.split("/")[1]
        account_id=(role_arn.split("::")[1]).split(":")[0]
        print("Processing...")
    else:
        print("Processing...")

    payload = {
        "type": "s3",
        "settings": {
            "bucket": s3bucket_name,
            "region": es_region,
            "role_arn": "arn:aws:iam::" + str(account_id) + ":role/" + snapshot_rolename

        }
    }

    r = requests.put(url, auth=awsauth, json=payload, headers=headers)
    if r.status_code == 200:
        print(
            name_of_snapshot_repo + " -snapshot repository has been registered successfully for ES domain where you want to restore the manual snapshot taken!")
    else:
        print("Failure occurred in snapshot repository creation for domain where you want to restore snapshot created!")


# Checking if snapshot repository entered already exists
s = requests.get(es_host + '/_snapshot', auth=awsauth, headers=headers)
if name_of_snapshot_repo in s.text:
    user_choice = raw_input(
        "Entered snapshot repository already exists. Please type \'Y\' to continue taking manual snapshot OR type \'N\' to terminate program:")
    if user_choice == 'Y' or user_choice == 'y':
        flag = 1
        snapshot_of_whole_cluster()
    else:
        print("Terminating Program...")
        sys.exit()
else:
    print("Please enter further inputs asked below, for the registering snapshot repository-")
    creating_snapshot_repo()
# EOF
