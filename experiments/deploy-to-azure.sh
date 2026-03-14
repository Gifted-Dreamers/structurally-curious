#!/bin/bash
# Deploy experiments to Azure GPU VM
# Prerequisites: az login, GPU quota approved
# Usage: ./deploy-to-azure.sh [subscription_id]

set -e

SUBSCRIPTION="${1:-e59fedee-bd27-4111-814f-08719788574e}"  # Default: Azure subscription 1
RESOURCE_GROUP="gpu-experiments"
VM_NAME="gpu-exp-vm"
LOCATION="eastus2"
VM_SIZE="Standard_NC4as_T4_v3"  # 1x T4 16GB, 4 vCPU, 28GB RAM
SSH_KEY="$HOME/.ssh/azure-gpu"
EXPERIMENTS_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "=== Deploying to Azure ==="
echo "Subscription: $SUBSCRIPTION"
echo "Location: $LOCATION"
echo "VM Size: $VM_SIZE"
echo "Experiments: $EXPERIMENTS_DIR"
echo ""

# 1. Set subscription
az account set --subscription "$SUBSCRIPTION"

# 2. Create resource group (idempotent)
echo "--- Creating resource group ---"
az group create --name "$RESOURCE_GROUP" --location "$LOCATION" --output none 2>/dev/null || true

# 3. Create VM
echo "--- Creating VM (this takes 2-3 minutes) ---"
VM_IP=$(az vm create \
  --resource-group "$RESOURCE_GROUP" \
  --name "$VM_NAME" \
  --image Canonical:ubuntu-24_04-lts:server:latest \
  --size "$VM_SIZE" \
  --admin-username azureuser \
  --ssh-key-values "${SSH_KEY}.pub" \
  --public-ip-sku Standard \
  --os-disk-size-gb 128 \
  --output tsv \
  --query publicIpAddress)

echo "VM created: $VM_IP"

# 4. Wait for SSH
echo "--- Waiting for SSH ---"
for i in {1..30}; do
  if ssh -i "$SSH_KEY" -o StrictHostKeyChecking=no -o ConnectTimeout=5 azureuser@"$VM_IP" "echo ok" 2>/dev/null; then
    break
  fi
  sleep 10
done

# 5. Upload experiment code
echo "--- Uploading experiments ---"
scp -i "$SSH_KEY" -r "$EXPERIMENTS_DIR" azureuser@"$VM_IP":~/experiments/

# 6. Run setup
echo "--- Running GPU setup (this takes 10-15 minutes) ---"
ssh -i "$SSH_KEY" azureuser@"$VM_IP" 'bash ~/experiments/setup-gpu-vm.sh'

echo ""
echo "=== READY ==="
echo "SSH: ssh -i $SSH_KEY azureuser@$VM_IP"
echo "Run: source ~/exp-env/bin/activate && cd ~/experiments"
echo "Exp 03b: python 03-geometric-correlation/run.py --gpu --all"
echo "Exp 04:  python 04-eigenspectral-profiles/run.py --all"
echo "Exp 05:  python 05-confidence-density/run.py --all"
echo "Exp 09:  python 09-multi-agent-consensus/run.py --all"
echo ""
echo "REMEMBER: Deallocate when done!"
echo "  az vm deallocate -g $RESOURCE_GROUP -n $VM_NAME"
echo "  (or delete everything: az group delete -n $RESOURCE_GROUP --yes)"
