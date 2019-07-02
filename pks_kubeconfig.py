#!/usr/local/bin/python
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import requests
import json

cluster="CLUSTER"
username="USERNAME"
password="PASSWORD"
# if you want to read the password from file, uncomment and edit these lines:
#with open(".password", "r") as fd:
#    password=fd.readline().rstrip()
pks_host="PKS_HOST"

pks_api="https://{}:9021".format(pks_host)
uaa_api="https://{}:8443".format(pks_host)

# Get token to retrieve the kubeconfig
data = {
        'response_type': 'token',
        'client_id': 'pks_cli',
        'client_secret': '',
        'grant_type': 'password',
        'username': username,
        'password': password
        }
r = requests.post("{}/oauth/token".format(uaa_api), data, verify=False)
access_token = r.json()['access_token']

# Get the kubeconfig skeleton
data = {}
headers = {
        'Authorization': 'Bearer {}'.format(access_token),
        'Content-Type': 'application/json'
        }

r = requests.post("{}/v1/clusters/{}/binds".format(pks_api, cluster), headers=headers, verify=False)

kubeconfig = r.json()

# Get the token for kubeconfig auth
data = {
        'response_type': 'token',
        'client_id': 'pks_cluster_client',
        'client_secret': '',
        'grant_type': 'password',
        'username': username,
        'password': password
        }

r = requests.post("{}/oauth/token".format(uaa_api), data, verify=False)
id_token = r.json()['id_token']
refresh_token = r.json()['refresh_token']

# Combine the kubeconfig and the keys
kubeconfig['users'][0]['user']['auth-provider']['config']['id-token'] = id_token
kubeconfig['users'][0]['user']['auth-provider']['config']['refresh-token'] = refresh_token

# Print the kubeconfig to stdout
print json.dumps(kubeconfig)
