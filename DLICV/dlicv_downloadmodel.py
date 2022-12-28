#!/usr/bin/python3

# dlicv

import argparse as _argparse
import os as _os
import urllib.request
from urllib.parse import urlparse
import zipfile
import sys as _sys

##############################################################
## This is a dictionary that keeps the saved models for now
mdlurl = 'https://github.com/CBICA/DeepMRSeg-Models/raw/main/models'

modelDict = {}
modelDict['dlicv'] = mdlurl + '/DLICV/DeepMRSeg_DLICV_v1.0.zip'

##############################################################

## Path to saved models
DEEPMRSEG = _os.path.expanduser(_os.path.join('~', '.dlicv'))
MDL_DIR = _os.path.join(DEEPMRSEG, 'trained_models')

def _main():
    """Main program for the script to download pre-trained models."""
    
    argv = _sys.argv

    exeName = _os.path.basename(argv[0])

    descTxt = '{prog} downloads pre-trained DLICV model'.format(prog=exeName)

    ## Download model
    mdl_type = 'dlicv'

    mdlurl = modelDict[mdl_type]
    mdlfname = _os.path.basename(urlparse(mdlurl).path)
    outFile = _os.path.join(MDL_DIR , mdl_type, mdlfname)

    if _os.path.isdir(outFile.replace('.zip', '')):
        print("Model already downloaded: " + outFile.replace('.zip', ''))

    else:
        print("Loading model: " + mdl_type)

        outPath = _os.path.join(MDL_DIR , mdl_type)
        if not _os.path.exists(outPath):
            _os.makedirs(outPath)
            print('Created dir : ' + outPath)

        urllib.request.urlretrieve(mdlurl, outFile)
        print('Downloaded model : ' + outFile)

        with zipfile.ZipFile(outFile, 'r') as fzip:
            fzip.extractall(outPath)
            print('Unzipped model : ' + outFile.replace('.zip', ''))

        _os.remove(outFile)

if __name__ == "__main__":
    main()
