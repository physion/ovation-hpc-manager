#! /bin/bash

# first job - no dependencies
jid1=$(sbatch ovation_download_files.job | cut -f4 -d' ')

echo "${jid1}"
# multiple jobs can depend on a single job
jid2=$(sbatch  --dependency=afterany:$jid1 ovation_upload_result.job)

squeue
