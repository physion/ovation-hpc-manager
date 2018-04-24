#!/usr/bin/env bash

#singularity build ovation_download_files.img ovation_download_files.def
#scp

singularity build ovation_upload_result.img ovation_upload_result.def
scp ovation_upload_result.img ovation@scc.alphacruncher.net:/cm/shared/sing-images/ovation/


