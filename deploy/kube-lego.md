# kube-lego

The _hpc-manager_ requires `kube-lego` running on the cluster.

To install:
```bash
helm install --name development stable/kube-lego\
    --namespace development \
    --set config.LEGO_EMAIL=dev@ovation.io \
    [--set config.LEGO_URL=https://acme-staging.api.letsencrypt.org/directory] # default
```

You may need to use `--set rbac.create=true` if RBAC is not already available

For production use
```
LEGO_URL=https://acme-v01.api.letsencrypt.org/directory
namespace=production
```
