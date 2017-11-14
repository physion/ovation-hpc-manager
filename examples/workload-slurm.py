#!/usr/bin/python

from sys import exit
import re, os

import pythoncm
clustermanager = pythoncm.ClusterManager()
if os.path.isfile('/root/.cm/admin.pem'):
  cluster = clustermanager.addCluster('https://localhost:8081', '/root/.cm/admin.pem', '/root/.cm/admin.key');
elif os.path.isfile('/root/.cm/cmsh/admin.pem'):
  cluster = clustermanager.addCluster('https://localhost:8081', '/root/.cm/cmsh/admin.pem', '/root/.cm/cmsh/admin.key');
else:
  print "No certificate found"
  exit(1)

if not cluster.connect():
  print "Unable to connect"
  print cluster.getLastError()
  exit(1)

###################################################
# Submit test mpi job into SLURM via CMDaemon API #
###################################################

job = pythoncm.Job()

# The same as sbatch --partition
job.queue = 'defq'

# The same as sbatch --job-name
job.jobname = 'myjob'

# The same as sbatch --account
job.account = 'myaccount'

# The same as sbatch --workdir
job.rundirectory = '/home/cmsupport'

# The same as sbatch --uid
job.username = 'cmsupport'

# The same as sbatch --gid
job.groupname = 'cmsupport'

# The same as sbatch --nice
job.priority = '1'

# The same as sbatch --input
job.stdinfile = '/home/cmsupport/stdin-openmpi'

# The same as sbatch --output
job.stdoutfile = '/home/cmsupport/stdout-openmpi'

# The same as sbatch --error
job.stderrfile = '/home/cmsupport/stderr-openmpi'

# The same as sbatch --constraint
job.resourceList = ['nodefeature']

# The same as sbatch --dependency
job.dependencies = ['afterok:42']

# Notify by email
job.mailNotify = True

# The same as sbatch --mail-type
job.mailOptions = 'ALL'

# The same as sbatch --mail-user
job.mailList = 'cmsupport@master.cm.cluster'

# The same as sbatch --time
job.maxWallClock = '00:01:00'

# The same as sbatch --ntasks
job.numberOfProcesses = 1

# The same as sbatch --nodes
job.numberOfNodes = 1

# The same as sbatch --nodelist
# Nodes could be defined either as hostnames or as unique keys
job.nodes = ['node001']

# Additional environment variables which will be exported before submission
#job.environmentVariables = ['TERM=xterm']

# Job script shebang
job.commandLineInterpreter = '/bin/bash'

# User defined lines will be put inside job script before executable
job.userdefined = ['cd /home/cmsupport', 'date', 'pwd']

# Executable name and its arguments which will be put
# at the end of a new created jobscript; the binary,
# in this case /home/cmsupport/hello_mpi, must exist
job.executable='mpirun'
job.arguments='hello_mpi'

# Module files will be added to job script environment
job.modules = ['openmpi/gcc']

# Debug option enables dry run and debug info will be returned
job.debug = True

# If scriptfile is specified, then only it will be submitted
#job.scriptFile = "/home/cmsupport/openmpi-job"

print cluster.submitJob(job) # OR cluster.submitJob(job, 'slurm')

jobs = cluster.getJobs()  # OR cluster.getJobs('slurm')
if len(jobs):
  print
  jobs_ids = []
  for job in jobs:
    jobs_ids.append(job.jobID)
  print "Jobs in queues:",','.join(jobs_ids)
else:
  print "No jobs found"

cluster.disconnect()
