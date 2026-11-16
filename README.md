# Azure from Zero: Photo Notes

The code for the **Azure** video course. One small app, Photo Notes (notes that can carry photos), grows on an Azure
free account: a budget and alerts, Entra ID and RBAC, the Azure CLI, a virtual machine, its own virtual network, storage,
App Service and Static Web Apps, Functions, free databases, containers, monitoring, Key Vault and policy, and finally
Bicep with GitHub Actions.

The root of this repository is the project as it stands after the latest finished chapter. Each chapter's finished
project is in [`chapters/`](chapters). Templates use placeholders such as `EMAIL`, `START` and `SUFFIX`; the videos
fill them in with `sed` into a `build/` folder that git ignores, so no account details are ever committed.

Everything runs in one region, `swedencentral`. Sign in with `az login` (Azure CLI); no keys are stored in the project.
Each chapter creates its resources in its own resource group and deletes it at the end, so follow along and clean up
the same way.

| # | Chapter | Folder |
|---|---------|--------|
| 1 | Your Free Azure Account, Safely | [chapters/01-your-free-azure-account-safely](chapters/01-your-free-azure-account-safely) |
| 2 | Identity: Entra ID, RBAC and Managed Identities | [chapters/02-identity-entra-id-rbac-and-managed-identities](chapters/02-identity-entra-id-rbac-and-managed-identities) |
| 3 | The Azure CLI and Cloud Shell | [chapters/03-the-azure-cli-and-cloud-shell](chapters/03-the-azure-cli-and-cloud-shell) |
| 4 | Virtual Machines: Your First Server | [chapters/04-virtual-machines-your-first-server](chapters/04-virtual-machines-your-first-server) |
| 5 | Virtual Networks: Private and Connected | [chapters/05-virtual-networks-private-and-connected](chapters/05-virtual-networks-private-and-connected) |
| 6 | Storage Accounts: Blobs, Files, Queues and Tables | [chapters/06-storage-accounts-blobs-files-queues-and-tables](chapters/06-storage-accounts-blobs-files-queues-and-tables) |
| 7 | Host a Web App: App Service and Static Web Apps | coming soon |
| 8 | Serverless with Azure Functions | coming soon |
| 9 | Databases: Azure SQL and Cosmos DB for Free | [chapters/09-databases-azure-sql-and-cosmos-db-for-free](chapters/09-databases-azure-sql-and-cosmos-db-for-free) |
| 10 | Containers: Container Registry and Container Apps | [chapters/10-containers-container-registry-and-container-apps](chapters/10-containers-container-registry-and-container-apps) |
| 11 | Monitoring: Azure Monitor, Log Analytics and Application Insights | [chapters/11-monitoring-azure-monitor-log-analytics-and-application-insights](chapters/11-monitoring-azure-monitor-log-analytics-and-application-insights) |
| 12 | Security: Key Vault, Azure Policy and Defender | [chapters/12-security-key-vault-azure-policy-and-defender](chapters/12-security-key-vault-azure-policy-and-defender) |
| 13 | Infrastructure as Code and CI/CD: Bicep and GitHub Actions | [chapters/13-infrastructure-as-code-and-ci-cd-bicep-and-github-actions](chapters/13-infrastructure-as-code-and-ci-cd-bicep-and-github-actions) |

## Versions

Azure CLI 2.92.0, Python 3.12 locally.

## License

MIT
