#!/usr/bin/env bash

NAMESPACE=$1

set -e

RELEASE_NAME=indexer-$NAMESPACE
CI_TIMESTAMP=local

# Install helm
curl https://raw.githubusercontent.com/kubernetes/helm/master/scripts/get | bash
helm init --upgrade

# Install helm-secrets
echo "Installing helm-secrets"
helm plugin install https://github.com/futuresimple/helm-secrets

echo "Upgrading indexer release..."

echo "NAMESPACE = $NAMESPACE"
echo "RELEASE_NAME = $RELEASE_NAME"
echo "CI_TIMESTAMP = $CI_TIMESTAMP"

helm-wrapper upgrade --install  --namespace=${NAMESPACE} --timeout 600 --wait \
    --set image.tag=${NAMESPACE}-${CI_TIMESTAMP} \
    -f ./deploy/values/${NAMESPACE}/secrets.yaml \
    ${RELEASE_NAME} \
    ./deploy/ovation-hpc/
