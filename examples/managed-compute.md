# Managed Compute

## Summary
Ovation supports running compute for any Activity that has an associated compute container image, using the managed HPC service _https://hpc.ovation.io_.

**The Ovation Compute service is currently in BETA.**

**The Ovation Compute service is NOT covered by the Ovation Business Associate Agreement.**

## Compute image
Ovation's compute service uses [Singularity](https://singularity.lbl.gov/) images to package the executable(s) and dependencies of a computation. 
This [Quick Start](https://singularity.lbl.gov/quickstart) can help you get started creating a Singularity image with your desired compute executable and dependencies. 

When you run a compute job, the compute service will run your Singularity image. Your image's command should be an executable that takes no arguments. 
Each compute job is associated with one Activity entity in Ovation. Your executable can read the
_Inputs_ of the Activity at `/data/inputs` within the image. If you need to pass parameters to your executable,
add those parameters in an _Input_ file to the activity. The compute service will also make Activity's _Associated_ files 
available at `/data/related` within the image. 

Your image's executable should place outputs into `/data/outputs`. The contents of `/data/outputs`, and
the stdout and stderr logs from your compute job will be uploaded to the Activity's _Outputs_ upon job completion (or failure).

This simple image definition defines a Singularity image that copies the contents of `/data/inputs/in.txt` to `/data/outputs/out.txt`:

```
BootStrap: docker
From: ubuntu:16.04

%post
    # Will be bound to a folder containing:
    # ./inputs: Contents of Ovation Activity's "inputs"
    # ./related: Contents of Ovation Activity's "associated files"
    # ./outputs: Files added here by your job will be uploaded to the Activity's outputs upon job completion
    mkdir /data
    chmod 777 /data

    # Un-comment these if you need access to the Ovation Python API from your job:
    #apt-get -y update && apt-get -y install python3-pip
    #pip3 install -U ovation

%runscript

    cat /data/inputs/in.txt > /data/outputs/out.txt

```   

## Activity setup
You can run a compute job for any `Activity` within Ovation. Any user with access to the Activity and the input file(s)
is permitted to start a compute job for the activity. 
  
1. Add the input(s) of the computation to the Activity's _Inputs_ section by clicking "Add Inputs" to add existing
files from the Project, or by dragging and dropping new files onto the _Inputs_ section of the Activity:

2. Add the compute image to the Activity's _Related_ files. You can add more than one image but only one image can be run 
in each compute job (you'll specify the name of that image when starting the compute job):

3. You can optionally indicate the operator that's running the compute or that wrote the analysis so that future collaborators
can know who performed the analysis:

## Running the compute job
To run a compute job, use the `hpc_run` command within the Ovation Python CLI:

```bash
$ python -m ovation.cli hpc_run --activity $ACTIVITY_UUID --image $IMAGE_NAME
```

where `$ACTIVITY_UUID` is the Id of the Activity, and `$IMAGE_NAME` is the _name_ of the image file. In the example above,
you would pass `dummy_pipeline.simg`.

