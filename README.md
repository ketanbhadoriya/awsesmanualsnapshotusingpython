## awsesmanualsnapshot
Download the python script from this repository to use python interactive tool for manual snapshot in AWS Elasticsearch.

# Please note few points about the same python script:

1. It will help in taking the manual snapshot of AWS Elasticsearch cluster and restoring it into another AWS Elasticsearch cluster if chose to do so (Cross Region is not supported - Both AWS Elasticsearch clusters need to be in the same region).

2. The manual snapshot will be taken of the whole cluster. Indices level snapshot is not supported.

3. While restoring the snapshot taken, please note that it will delete all the old indices (including .kibana* indices) of the AWS Elastcisearch cluster where you are restoring the data using manual snapshot.

4. This script best suited in follwing scenarios:

  . If you want to enable encryption at rest option on an existing AWS Elasticsearch cluster, you will have to first create a new AWS Elasticsearch cluster with same configuration of already existing AWS Elasticsearch cluster and enabling 'Encryption at Rest' option too while creating the new AWS Elasticsearch cluster. 
  . Once the new AWS Elasticsearch cluster is created with required configuration, you can proceed taking manual snapshot of already existing AWS Elasticsearch cluster and restoring data using this manual snapshot into newly created AWS Elasticsearch cluster.
  
  . Lastly, for some reason if you want to duplicate the data of 

3. The IAM user who will run the given python script on an AWS EC2 Linux instance needs to have an 'Adminstrator access' or a role attached with following aws managed policies:

  . IAMFullAccess 
  . AmazonESFullAccess
  . AmazonS3FullAccess 
  . AmazonEC2FullAccess 
  
4. 
