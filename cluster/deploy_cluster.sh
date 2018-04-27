#!/usr/bin/env bash

VERSION=$1

rm *.img

sudo singularity build ovation_download_files.img ovation_download_files.def
sudo singularity build ovation_upload_result.img ovation_upload_result.def

scp *.img ovation@scc.alphacruncher.net:/cm/shared/sing-images/ovation/

scp ovation_core.sh ovation@scc.alphacruncher.net:~/bin/$VERSION/
scp ovation_delivery.py ovation@scc.alphacruncher.net:~/bin/$VERSION/
scp *.job ovation@scc.alphacruncher.net:~/bin/$VERSION/
