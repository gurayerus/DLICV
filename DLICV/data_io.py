
################################################ DECLARATIONS ################################################
__author__ 	= 'Jimit Doshi'
__EXEC_NAME__ 	= "data_io"

import numpy as _np

from . import rescaleimages
from . import pythonUtilities
from . import tfrecordutils

################################################ FUNCTIONS ################################################

#DEF
def check_files( refImg=None, otherImg=None, labImg=None ):

	### Import modules
	import nibabel as _nib

	### Check if the files exist
	pythonUtilities.check_file( refImg )
	if labImg:
		pythonUtilities.check_file( labImg )
	if otherImg:
		for m in otherImg:
			pythonUtilities.check_file( m )

	### Load files
	ref = _nib.load( refImg )
	if labImg:
		lab = _nib.load( labImg )
	others = []
	if otherImg:
		for m in range( len(otherImg) ):
			others.extend( [ _nib.load( otherImg[m] ) ] )

	### Check if they have the same dimensions
	if labImg:
		assert lab.shape == ref.shape, "Shape misatch between %s and %s images" % ( labImg,refImg )

	if otherImg:
		for m in range( len(otherImg) ):
			assert others[m].shape == ref.shape, "Shape misatch between %s and %s images" % ( otherImg[m],refImg )

	### Check if they have the same affine matrices
	if labImg:
		assert ( _np.round(lab.header.get_base_affine(),4) == _np.round(ref.header.get_base_affine(),4) ).all(), \
						"Affine matrix misatch between %s and %s" % ( labImg,refImg )

	if otherImg:
		for m in range( len(otherImg) ):
			assert ( _np.round(others[m].header.get_base_affine(),4) == _np.round(ref.header.get_base_affine(),4) ).all(), \
						"Affine matrix misatch between %s and %s" % ( otherImg[m],refImg )

#ENDDEF

#DEF
def load_res_norm( in_path,xy_width,ressize,orient='LPS',mask=0,rescalemethod='minmax',out_path=None ):

	### Import modules
	import nibabel as _nib
	import nibabel.processing as _nibp
	
	### Load image if it is a file path
	#IF
	if isinstance( in_path,str ):
		FileRead = _nib.load( in_path )
	### Else, verify if it is a nibabel object with a header
	elif isinstance( in_path,_nib.Nifti1Image ):
		assert in_path.header
		FileRead = in_path
	#ENDIF
    
	### Re-orient, resample and resize the image
	#IF
	if mask:
		spline_order = 0	#NN
	else:
		spline_order = 1	#Linear
	#ENDIF

	FileRead_res = _nibp.conform( FileRead, \
					out_shape=(xy_width,xy_width,xy_width), \
					voxel_size=(ressize,ressize,ressize), \
					orientation=orient, \
					order=spline_order )

	# IF
	if len( FileRead_res.get_data().shape ) > 3:
		FileDat = FileRead_res.get_data()[ :,:,:,0 ]
	else:
		FileDat = FileRead_res.get_data()
	# ENDIF

    	### Rescale image
	if mask == 0:
		FileDat = rescaleimages.rescale_image( FileDat, minInt=0, maxInt=1, perc=99.9, method=rescalemethod )
    		
	# IF
	# Save as numpy file
	if out_path:
		_np.save( out_path, FileDat )
	# Return numpy array
	else:
		return FileDat, FileRead_res
	# ENDIF
#ENDDEF

#DEF
def extract_data_for_subject( otherImg=None, refImg=None, labImg=None, \
				ressize=1, orient='LPS', out_path=None, xy_width=320, rescalemethod='minmax' ):
	
	### Load images
	ref,_ = load_res_norm( refImg,xy_width,ressize,orient,mask=0,rescalemethod=rescalemethod )
	lab,_ = load_res_norm( labImg,xy_width,ressize,orient,mask=1 )
	others = []
	for img in otherImg:
		others.extend( [ load_res_norm( img,xy_width,ressize,orient,mask=0,rescalemethod=rescalemethod )[0] ] )
		
	### Restructure matrices from [x,y,z] to [z,x,y]
	ref = _np.moveaxis( ref,2,0 )
	lab = _np.moveaxis( lab,2,0 )
	for m in range( len(otherImg) ):
		others[m] = _np.moveaxis( others[m],2,0 )
	
	### Reshape T1 and FL to add a new axis
	ref = ref.reshape( ( ref.shape+(1,) ) )
	lab = lab.reshape( ( lab.shape+(1,) ) )
	for m in range( len(otherImg) ):
		others[m] = others[m].reshape( ( others[m].shape+(1,) ) )

	### Return appended T1 and FL and the wml
	#IF
	if len(otherImg) > 0:
		allMods = ref.copy()
		for m in range( len(otherImg) ):
			allMods = _np.append( allMods,others[m],axis=3 )
		
		return allMods, lab
	else:
		return ref, lab
	#ENDIF
#ENDDEF

#DEF
def extract_pkl( subListFile, idcolumn, labCol, refMod, otherMods, num_modalities, subjectlist, \
		roicsv=None, out_path=None, rescalemethod='minmax', xy_width=320, \
		pos_label_balance=1, ressize=1, orient='LPS' ):

	### Import modules
	import csv as _csv
	
	### Extract data for training
	#WITH
	with open(subListFile) as f:
		reader = _csv.DictReader( f )
		idcolumn = reader.fieldnames[0]

		#FOR
		for row in reader:
			#IF
			if row[idcolumn] in subjectlist:
				
				# Get files for other modalities
				otherModsFileList = []
				if otherMods:
					for mod in otherMods:
						otherModsFileList.extend( [ row[mod] ] )
		
				# extract data from images
				imdat,imlab = extract_data_for_subject( \
						otherImg=otherModsFileList, \
						refImg=row[refMod], \
						labImg=row[labCol], \
						ressize=ressize, \
						orient=orient, \
						xy_width=xy_width, \
						out_path=None, \
						rescalemethod=rescalemethod )
				
				# encode rois to indices if provided
				#IF
				if roicsv:
					imlab_enc = _np.zeros_like( imlab )
					
					#WITH
					with open(roicsv) as roicsvfile:
						roi_reader = _csv.DictReader( roicsvfile )

						#FOR
						for roi_row in roi_reader:
							imlab_enc = _np.where( imlab.astype(int)==int(roi_row['ROI']), \
										int(roi_row['Index']), imlab_enc )
						#ENDFOR
					#ENDWITH
					
					imlab = imlab_enc.copy()
					del imlab_enc
				#ENDIF
					
				
				
				# Oversample foreground labels
				#IF
				if pos_label_balance>1:
					pos_sample_slices = imdat[ _np.where( imlab.sum(axis=(3,2,1)) > 0 ), :,:,: ][ 0 ]
					pos_sample_labels = imlab[ _np.where( imlab.sum(axis=(3,2,1)) > 0 ), :,:,: ][ 0 ]
				
					#FOR
					for _ in range( 1,pos_label_balance ):
						imlab = _np.append( imlab,pos_sample_labels,axis=0 )
						imdat = _np.append( imdat,pos_sample_slices,axis=0 )
					#ENDFOR
					
					del pos_sample_labels, pos_sample_slices
				#ENDIF
				
				# Shuffle data
				indices = _np.arange( imlab.shape[0] )
				_np.random.shuffle( indices )

				imdat = imdat[ indices ]
				imlab = imlab[ indices ]
				
				tfrecordutils.tfrecordwriter( out_path, \
								rfeats=imdat, \
								rlabels=imlab, \
								feats_dtype='float32', \
								labels_dtype='int64' )
				
			# ENDIF
		#ENDFOR
	#ENDWITH
	
	del imdat,imlab,indices
#ENDDEF
