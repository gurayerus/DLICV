# DLICV

DLICV is a Python-based package for segmenting the intra-cranial volume (ICV) on T1-weighted MRI scans.

DLICV operates directly on the raw T1 scan, and produces a binary ICV mask. The ICV mask can be used as a "brain mask" for subsequent image processing steps, as well as for estimating the ICV value, a variable used for correcting other imaging variables against variations in head size across subjects.

DLICV aims to provide a more accurate estimation of the actual ICV, mainly by delineating the external boundary of cortical cerebro-spinal-fluid (CSF), rather than focusing on segmenting a "tight brain mask" as done by many other methods. This is specifically critical for cases with a lot of cortical atrophy (i.e. a tight brain mask would underestimate the actual ICV, while DLICV would be minimally affected from cortical atrophy)

DLICV uses the [DeepMRSeg](https://github.com/CBICA/DeepMRSeg) package for segmentation, a generic convolutional Deep Learning model designed to perform a set of image segmentation tasks on MRI scans.

## Prerequisities
-   [Python 3](https://www.python.org/downloads/)
-   If you prefer conda, you may install it from [here](https://www.anaconda.com/products/individual)

## Installation Instructions
DLICV can be run on CPU. For the application of a pre-trained DLICV model on a new image, performance is comparable between running it on CPU or GPU. The users can optionally setup their GPU for using with tensorflow following the tensorflow guide for [GPU support](https://www.tensorflow.org/install/gpu).

### 1) Direct installation at default location 
```
git clone  https://github.com/gurayerus/DLICV.git
cd DLICV
python setup.py install #install DLICV and its dependencies
```

### 2) Installation in conda environment
```
conda create --name DLICV python=3.7.9
conda activate DLICV
```
Then follow steps from [direct installation](#direct-installation-at-default-location)

## Usage

After installation of the package, users can call DeepMRSeg commands on the command prompt (or on Anaconda prompt):

### Step 1: Load pre-trained model

Pre-trained DLICV model should be first downloaded to a pre-defined local folder (_~/.dlicv/trained_models_) automatically using the command:

```
dlicv_downloadmodel 
```

### Step2: Apply DLICV

Users can apply DLICV on their input scan(s) in .nii.gz or .nii format using the command "dlicv_apply". The command provides a different set of options for three different use cases:

#### Use case A: Segment single scan

For processing a single scan

```
dlicv_apply --inImg subj1_T1.nii.gz --outImg subj1_T1_DLICV.nii.gz
```

#### Use case B: Segment all scans in a folder

For processing multiple scans, but the data should be organized in a single folder, so less flexibility 

```
dlicv_apply --inDir myindir --outDir myoutdir --inSuff _T1.nii.gz --outSuff _DLICV.nii.gz

# Segmentation is applied sequentially to each scan with the given suffix in the input folder
# Output mask is saved in the provided out dir, with the same base name for each scan with input suffix replaced by output suffix

```

#### Use case C: Segment all scans in a list

For processing multiple scans in a more flexible way, but the user should prepare a list with information about input/output simages

```
dlicv_apply --sList subjectList.csv

# User provides a csv file with columns: ID, InImg, OutImg , with values for each scan in a row

```

Please call the commands with the -h option to display usage information

## License

## How to cite DLICV

## Publications

_[1] Doshi, Jimit, et al. DeepMRSeg: A convolutional deep neural network for anatomy and abnormality segmentation on MR images. arXiv preprint arXiv:1907.02110 (2019)_.

## Authors and Contributors

The DLICV package is currently developed and maintained by:

Others who contributed to the project are:

## Grant support

Development of the DLICV package is supported by the following grants:

## Disclaimer
-   The software has been designed for research purposes only and has neither been reviewed nor approved for clinical use by the Food and Drug Administration (FDA) or by any other federal/state agency.
-   This code (excluding dependent libraries) is governed by the license provided in https://www.med.upenn.edu/cbica/software-agreement-non-commercial.html unless otherwise specified.
-   By using DLICV, you agree to the license as stated in the [license file](https://github.com/CBICA/DeepMRSeg/blob/main/LICENSE).

## Contact
For more information, please contact <a href="mailto:guray.erus@pennmedicine.upenn.edu">CBICA Software</a>.
