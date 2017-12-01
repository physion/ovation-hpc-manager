#! /bin/bash

API_TOKEN=$1
ACTIVITY_UUID=$2
USER_IMAGE=$3



# first job - no dependencies
jid1=$(sbatch ovation_download_files.job $API_TOKEN $ACTIVITY_UUID $USER_IMAGE | cut -f4 -d' ')

echo "${jid1}"
# multiple jobs can depend on a single job
jid2=$(sbatch --dependency=afterany:$jid1 ovation_user.job $ACTIVITY_UUID $USER_IMAGE | cut -f4 -d' ')


jid3=$(sbatch --dependency=afterany:$jid2 ovation_upload_result.job $API_TOKEN $ACTIVITY_UUID $jid2 $USER_IMAGE | cut -f4 -d' ')

squeue
