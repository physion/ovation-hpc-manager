# kube-lego

The _hpc-manager_ requires `kube-lego` running on the cluster.

To install:
(**FIXME: jetstack isn't a helm chart**)
```bash
helm install --name kube-lego-development stable/kube-lego\
    --namespace development \
    --set config.LEGO_EMAIL=dev@ovation.io \
    --set config.LEGO_URL=https://acme-staging.api.letsencrypt.org/directory
```

For production use
```
LEGO_URL=https://acme-v01.api.letsencrypt.org/directory
namespace=production
```
