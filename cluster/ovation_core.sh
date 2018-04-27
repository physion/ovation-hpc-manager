#! /bin/bash

ORG=$1
API_TOKEN=$2
ACTIVITY_UUID=$3
USER_IMAGE=$4
OVATION_CLI_ARGS=$5
VERSION="1.0.0"



# first job - no dependencies
jid1=$(sbatch ~/bin/$VERSION/ovation_download_files.job $ORG $API_TOKEN $ACTIVITY_UUID $USER_IMAGE $OVATION_CLI_ARGS | cut -f4 -d' ')

# multiple jobs can depend on a single job
jid2=$(sbatch --dependency=afterany:$jid1 ~/bin/$VERSION/ovation_user.job $ACTIVITY_UUID $USER_IMAGE $jid1 | cut -f4 -d' ')


sbatch --dependency=afterany:$jid2 ~/bin/$VERSION/ovation_upload_result.job $ORG $API_TOKEN $ACTIVITY_UUID $jid2 $USER_IMAGE $jid1 $OVATION_CLI_ARGS

squeue
