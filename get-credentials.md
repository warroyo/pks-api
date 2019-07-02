# getting a kubeconfig via API

## using OIDC as a provider 
1. get an access token from UAA

```bash
curl 'https://api.pks.$DOMAIN:8443/oauth/token' -k -i -X POST \
    -H 'Content-Type: application/x-www-form-urlencoded' \
    -H 'Accept: application/json' \
    -d 'response_type=token&client_id=pks_cli&client_secret=&grant_type=password&username=admin&password=<secret-here>'
```

2. take the access token above and get the kubeconfig from the PKS API

```bash
curl 'https://api.pks.$DOMAIN:9021/v1/clusters/pas/binds' -k -s -X POST \
    -H 'Accept: application/json' \
    -H 'Content-Type: application/json' \
    -H 'Authorization: Bearer <token>' > config.json
```

3. get the acess token needed for the cluster from UAA

```bash
curl 'https://api.pks.$DOMAIN:8443/oauth/token' -k -s -X POST \
    -H 'Content-Type: application/x-www-form-urlencoded' \
    -H 'Accept: application/json' \
    -d 'response_type=token&client_id=pks_cluster_client&client_secret=&grant_type=password&username=admin&password=<secret-here>' > token.json
```

4. set the credentials in the kubeconfig

```bash
kubectl config set-credentials admin --auth-provider-arg=id-token=$(cat token.json | jq -r .id_token) --kubeconfig=./config.json

kubectl config set-credentials admin --auth-provider-arg=refresh-token=$(cat token.json | jq -r .refresh_token) --kubeconfig=./config.json
```

5. test it

```bash
kubectl get nodes --kubeconfig=./config.json
```