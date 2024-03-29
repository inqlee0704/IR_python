# ##############################################################################
# Usage: python Emph.py Subj Emphysema_threshold 
# Time: ~ 40s
# Ref: [Computed tomography–based biomarker provides unique signature...]
# ##############################################################################
# 03/22/2021, In Kyu Lee
# Calculate Emphy% only
# ##############################################################################
# Input: 
#  - IN CT image, ex) PMSN03001_IN0.img.gz
#  - IN lobe mask, ex) PMSN03001_IN0_vida-lobes.img
# Output:
#  - Emphysema statistics, ex) PMSN03001_EX0-TO-PMSN03001_IN0-SSTVD_lobar_Emph.txt
#  - Emphysema image, ex) PMSN03001_EX0-TO-PMSN03001_IN0-SSTVD_Emph.img
# ##############################################################################

# import libraries
import os
import sys
from medpy.io import load, save
import numpy as np
import pandas as pd
import time
import SimpleITK as sitk
sitk.ProcessObject_SetGlobalWarningDisplay(False)

start = time.time()
Subj = str(sys.argv[1]) # Subj = 'PMSN03001'
I1 = str(sys.argv[2]) # I1 = 'IN0'
I2 = str(sys.argv[3]) # I2 = 'EX0'
if len(sys.argv)==3:
    emphy_threshold = -950
else:
    emphy_threshold = int(sys.argv[4])

# Input Path
IN_path = f'{Subj}_{I1}.img.gz'
IN_lobe_path = f'{Subj}_{I1}_vida-lobes.img'
if not os.path.exists(IN_lobe_path):
    IN_lobe_path = f'{Subj}_{I1}_vida-lobes.img.gz'

# Output Path
emphy_stat_path = f'{Subj}_{I2}-TO-{Subj}_{I1}-SSTVD_lobar_Emph.txt'
emphy_img_path = f'{Subj}_{I2}-TO-{Subj}_{I1}-SSTVD_Emph.img'

# Data Loading . . .
IN_img,IN_header = load(IN_path)
IN_lobe_img, IN_lobe_header = load(IN_lobe_path)
# get .hdr from IN.hdr
emphy_h = IN_header

# prepare .img
emphy_img = np.zeros((IN_img.shape),dtype='uint8')
# 2 if Emphysema
emphy_img[(IN_img<emphy_threshold)] = 2
# 0 if outside lobe
emphy_img[IN_lobe_img==0] = 0

# prepare emphysema & fsad stats
IN_l0 = len(IN_img[IN_lobe_img==8])
IN_l1 = len(IN_img[IN_lobe_img==16])
IN_l2 = len(IN_img[IN_lobe_img==32])
IN_l3 = len(IN_img[IN_lobe_img==64])
IN_l4 = len(IN_img[IN_lobe_img==128])
IN_t = IN_l0 + IN_l1 + IN_l2 + IN_l3 + IN_l4

emphy_l0 = len(emphy_img[(IN_lobe_img==8)&(emphy_img==2)])
emphy_l1 = len(emphy_img[(IN_lobe_img==16)&(emphy_img==2)])
emphy_l2 = len(emphy_img[(IN_lobe_img==32)&(emphy_img==2)])
emphy_l3 = len(emphy_img[(IN_lobe_img==64)&(emphy_img==2)])
emphy_l4 = len(emphy_img[(IN_lobe_img==128)&(emphy_img==2)])
emphy_t = emphy_l0 + emphy_l1 + emphy_l2 + emphy_l3 + emphy_l4

emphy_stat = pd.DataFrame({'Lobes':['Lobe0','Lobe1','Lobe2','Lobe3','Lobe4','Total'],
              'Emphysratio':np.float16([emphy_l0/IN_l0,emphy_l1/IN_l1,emphy_l2/IN_l2,emphy_l3/IN_l3,emphy_l4/IN_l4,emphy_t/IN_t]),
              'voxels_Emphys':[emphy_l0,emphy_l1,emphy_l2,emphy_l3,emphy_l4,emphy_t],
              'VoxelsAll':[IN_l0,IN_l1,IN_l2,IN_l3,IN_l4,IN_t]})

# Save
emphy_stat.to_csv(emphy_stat_path, index=False, sep=' ')
save(emphy_img,emphy_img_path,hdr=emphy_h)
end = time.time()
print(f'Elapsed time: {end-start}')
