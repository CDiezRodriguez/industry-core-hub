# Tractus-X Umbrella Minimal Deployment Guide

The Tractus-X Umbrella Chart serves as a comprehensive deployment solution for the Catena-X ecosystem components.

Using Umbrella v2.6.0 released chart

>[!note]
>As Industry Core Hub needs to connect to several Tractus-x components, this guide will ease the local deployment of these services for those who are not familiar with the required configuration of these components or don't know much about Kubernetes and Helm.


This guide helps you deploy a minimal version of the Tractus-X Umbrella chart focused on the following services:
- centralidp
- sharedidp
- portal
- ssi-dim-wallet-stub
- tx-data-provider (tractus-x connector)
- digital-twin-registry
- submodel server

For a deeper understanding, you can reference the full guides: https://github.com/eclipse-tractusx/tractus-x-umbrella/tree/main/docs/user

## Cluster Setup

### Prerequisites

1. A system with at least:
  - 4 CPU cores
  - 16GB RAM
  - 20GB storage

2. Required tools:
  - kubectl (Installation [kubernetes.io](https://kubernetes.io/docs/tasks/tools/#kubectl))
  - Helm v3.8+ (Installation [helm.sh](https://helm.sh/docs/intro/install/))
  - Minikube (Installation [minikube.sigs.k8s.io](https://minikube.sigs.k8s.io/docs/start/)) *only if you are going to use minikube*

### 1. Set Up Minikube (for local development)

>[!note]
> **[MacOS Only]** In case Docker Desktop isn't available, follow this guide: https://github.com/eclipse-tractusx/tractus-x-umbrella/tree/main/docs/user/setup#option-1-docker-desktop-available
>
> If you follow the guide above ignore all minikube related commands

#### Linux Set Up

Start Minikube with sufficient resources:

```bash
minikube start --cpus=4 --memory=8Gb
```

#### Windows Set Up

For windows the easy way is to enable Kubernetes in Docker Desktop:

1. Enable Kubernetes in Docker Desktop:
- Navigate to Settings > Kubernetes and enable the Kubernetes option.

2. Install an NGINX Ingress Controller:
```sh
helm upgrade --install ingress-nginx ingress-nginx --repo https://kubernetes.github.io/ingress-nginx --namespace ingress-nginx --create-namespace
```
Use 127.0.0.1 as the Cluster IP and manually configure ingress.

>[!important]
> If you follow the windows guide, ignore all minikube commands

>[!warning]
> The Windows setup isn't extensively tested, and you may encounter issues. We would appreciate any contributions from those who successfully deploy it on Windows.

#### Verifying the Cluster
After starting Minikube or Docker Desktop Kubernetes, verify the cluster setup:

- Check that your cluster is running:
```bash
kubectl cluster-info
```
- Open the Minikube dashboard to monitor resources:
```bash
minikube dashboard
```

### 2. Enable Ingress Controller and Kubernetes Dashboard (Minikube Only)

```bash
minikube addons enable ingress
minikube addons enable ingress-dns
minikube addons enable dashboard
```

### 3. Get Minikube IP

```bash
MINIKUBE_IP=$(minikube ip)
echo "Minikube IP: $MINIKUBE_IP"
```

### 4. Configure DNS

Add these entries to your `/etc/hosts` file (replace **192.168.49.2** with your Minikube IP, 192.168.49.2 is the default Minikube IP):

```bash
# Add to /etc/hosts
192.168.49.2 centralidp.tx.test
192.168.49.2 sharedidp.tx.test
192.168.49.2 portal.tx.test
192.168.49.2 portal-backend.tx.test
192.168.49.2 dataprovider.tx.test
192.168.49.2 dataprovider-controlplane.tx.test
192.168.49.2 dataprovider-dataplane.tx.test
192.168.49.2 dataprovider-dtr.tx.test
192.168.49.2 dataprovider-submodelserver.tx.test
192.168.49.2 ssi-dim-wallet-stub.tx.test
192.168.49.2 pgadmin4.tx.test
```

## Deployment

### 1. Custom Values File

The Helm chart configuration for Tractus-X Umbrella is complex and contains hundreds of values across multiple files. The [minimal-values.yaml](./minimal-values.yaml) file we're using only overrides specific values from the main `values.yaml` file in the Umbrella chart repository.

> **Important**: Only developers familiar with Helm charts and the Tractus-X architecture should modify the values beyond what's provided in this guide. Incorrect configurations can lead to non-functional deployments or security issues.

The base values can be found in the [umbrella chart's values.yaml file](https://github.com/eclipse-tractusx/tractus-x-umbrella/blob/umbrella-2.6.0/charts/umbrella/values.yaml). Our [minimal-values.yaml](./minimal-values.yaml) follows a similar structure as the `values-adopter-portal.yaml` file but focuses on only the essential services.

### 2. Install the Chart

Assuming you are in the root folder of the project, run these commands. If you're working from a different directory, adjust the path to the minimal-values.yaml file accordingly.

```bash
kubectl create namespace umbrella
helm repo add tractusx-dev https://eclipse-tractusx.github.io/charts/dev
helm repo update
helm install -f docs/umbrella/minimal-values.yaml umbrella tractusx-dev/umbrella --namespace umbrella --version v2.6.0
```

If you modify any value in the `minimal-values.yaml` you can upgrade the deployment running
```bash
helm upgrade -f docs/umbrella/minimal-values.yaml umbrella tractusx-dev/umbrella --namespace umbrella --version v2.6.0
```

>[!important]
>Once the installation or upgrade is succesfull run this patch
>```bash
>kubectl patch ingress umbrella-dataprovider-dtr \
>  --type='json' \
>  -p='[{"op": "replace", "path": "/spec/rules/0/http/paths/0/path", "value": "/"}]' \
>  -n umbrella
>```
>
> This patch modifies the Digital Twin Registry (DTR) ingress path to use a simple root path ("/") instead of the more complex URL pattern defined in the template. This patch is necessary due to not overridable configuration in the DTR chart. While the technical details involve how the ingress controller processes URL patterns, the important part is that this patch ensures the DTR API endpoints are properly accessible at the expected URL.

### 3. Check Deployment Status

```bash
kubectl get pods -n umbrella
```

Wait until all pods are in the Running state. This may take several minutes for the first deployment.

```bash
# You can watch the pod status
kubectl get pods -n umbrella -w
```

### 4. Check Service Access

Verify that the ingress resources are properly created:

```bash
kubectl get ingress -n umbrella
```

## Default Credentials

### CentralIDP (Keycloak)

- URL: http://centralidp.tx.test/auth/
- Username: `admin`
- Password: `adminconsolepwcentralidp`

### SharedIDP (Keycloak)

- URL: http://sharedidp.tx.test/auth/
- Username: `admin` 
- Password: `adminconsolepwsharedidp`

### Portal

- URL: http://portal.tx.test/
- Username: `cx-operator@tx.test`
- Password: `tractusx-umbr3lla!`

### PGAdmin4

- URL: http://pgadmin4.tx.test
- Username: `pgadmin4@txtest.org`
- Password: `tractusxpgadmin4`

#### Database Connection Details

For all connections:
- Username: `postgres`
- Port: `5432`

| Component         | Host                              |Password                   |
|-------------------|-----------------------------------|---------------------------|
| Portal            | `umbrella-portal-backend-postgresql` |`dbpasswordportal`         |
| CentralIdP        | `umbrella-centralidp-postgresql`    |`dbpasswordcentralidp`     |
| SharedIdP         | `umbrella-sharedidp-postgresql`    |`dbpasswordsharedidp`      |
| MIW               | `umbrella-miw-postgres`            |`dbpasswordmiw`            |
| Data Provider     | `umbrella-dataprovider-db`         |`dbpasswordtxdataprovider` |

#### Verifying Database Access

To verify access, follow these steps:

1. Open pgAdmin4.
2. Add a new server connection for the desired database.
3. Test the connection by browsing schemas and running queries.

## Interacting with Services

### 1. CentralIDP

The CentralIDP is a Keycloak instance that serves as the central identity provider:

1. Access the admin console at http://centralidp.tx.test/auth/admin/
2. Login with the admin credentials
3. You can manage clients, users, and realms for the Catena-X ecosystem

Key features:
- Client management for all Catena-X services
- User federation
- Role and permission management

### 2. SharedIDP

The SharedIDP is another Keycloak instance for company-specific identities:

1. Access the admin console at http://sharedidp.tx.test/auth/admin/
2. Login with the admin credentials
3. This IDP is used by applications like the portal and dataprovider

Key features:
- Manages company-specific user identities
- Federation with CentralIDP
- Used by Portal and other applications for user authentication

### 3. Portal

The Portal is the main entry point for Catena-X applications:

1. Access the portal at http://portal.tx.test/
2. Login with the cx-operator user
3. From here you can access registered apps and manage users

Key features:
- App Marketplace for Catena-X applications
- User and company management
- Service subscription and management

### 4. Dataprovider and Related Components

The Dataprovider deployment includes several integrated components that enable data exchange and digital twin functionality:

#### 4.1 Dataprovider EDC Connectors
- Data sharing and exchange functionality through Eclipse Dataspace Connector (EDC)
- API endpoints for data assets and contract negotiation
- Consists of both control plane and data plane components
- Control plane URL: http://dataprovider-controlplane.tx.test/
- Data plane URL: http://dataprovider-dataplane.tx.test/

#### 4.2 Digital Twin Registry
- Allows registration and discovery of digital twins
- Provides APIs for managing digital twin metadata
- Digital Twin Registry URL: http://dataprovider-dtr.tx.test/

#### 4.3 Submodel Server
- Hosts the actual data models and assets
- Provides standardized APIs for accessing submodel data
- Submodel server URL: http://dataprovider-submodelserver.tx.test/

These components work together to enable the complete data exchange and digital twin capabilities required for Catena-X use cases.

### 6. PGAdmin4

PGAdmin4 is a web-based administration tool for PostgreSQL databases:

1. Access the web UI at http://pgadmin4.tx.test
2. Login using the admin credentials
3. To connect to a database:
   - Right-click on "Servers" and select "Create" → "Server..."
   - Name: Give a descriptive name (e.g., "Portal DB")
   - Connection tab:
     - Host: Use the service name of the database (e.g., `umbrella-portal-backend-postgresql`)
     - Port: 5432
     - Maintenance database: postgres
     - Username: postgres
     - Password: Use the password defined in [#### Database Connection Details] (e.g., "dbpasswordportal")

## Postman Collections

We provide several Postman collections pre-configured with umbrella values in the `postman` folder.

- Digital Twin Registry: [ic-hub-aas-registry-v3.postman_collection.json](./postman/ic-hub-aas-registry-v3.postman_collection.json)

## Troubleshooting

### Common Issues

1. **Ingress not working**:
- Verify that your `/etc/hosts` file is correctly configured with the Minikube IP
- Check if the Minikube ingress addon is enabled: `minikube addons list`
- Ensure your Minikube IP is correct: `minikube ip`

2. **Pods not starting**:
```bash
kubectl describe pod <pod-name> -n umbrella
```

3. **Service connectivity issues**:
```bash
kubectl get ingress -n umbrella
```

4. **Resource constraints**:
If pods are stuck in Pending state, check if you have enough resources:
```bash
kubectl describe nodes
```

5. **Log inspection**:
```bash
kubectl logs <pod-name> -n umbrella
```

### Specific Service Issues

1. **CentralIDP/SharedIDP Keycloak Issues**:
```bash
kubectl logs -l app.kubernetes.io/name=centralidp -n umbrella
kubectl logs -l app.kubernetes.io/name=sharedidp -n umbrella
```

2. **Portal Issues**:
```bash
kubectl logs -l app.kubernetes.io/name=portal -n umbrella
```

3. **Dataprovider Issues**:
```bash
kubectl logs -l app.kubernetes.io/name=dataprovider-edc-controlplane -n umbrella
kubectl logs -l app.kubernetes.io/name=dataprovider-edc-dataplane -n umbrella
kubectl logs -l app.kubernetes.io/name=dataprovider-dtr -n umbrella
kubectl logs -l app.kubernetes.io/name=dataprovider-submodelserver -n umbrella
```

## Cleanup

To remove the deployment:

```bash
helm uninstall umbrella -n umbrella
kubectl delete namespace umbrella
```

To stop the cluster:
```bash
minikube stop
```

To restart the cluster:
```bash
minikube start
```

To delete the cluster:
```bash
minikube delete
```

## NOTICE

This work is licensed under the [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/legalcode).

* SPDX-License-Identifier: CC-BY-4.0
* SPDX-FileCopyrightText: 2025 Contributors to the Eclipse Foundation
* Source URL: <https://github.com/eclipse-tractusx/industry-core-hub>