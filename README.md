This project was delivered to BCPlatform partner in Finland. This partner wanted to prototype how to run their BCP Server on CentOS server to compute 100's of thousands of genomics calculations in HPC scenarios.

Goal of the partner was to leverage their software in an Azure Batch Linux.
What you will find in this sample code (produced for the partner) is the following:

Sample code #1 
batch_client.py : Whole workflow to drive creation of a Batch Pool, along with its nodes, copy local files to remote blob storage, to add task to the pool, execute them on the newly stored files, and to get the results back locally.
batch_task.py : task to be executed on the nodes from the pool (pulling data from a directory

Sample code #2 
configuration.cfg : You need to define your Batch/Storage account configuration credentials
bcpscript.sh : script to run as a startup script on each new Node instance of the batch cluster
changePoolSettings.py : How to modify your Azure Batch pool (batch name for a cluster of nodes) with new configuration
changePoolSettings.cfg : Pool settings configuration
connectToNodes.py : This will generate all the user credentials so that you can login to the different nodes of your pool
connectToNodes.cfg : Nodes configuration
requirements.txt : Package requirements
