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

def connectToNodes(batch_client, pool_id, usernameToGive, passwordToGive, expirationDays):
    # Create the user that will be added to each node
    # in the pool
    user = batchmodels.ComputeNodeUser(usernameToGive)
    user.password = passwordToGive
    user.is_admin = True
    user.expiry_time = (datetime.datetime.today() + datetime.timedelta(days=expirationDays)).isoformat()

    # Get the list of nodes in the pool
    nodes = batch_client.compute_node.list(pool_id)
    
    # Add the user to each node in the pool and print
    # the connection information for the node
    for node in nodes:
        # Add the user to the node
        batch_client.compute_node.add_user(pool_id, node.id, user)

        # Obtain SSH login information for the node
        login = batch_client.compute_node.get_remote_login_settings(pool_id,
                                                                node.id)
        # Print the connection info for the node
        print("{0} | {1} | {2} | {3} | {4} | {5}".format(node.id,
                                                node.state,
                                                login.remote_login_ip_address,
                                                login.remote_login_port,
                                                usernameToGive,
                                                passwordToGive))

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

    #coming from the script specified config
    pool_id = script_config.get(
        'DEFAULT',
        'pool_id')
    username = script_config.get(
        'DEFAULT',
        'username')
    password = script_config.get( #getpass.getpass()
        'DEFAULT',
        'password')
    expirationTime = script_config.getint(
        'DEFAULT',
        'expirationTime')

    # Print the settings we are running with
    common.helpers.print_configuration(global_config)
    common.helpers.print_configuration(script_config)

    credentials = batchauth.SharedKeyCredentials(
        batch_account_name,
        batch_account_key)

    batch_client = batch.BatchServiceClient(
        credentials,
        base_url=batch_service_url)

    try:
        connectToNodes(batch_client, pool_id, username, password, expirationTime)
    except Exception as e:
        print('error/exception: '+ e)

if __name__ == '__main__':
    global_config = configparser.ConfigParser()
    global_config.read(common.helpers._SAMPLES_CONFIG_FILE_NAME)

    sample_config = configparser.ConfigParser()
    sample_config.read(os.path.splitext(os.path.basename(__file__))[0] + '.cfg')

    execute_script(global_config, sample_config)