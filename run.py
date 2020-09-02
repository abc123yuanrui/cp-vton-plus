
import os, subprocess, sys, datetime, signal, shutil

runcase = int(sys.argv[1])
print ("Testing end to end %d" % runcase)

def preexec(): # Don't forward signals.
    os.setpgrp()
    
def mycall(cmd, block=False):
    if not block:
        return subprocess.Popen(cmd)
    else:
        return subprocess.Popen(cmd, preexec_fn = preexec)
    
def folder_check(path):
    try_num = 1
    oripath = path[:-1] if path.endswith('/') else path
    while os.path.exists(path):
        print("Delete existing folder " + path + "?(Y/N)")
        decision = input()
        if decision == "Y":
            shutil.rmtree(path, ignore_errors=True)
            break
        else:
            path = oripath + "_%d/"%try_num
            try_num += 1
            print(path)
    
    return path

if( runcase == 0 ): # download inference data, trained models
    cmd1 = "python segamentation/simple_extractor.py --dataset 'lip' --model-restore storage/checkpoints-humanParsing/exp-schp-201908261155-lip.pth --input-dir storage/data/test-end2end/image --output-dir storage/data/test-end2end/image-parse"
    subprocess.call(cmd1, shell=True)
    
    # download some test data
    cmd2 = "python dataset_neck_skin_correction.py"
    subprocess.call(cmd2, shell=True)
    
    shutil.rmtree('storage/data/test-end2end/image-parse-new/.ipynb_checkpoints')
    
    # download the ground-truth data
    cmd3 = "python body_binary_masking.py"
    subprocess.call(cmd3, shell=True)
    # clothes mask
    cmd4 = "python cloth_binary_masking.py"
    subprocess.call(cmd4, shell=True)
    #GMM
    cmd5 = "python test.py --name GMM --dataroot storage/data --stage GMM --workers 4 --datamode test-end2end --data_list test_end2end_pairs.txt --checkpoint storage/checkpoints-cpvton-plus/GMM/GMM/gmm_final.pth"
    subprocess.call(cmd5, shell=True)
    
    ## python test.py --name GMM --dataroot storage/data --stage GMM --workers 4 --datamode test-end2end --data_list test_end2end_pairs.txt --checkpoint storage/checkpoints-cpvton-plus/checkpoints/GMM/gmm_final.pth