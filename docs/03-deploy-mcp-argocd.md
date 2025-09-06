# Deploy MCP Server on ArgoCD

This chapter covers how to set up the [Akuity's ArgoCD MCP server](https://github.com/akuity/argocd-mcp) for GitOps-based MCP deployments. This is of Model Context Protocol (MCP) server for Argo CD, enabling AI assistants to interact with your Argo CD applications through natural language. This server allows for seamless integration with Visual Studio Code and other MCP clients through stdio and HTTP stream transport protocols.



## Step 1: Building and pushing the Container Image

First, build the MCP Server image and push it to your container registry. This step creates a containerized version of the argocd-mcp that can be deployed to Kubernetes.

```bash
# Build and tag the image with version v0.0.49
./dockerfile-argocd-mcp/build.sh 0.3.0 latest quay.io/alopezme
```

> **Note:** The build script will prompt you to push the image to the registry.


## Step 2: Deploying the MCP Server

Deploy the MCP server to your Kubernetes cluster using the Helm chart. This will create all necessary resources including the deployment, service, ane the env variables for the MCP server.


First, get the ArgoCD base URL and API token:

```bash
ARGOCD_BASE_URL=$(oc get route argocd-server -n openshift-gitops --template='https://{{ .spec.host }}')

ARGOCD_ADMIN_USERNAME=admin

ARGOCD_ADMIN_PASSWORD=$(oc get secret argocd-cluster -n openshift-gitops --template='{{index .data "admin.password"}}' | base64 -d)

ARGOCD_API_TOKEN=$(curl -k -s $ARGOCD_BASE_URL/api/v1/session \
  -H 'Content-Type:application/json' \
  -d '{"username":"'"$ARGOCD_ADMIN_USERNAME"'","password":"'"$ARGOCD_ADMIN_PASSWORD"'"}' | sed -n 's/.*"token":"\([^"]*\)".*/\1/p')

# Test if the params are working directly to the ArgoCD API
curl -sk $ARGOCD_BASE_URL/api/v1/applications -H "Authorization: Bearer $ARGOCD_API_TOKEN" | jq '.items[].metadata.name' 

echo "Print variables:"
echo "ARGOCD_BASE_URL: $ARGOCD_BASE_URL"
echo "ARGOCD_ADMIN_USERNAME: $ARGOCD_ADMIN_USERNAME"
echo "ARGOCD_ADMIN_PASSWORD: ${ARGOCD_ADMIN_PASSWORD:0:10}..."
echo "ARGOCD_API_TOKEN: ${ARGOCD_API_TOKEN:0:10}..."

# You can test the MCP server locally with the following command:
npm exec argocd-mcp@latest sse
```


Second, as soon as it works locally, you can deploy it to your Kubernetes cluster using the Helm chart.

```bash
helm template mcp-server-chart --values mcp-server-chart/values-argocd.yaml \
  --set env[0].name=ARGOCD_BASE_URL --set env[0].value="$ARGOCD_BASE_URL" \
  --set env[1].name=ARGOCD_API_TOKEN --set env[1].value="$ARGOCD_API_TOKEN" \
  | oc apply -f -
```


If you want to test the MCP server, you can follow the same steps as in the [OpenShift MCP server](02-deploy-mcp-openshift.md) chapter.