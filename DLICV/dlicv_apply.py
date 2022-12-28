#!/usr/bin/python3

# dlicv

import argparse as _argparse
import os as _os
import sys as _sys
import urllib.request
from urllib.parse import urlparse
import zipfile
from . import dlicv_test
from . import pythonUtilities

_os.environ['COLUMNS'] = "90"

##############################################################
## Path to saved models

DLICV = _os.path.expanduser(_os.path.join('~', '.dlicv'))
MDL_DIR = _os.path.join(DLICV, 'trained_models')

modelDict = {}
modelDict['dlicv'] = _os.path.join(MDL_DIR, 'dlicv', 'DeepMRSeg_DLICV_v1.0')

##############################################################

#DEF ARGPARSER
def read_flags(argv):
    """Parses args and returns the flags and parser."""
    ### Import modules
    import argparse as _argparse

    exeName = _os.path.basename(argv[0])

    descTxt = '{prog} segments dlicv using pre-trained model. Users should first download the trained model using dlicv_downloadmodel'.format(prog=exeName)

    epilogTxt = '''Examples:
    
  ## Apply dlicv model on single image (Use Case A)
  dlicv_downloadmodel
  {prog} --inImg sub1_T1.nii.gz --outImg sub1_DLICV.nii.gz
      
  ## Apply dlicv model on all T1 images in the input folder (Use Case B)
  {prog} --inDir /my/indir --outDir /my/outdir --inSuff _T1.nii.gz --outSuff _DLICV.nii.gz
 
  ## Apply dlicv model on multiple subjects using an image list (Use Case C)
  {prog} --sList dlicv_list.csv
     with dlicv_list.csv:
       ID, InImg, OutImg
       sub1,/my/indir/sub1_T1.nii.gz,/my/outdir/sub1_DLICV.nii.gz
       sub2,/my/indir/sub2_T1.nii.gz,/my/outdir/sub2_DLICV.nii.gz
       ...
 
  '''.format(prog=exeName)

    parser = _argparse.ArgumentParser( formatter_class=_argparse.RawDescriptionHelpFormatter, \
        description=descTxt, epilog=epilogTxt )

#    I/O
#    ==========
    ## I/O Option1: Single case processing
    ioArgs1 = parser.add_argument_group( 'Use Case A', 'Single scan processing')
    ioArgs1.add_argument( "--inImg", action='append', default=None, type=str, \
        help=    'Input image name. For multi-modal tasks multiple image names \
            can be entered as "--inImg imgMod1 --inImg imgMod2 ..." . (REQUIRED)')
    
    ioArgs1.add_argument( "--outImg", default=None, type=str, \
        help=    'Output image name. (REQUIRED)')

    ## I/O Option3: Batch I/O from folder
    ioArgs3 = parser.add_argument_group( 'Use Case B', 'Batch processing of all scans in a folder')
    ioArgs3.add_argument( "--inDir", default=None, type=str, \
        help=    'Input folder name. (REQUIRED)')
    
    ioArgs3.add_argument( "--outDir", default=None, type=str, \
        help=    'Output folder name. (REQUIRED)')
    
    ioArgs3.add_argument( "--inSuff", default='.nii.gz', type=str, \
        help='Input image suffix (default: .nii.gz)')
    
    ioArgs3.add_argument( "--outSuff", default='_SEG.nii.gz', type=str, \
        help="Output image suffix  (default: _DLICV.nii.gz)")

    ## I/O Option2: Batch I/O from list
    ioArgs2 = parser.add_argument_group( 'Use Case C', 'Batch processing using image list')
    ioArgs2.add_argument( "--sList", default=None, type=str, \
        help=    'Image list file name. Enter a comma separated list file with \
            columns for: ID, InImg, OutImg. (REQUIRED)')

#    OTHER OPTIONS
#    ===========
    otherArgs = parser.add_argument_group( 'OTHER OPTIONS')

    otherArgs.add_argument( "--batch", default=None, type=int, \
        help="Batch size  (default: Depends on the task)" )

    otherArgs.add_argument( "--probs", default=False, action="store_true", \
        help=    'Flag to indicate whether to save a probability map for \
            each segmentation label. (default: False)')

    otherArgs.add_argument( "--nJobs", default=None, type=int, \
        help="Number of jobs/threads (default: automatically determined)" )
    
    otherArgs.add_argument( "--tmpDir", default=None, type=str, \
                help=    'Absolute path to the temporary directory. If not provided, \
            temporary directory will be created automatically and will be \
            deleted at the end of processing. (default: None)' )

    ### Read args from CLI
    flags = parser.parse_args(argv[1:])

    ### Return flags and parser
    return flags, parser

    #ENDDEF ARGPARSER


def verify_flags(FLAGS, parser):
    
    ##################################################
    ### Check required args

    ## Check Use Cases
    if FLAGS.inImg is not None:                         ## CASE A: Single inImg
        for tmpImg in FLAGS.inImg:
            pythonUtilities.check_file( tmpImg )

    elif FLAGS.inDir is not None:                       ## CASE B: Img dir
        pythonUtilities.check_file( FLAGS.inDir )
        if FLAGS.outDir is None:
            parser.print_help( _sys.stderr )
            print('ERROR: Missing required arg: outDir')
            _sys.exit(1)

    elif FLAGS.sList is not None:                       ## CASE C: Img list
        pythonUtilities.check_file( FLAGS.sList )        
            
    else:
        parser.print_help( _sys.stderr )
        print('ERROR: Missing required arg - The user should select options for one of the 3 Use Cases')
        _sys.exit(1)

def _main():
    """Main program for the script"""

    ### init argv
    argv0 = [_sys.argv[0]]
    argv = _sys.argv

    ### Read command line args
    FLAGS, parser = read_flags(argv)
    verify_flags(FLAGS, parser)

    ## Add models in 3 orientation        
    argv = argv[1:]
    argv.append('--mdlDir')
    argv.append(_os.path.join(modelDict[FLAGS.task], 'LPS'))
    argv.append('--mdlDir')
    argv.append(_os.path.join(modelDict[FLAGS.task], 'PSL'))
    argv.append('--mdlDir')
    argv.append(_os.path.join(modelDict[FLAGS.task], 'SLP'))
    print(argv)
    #print(argsExt)
    
    print('Calling dlicv_test')
    dlicv_test._main_warg(argv0 + argv)

if __name__ == "__main__":
    _main()
