# BCPlatforms with Python for Azure Batch on CentOS
##### Last update 20/10/2016 - Partner using library below in their production code 

This prototype & libraries were delivered to BCPlatform partner in Finland. This partner wanted to understand how they could run their BCP Server on CentOS server to compute of millions of genomics calculations within HPC scenarios on Azure.

> Goal of the partner was to leverage their BCPlatforms Server in an Azure Batch Linux (CentOS 7) Cluster.

## Complete Workflow with Azure Batch 
  - batch_client.py : Whole workflow to drive creation of a Batch Pool, along with its nodes, copy local files to remote blob storage, to add task to the pool, execute them on the newly stored files, and to get the results back locally.
  - batch_task.py : task to be executed on the nodes from the pool (pulling data from a directory
  
## Pool update / Nodes Connection 
  - configuration.cfg : You need to define your Batch/Storage account configuration credentials (includes batch/storage service name & key but also batch service URL), those come from the Azure Portal
  - bcpscript.sh : script to run as a startup script on each new Node instance of the batch cluster
  - changePoolSettings.py : How to modify your Azure Batch pool (batch name for a cluster of nodes) with new configuration
  - changePoolSettings.cfg : Pool settings configuration
  - connectToNodes.py : This will generate all the user credentials so that you can login to the different nodes of your pool
  - connectToNodes.cfg : Nodes configuration
  - requirements.txt : Package requirements

## Tech resources
* [Azure Batch Doc] - Cloud-scale job scheduling and compute management
* [Python For Batch] - Get started with the Python SDK for Azure Batch
* [CentOS Doc] - CentOS Wiki

[Azure Batch Doc]: <https://azure.microsoft.com/en-us/documentation/services/batch/>
[Python For Batch]: <https://azure.microsoft.com/en-us/documentation/articles/batch-python-tutorial/>
[CentOS Doc]: <https://wiki.centos.org/Documentation>
