# TwitterAnalyticsUsingAWS
This is an application for analysing Real Time Twitter data. It has following steps:

 Requirements: 
 
 Requires a stream running in Kinesis.
 Use aws configure on your machine and set up the aws key and secret token.
 Requires MySQL instance in AWS RDS
 Tableau
 
 There are two main parts to it:
 
1) Kinesis Producer:
Kinesis Producer produces twitter streams and puts in on kinesis steam

Run: python twitter_streaming.py

2) Kinesis Consumer:
Kinesis Consumer consumes kinesis streams and puts it on AWS RDS MYSQL

Run: python kinesis.py
This code will create a table in MySQL and start generating data within it.

To visualize it, we need to use MYSQL connection in Tableau and visualize it using column parameters.
Example visualisation has been done on:
https://public.tableau.com/profile/aakash.wadhwani#!/vizhome/TwitterStreaming/Sheet1

Note: You need AWS credentials for Kinesis, RDS, EC2 and Tableau
Producer and Consumer could be run without the EC2 instance, we preferred to run it on EC2 instances to move everthing on cloud.

 
