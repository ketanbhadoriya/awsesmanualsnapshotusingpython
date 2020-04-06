# awsesmanualsnapshot

- A Python Interactive tool for manual snapshot in AWS Elasticsearch.

![alt text](https://raw.githubusercontent.com/ksingh7575/awsesmanualsnapshotusingpython/master/AWSESManualSnapshot.png)

                  The given Python Tool will automate all the steps mentioned in the above flow image

### Please note few points about the same python script:

1. It will help in taking the manual snapshot of AWS Elasticsearch cluster and restoring it into another AWS Elasticsearch cluster, if chose to do so (Cross Region is not supported - Both AWS Elasticsearch clusters need to be in the same region).

2. The manual snapshot will be taken of the whole cluster. Indices level snapshot is not supported by the given python script.

3. While restoring the snapshot taken, please note that it will delete all the old indices (including .kibana* indices) of the AWS Elastcisearch destination cluster where you are restoring the data using manual snapshot.

4. This script best suited in follwing scenarios:

    - If you want to enable encryption at rest option on an existing AWS Elasticsearch cluster, you will have to first create a new AWS Elasticsearch cluster with same configuration of already existing AWS Elasticsearch cluster and enabling 'Encryption at Rest' option too while creating this new AWS Elasticsearch cluster. 
    - Once the new AWS Elasticsearch cluster is created with required configuration, you can proceed taking manual snapshot of already existing AWS Elasticsearch cluster and restoring data using this manual snapshot into newly created AWS Elasticsearch cluster.
  
    - Lastly, for some reason if you want to duplicate the data of already existing AWS ES cluster into into a new AWS ES cluster in the same region, you can achieve that using given python script.

### VIMP NOTE: Before going to prerequisites, please check the following:

If you have enabled fine grained access for your Amazon Elasticsearch cluster, then please go through the  following steps before jumping to prerequisites section; if fine grained has not been enabled then you can ignore the below steps and directly proceed with prerequisites section:

	i. If you have Set IAM ARN as master user then -> Select your AWS ES domain and choose action ----> Modify master user -> And in the "IAM ARN" field paste IAM user ARN (which you are using to register the snapshot repository) -> After this proceed with the prerequisites 

												OR

	ii. If you have created a master user (i.e. you have master user name and master password) then -> Login to the Kibana console -> Follow below steps -> After this proceed with the prerequisites: 

		1. After logging in, on the left side menu, choose "security" (lock icon). 
		2. In the next window choose the role mappings.
		3. Click the "+" icon next to the search field.
		4. In the next window, from the role drop down choose "manage_snapshots" role.
		5. In the users section add the IAM user ARN (which you are using to register the snapshot repository) "arn:aws:iam::<put_account_id_here>:user/<put_IAM_user_name_here>" and click submit.


### Prerequites to run this python script

1. An AWS EC2 Linux Instance 

2. An IAM user who will run the given python script on an AWS EC2 Linux instance. This IAM user needs to have an 'Adminstrator access' or a role attached with following aws managed policies:

    - IAMFullAccess 
    - AmazonESFullAccess
    - AmazonS3FullAccess 
    - AmazonEC2FullAccess 
  
3. SSH into the same EC2 instance and configure AWS CLI using credentials of above IAM user (Please refer to configure AWS CLI: https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html)

4. One new AWS ES domain with same configuration as of the old AWS ES domain (and if needed then enable 'Encryption at rest' option) of which you will take the manual snapshot using given python script.

5. One S3 bucket to register manual snapshot repository.

6. After all this created, please make note of:

    - Endpoint of ES domain of which you want to take the manual snapshot
    - Region of ES domain of which you want to take the manual snapshot
    - Your AWS Account ID
    - Your IAM User Name
    - ES domain ARN of which you are going to take manual snapshot
    - Name of S3 bucket created earlier (Just the name, not full ARN)
    - Endpoint of ES domain if you wish to restore the manual snapshot taken. 
  
7. **Note**: If for some reason you want to restore the manual snapshot later, please make note of snapshot respository that you will be creating while running this script.

### Steps to follow to run the given Python script:

1. Make sure you have all the prerequistes mentioned above.

2. SSH into the EC2 instance

3. Run following commands one by one:

    - $ sudo yum -y install python-pip

    - $ sudo pip install boto3

    - $ sudo pip install requests-aws4auth

4. After this, download the python file attached on the EC2 instance using followinng command:

    - $ wget https://raw.githubusercontent.com/ksingh7575/awsesmanualsnapshotusingpython/master/manualsnapshotawses.py
  
5. Once the python file downloaded successfully to the EC2 instance, run following command:

    - $ chmod 700 manualsnapshotawses.py
  
6. Lastly, go ahead and run the script using:

    - $ python manualsnapshotawses.py
    
Once you will run the tool you will be asked to put different inputs which you should have make note of as given in Prerequites.

**Below is the screengrab of the same python tool after you finish running it! (Note: The account ID has been kept hidden for security reasons)**

![alt text](https://raw.githubusercontent.com/ksingh7575/awsesmanualsnapshotusingpython/master/ScreeGrabofPythonTool.png)

*Thanks for viewing, I hope that you found this tool helpful!*
