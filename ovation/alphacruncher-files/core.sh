#! /bin/bash

# first job - no dependencies
jid1=$(sbatch ovation_download_files.job $1 $2 | cut -f4 -d' ')

echo "${jid1}"
# multiple jobs can depend on a single job
jid2=$(sbatch --dependency=afterany:$jid1 ovation_user.job $jid1)


jid3=$(sbatch --dependency=afterany:$jid2 ovation_upload_result.job $1 $2 $jid2 | cut -f4 -d' ')

squeue
