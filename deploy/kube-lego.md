# kube-lego

The _hpc-manager_ requires `kube-lego` running on the cluster.

To install:
```bash
helm upgrade --install kube-lego stable/kube-lego\
    --namespace development \
    --set config.LEGO_URL=https://acme-v01.api.letsencrypt.org/directory \
    --set config.LEGO_EMAIL=dev@ovation.io \
    --set config.LEGO_DEFAULT_INGRESS_CLASS=gce \
    --set rbac.create=true 
```

(default `LEGO_URL` is https://acme-staging.api.letsencrypt.org/directory)

You may need to use `--set rbac.create=true` if RBAC is not already available

For production use
```
LEGO_URL=https://acme-v01.api.letsencrypt.org/directory
namespace=production
```
