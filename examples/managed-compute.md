# Managed Compute

## Summary
Ovation supports running compute for Activities using the managed HPC service `https://hpc.ovation.io`. A compute 'job'
can be run for any Activity that has a compute container image associated with the Activity.

With managed compute, you and your collaborators can: 

- run analyses of data stored within Ovation
- automatically store analysis results in Ovation
- track provenance of analyses including inputs, outputs, parameters, and code

## Compute image
Ovation's HPC service uses [Singularity](https://singularity.lbl.gov/) images to package the executable(s) and dependencies of a computation.
Each compute job is associated with one Activity entity in Ovation.

If you are new to Singularity and HPC, [Quick Start](https://singularity.lbl.gov/quickstart) will help you get started creating a Singularity image containing your desired compute executable and dependencies.

Your image's default command should be an executable that takes no arguments. 

When you run a compute job, the compute service will call the default command of your Singularity image. The compute service will download the
_Inputs_ of an Activity to a volume mounted at `/inputs` within the image. If you need to pass parameters to your executable,
add those parameters in an _Input_ file to the activity. The compute service will also download the Activity's _Related_ files 
and mount them at `/related` within the image. 

Your image's executable should place outputs into `/outputs`. The contents of `/outputs`, and
the stdout and stderr logs from your compute job will be uploaded to the Activity's _Outputs_ upon job completion (or failure).   

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

