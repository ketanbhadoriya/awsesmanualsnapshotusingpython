# awsesmanualsnapshot
Download the python script from this repository to use python interactive tool for manual snapshot in AWS Elasticsearch.

### Please note few points about the same python script:

1. It will help in taking the manual snapshot of AWS Elasticsearch cluster and restoring it into another AWS Elasticsearch cluster, if chose to do so (Cross Region is not supported - Both AWS Elasticsearch clusters need to be in the same region).

2. The manual snapshot will be taken of the whole cluster. Indices level snapshot is not supported by the given python script.

3. While restoring the snapshot taken, please note that it will delete all the old indices (including .kibana* indices) of the AWS Elastcisearch destination cluster where you are restoring the data using manual snapshot.

4. This script best suited in follwing scenarios:

    - If you want to enable encryption at rest option on an existing AWS Elasticsearch cluster, you will have to first create a new AWS Elasticsearch cluster with same configuration of already existing AWS Elasticsearch cluster and enabling 'Encryption at Rest' option too while creating this new AWS Elasticsearch cluster. 
    - Once the new AWS Elasticsearch cluster is created with required configuration, you can proceed taking manual snapshot of already existing AWS Elasticsearch cluster and restoring data using this manual snapshot into newly created AWS Elasticsearch cluster.
  
    - Lastly, for some reason if you want to duplicate the data of already existing AWS ES cluster into into a new AWS ES cluster in the same region, you can achieve that using given python script.
  

### Prerequites to run this python script

1. An AWS EC2 Linux Instance 

2. An IAM user who will run the given python script on an AWS EC2 Linux instance. This IAM user needs to have an 'Adminstrator access' or a role attached with following aws managed policies:

    - IAMFullAccess 
    - AmazonESFullAccess
    - AmazonS3FullAccess 
    - AmazonEC2FullAccess 
  
3. SSH into the same EC2 instance and configure AWS CLI using credentials of above IAM user (Please refer to configure AWS CLI: https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html)

4. One new AWS ES domain with same configuration as of the old AWS ES domain (and if needed then enable 'Encryption at rest' option) of which you will take the manual snapshot using given python script.

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
    
***Image Reference:*** https://github.com/miztiik/AWS-Demos/tree/master/How-To/setup-manual-elasticsearch-snapshots
