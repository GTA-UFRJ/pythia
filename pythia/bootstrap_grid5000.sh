#This file should run in the g5k frontend

#Setup Kubernetes
git clone $TERRAFORM_PROVIDER_REPO
mv $TERRAFORM_CONFIG terraform-provider-grid5000/examples/kubernetes
cd terraform-provider-grid5000/examples/kubernetes
terraform init
terraform apply -auto-approve
export KUBECONFIG=${PWD}/kube_config_cluster.yml

/Users/cruz/Code Kollaps-master/kollaps/Kollapslib/deploymentGenerators/bootstrap_grid500.sh