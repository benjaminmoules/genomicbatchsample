from __future__ import print_function
try:
    import configparser
except ImportError:
    import ConfigParser as configparser
import datetime
import os

import azure.storage.blob as azureblob #need to import azure-batch & azure-storage library first

import azure.batch.batch_service_client as batch
import azure.batch.batch_auth as batchauth
import azure.batch.models as batchmodels

import common.helpers


def changePoolSettings(pool_id,vm_size,distro, version, pool_node_count,resource_files,batch_service_client): 
    task_commands = [
            # Copy the python_tutorial_task.py script to the "shared" directory
            # that all tasks that run on the node have access to.
            'cp -r $AZ_BATCH_TASK_WORKING_DIR/* $AZ_BATCH_NODE_SHARED_DIR',
            '$AZ_BATCH_NODE_SHARED_DIR/bcpscript.sh',
            # Install pip and then the azure-storage module so that the task
            # script can access Azure Blob storage
            'apt-get update',
            'apt-get -f install python-pip',
            'pip install azure-storage']

    # Get the virtual machine configuration for the desired distro and version.
    # For more information about the virtual machine configuration, see:
    # https://azure.microsoft.com/documentation/articles/batch-linux-nodes/
    vm_config = common.helpers.get_vm_config_for_distro(batch_service_client, distro, version)

    pool = batch.models.PoolAddParameter(
        id=pool_id,
        virtual_machine_configuration=vm_config,
        vm_size=vm_size,
        target_dedicated=pool_node_count,
        start_task=batch.models.StartTask(
            command_line=common.helpers.wrap_commands_in_shell('linux', task_commands),
            run_elevated=True,
            wait_for_success=True,
            resource_files=resource_files),
        )
    common.helpers.create_pool_if_not_exist(batch_service_client, pool)

def execute_script(global_config, script_config):
    """Executes the sample with the specified configurations.

    :param global_config: The global configuration to use.
    :type global_config: `configparser.ConfigParser`
    :param script_config: The script specific configuration to use.
    :type script_config: `configparser.ConfigParser`
    """
    # Set up the configuration
    batch_account_key = global_config.get('Batch', 'batchaccountkey')
    batch_account_name = global_config.get('Batch', 'batchaccountname')
    batch_service_url = global_config.get('Batch', 'batchserviceurl')
    storage_account_key = global_config.get('Storage', 'storageaccountkey')
    storage_account_name = global_config.get('Storage', 'storageaccountname')

    #coming from the script specified config
    pool_id = script_config.get(
        'DEFAULT',
        'pool_id')
    pool_node_count = script_config.getint(
        'DEFAULT',
        'pool_node_count')
    vm_size = script_config.get(
        'DEFAULT',
        'vm_size')
    distro = script_config.get(
        'DEFAULT',
        'distribution')
    version = script_config.get(
        'DEFAULT',
        'version')

    # Print the settings we are running with
    common.helpers.print_configuration(global_config)
    common.helpers.print_configuration(script_config)

    credentials = batchauth.SharedKeyCredentials(
        batch_account_name,
        batch_account_key)

    batch_client = batch.BatchServiceClient(
        credentials,
        base_url=batch_service_url)
    
    blob_client = azureblob.BlockBlobService(
        account_name=storage_account_name,
        account_key=storage_account_key)
    
    #uploading script to Pool/Node/Blob Container
    bcplatform_container_name = 'bcp'
    application_file_paths = [os.path.realpath('bcpscript.sh')]
    blob_client.create_container(bcplatform_container_name, fail_on_exist=False)
    resource_files = [common.helpers.upload_file_to_container(blob_client, bcplatform_container_name, file_path) for file_path in application_file_paths]

    try:
        changePoolSettings(pool_id, vm_size, distro, version, pool_node_count, resource_files, batch_client)
    except Exception as e:
        print('error/exception: '+ e)

if __name__ == '__main__':
    global_config = configparser.ConfigParser()
    global_config.read(common.helpers._SAMPLES_CONFIG_FILE_NAME)

    sample_config = configparser.ConfigParser()
    sample_config.read(os.path.splitext(os.path.basename(__file__))[0] + '.cfg')

    execute_script(global_config, sample_config)
