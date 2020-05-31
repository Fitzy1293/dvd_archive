import os
from pprint import pprint
import shutil
import time
import subprocess

from humanfriendly import format_size


def countFolders(archiveDir):
    ct = 0
    for file in os.listdir(archiveDir):
        fullpath = os.path.join(archiveDir, file)
        if not '.' in file and not 'pycache' in file:
            ct += 1

            empty = True
            dvdFiles = [i for i in os.listdir(fullpath)]
            for i in dvdFiles:
                if i.endswith(('.mp4', '.VOB')) or 'pycache' in i:
                    empty = False
                    break
            if empty:
                ct += -1

    appropriateDir = 'DVD' + '_' + str(ct + 1)

    return appropriateDir


archiveDir = os.getcwd()

newVideosDir = countFolders(archiveDir)

fullpathVideosDir = os.path.join(archiveDir, newVideosDir)
if not os.path.exists(fullpathVideosDir):
    os.makedirs(fullpathVideosDir)

print(fullpathVideosDir)

#Stored in .VOB files, will change to .mp4 for file size.
vidDir = '/media/fit/DVD Video Recording/VIDEO_TS'


if os.path.exists(vidDir):

    start = time.time()



    filesInVidDir = [i for i in os.listdir(vidDir)]
    vidSizes = 0
    for file in filesInVidDir:
        if file.startswith('VTS') and file.endswith('.VOB'):
            fullpath = os.path.join(vidDir, file)
            vidSizes = vidSizes + os.path.getsize(fullpath)

    print('Video Size: ' + str(format_size(vidSizes)))

    print()
    print('Copying video files from DVD, this may take some time.')
    newVideoFullPaths = []
    for file in filesInVidDir:
        vidStart = time.time()
        fname = os.path.split(file)[-1]

        if fname.startswith('VTS') and fname.endswith('.VOB'):
            print()
            fullpath = os.path.join(vidDir, fname)
            newLocation = os.path.join(fullpathVideosDir, fname)
            newVideoFullPaths.append(newLocation)

            print('\tTransfering ' + str(fname))

            shutil.copyfile(fullpath, newLocation)



            #commandMP4 = f'./reduce.sh {newLocation} {newLocation.replace(".VOB", ".mp4")}'
            #subprocess.Popen(commandMP4, shell=True)
            #os.remove("output.mp4")


            timeVid =  f'{round( (time.time() - vidStart), 1) } seconds'
            print('\t' + timeVid)



    timeAllVids = f'Total transfer time: {round( (time.time() - start), 1) } seconds'
    print()
    print(timeAllVids)

else:
    print('Could not find media. Check if there is a DVD in player.')
