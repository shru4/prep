# prep DevOps Mock — Order Service

End-to-end Azure DevOps exercise:

GitHub -> Azure DevOps Pipeline -> Terraform -> AKS/ACR/PostgreSQL/Key Vault/Service Bus -> Kubernetes deployment

## Prerequisites

- Azure subscription
- Azure DevOps project
- GitHub repository
- Azure CLI
- Terraform >= 1.6
- kubectl
- Docker for local testing

## Important before `terraform apply`

Supply the PostgreSQL password securely. For local practice:

```bash
export TF_VAR_postgres_password='Use-A-Strong-Password-Here'
```

Do not commit `terraform.tfvars` with real secrets.

## Local Terraform

```bash
cd terraform
terraform fmt -recursive
terraform init
terraform validate
terraform plan
terraform apply
```

## Azure DevOps service connections

Create:

1. `azure-prep-connection` — Azure Resource Manager, preferably workload identity federation.
2. `acr-prep-connection` — ACR/Docker Registry connection for image push.

The pipeline assumes the Terraform state backend already exists:

- resource group: `terraform-rg`
- storage account: `terraformstateaccount`
- container: `tfstate`
- key: `prep.tfstate`

For an interview, explain that state storage is normally bootstrapped separately.

## Pipeline variables to change

Edit these values in `azure-pipelines.yml` for your environment:

- `azureServiceConnection`
- `acrServiceConnection`
- `aksResourceGroup`
- `aksClusterName`
- `acrLoginServer`

## Application

The app provides:

- `GET /health`
- `GET /ready`
- `GET /orders`
- `POST /orders`

Example:

```bash
curl http://<EXTERNAL-IP>/health
curl http://<EXTERNAL-IP>/orders
curl -X POST http://<EXTERNAL-IP>/orders \
  -H 'Content-Type: application/json' \
  -d '{"name":"Laptop"}'
```

## Security model

- Azure DevOps -> Azure: workload identity federation/service connection
- AKS -> ACR: `AcrPull` on AKS kubelet identity
- AKS workload -> Key Vault: user-assigned managed identity + workload identity + `Key Vault Secrets User`
- AKS workload -> Service Bus: user-assigned managed identity + `Azure Service Bus Data Sender`
- PostgreSQL: private subnet + private DNS, public access disabled

## Interview talking points

1. Never hardcode credentials in Git.
2. Terraform state can contain sensitive values, so secure the remote backend.
3. Use unique immutable image tags instead of relying on `latest`.
4. Use readiness/liveness probes and resource requests/limits.
5. Use rolling deployment and `kubectl rollout status`.
6. Distinguish Azure RBAC from Kubernetes RBAC.
7. Azure DevOps->ACR push permission is different from AKS->ACR pull permission.
