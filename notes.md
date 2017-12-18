# Notes

## Falcon
- [x] add gunicorn -> falcon app for liveness/readiness probe
- [x] update `startup.sh` to start falcon app
- [x] update `make_system` to create & return api
- [x] update liveness probe with `initialDelaySeconds: 60`

## VPN
- [x] create vpn secret
- [x] download ovation.ovpn
- [x] modify ovpn and create credentials file
- [x] add ovpn and credentials text to `.Values.secret.(OVATION_OVPN|VPN_CREDENTIALS)`

## Auth/Authz
- [ ] Pass user auth0 ID with message
- [ ] Get user access token from Web API
- [ ] Ovation service key for getting access token

## Callbacks
- [ ] provide Google credentials.json to paramkiko -> core.sh -> last job
- [ ] publish to pubsub from job success/failure

## Web API
- [ ] `activities/:id/run` 
- [ ] request user access_token `/oauth/authorize`? (requites `masquerade:global`)
    - [ ] Can we add all `/oauth` proxy to Auth0?
- [ ] add `masquerade:global` scope
