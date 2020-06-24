import os
from pprint import pprint
import shutil
import time
import subprocess
from humanfriendly import format_size

def elapsedTime(elapsedSeconds):
    elapsedMinutes = elapsedSeconds // 60

    leftOverSeconds = elapsedSeconds - (60 * elapsedMinutes)
    if leftOverSeconds < 10:
        secondsString = '0' + str(leftOverSeconds)
    else:
        secondsString = str(leftOverSeconds)

    return(str(elapsedMinutes) + ':' + secondsString + ' (minutes:seconds)')


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

def archiveMovie(archiveDir):
    print('- Currently in archive HDD - ')
    os.system('ls ' + '\\ '.join( str(archiveDir).split(' '))) #What's in destination HDD.

    newVideosDir = countFolders(archiveDir)
    fullpathVideosDir = os.path.join(archiveDir, newVideosDir)

    if not os.path.exists(fullpathVideosDir):
        os.makedirs(fullpathVideosDir)

    print()
    print(f'DVD number: {newVideosDir.split("_")[-1]}')
    print(f'New DVD location: {fullpathVideosDir}')
    print(f'Destination storage drive: {os.path.split(archiveDir)[-1]}')

    vidDir = '/media/fit/DVD Video Recording/VIDEO_TS' #Relevant files start with VTS, end in .VOB.

    if os.path.exists(vidDir):

        totalVidSizes = 0
        fileSizes = []
        pathsOnDVD = []
        for file in [i for i in os.listdir(vidDir)]:
            if file.startswith('VTS') and file.endswith('.VOB'):
                fullpath = os.path.join(vidDir, file)
                vidSize = os.path.getsize(fullpath)
                totalVidSizes = totalVidSizes + vidSize

                ogPath = os.path.join(vidDir, file)
                commandPath = '\\ '.join( str(ogPath).split(' '))
                pathsOnDVD.append(commandPath)

                fileSizes.append('\t' + f'{file}: {format_size(vidSize)}')


        print()
        print(f'Total size to copy: {format_size(totalVidSizes)}' )
        print(*fileSizes, sep='\n')

        print()
        print('Copying video files from DVD, this may take some time.')

        start = time.time()

        destinationCommandPath = '\\ '.join( str(fullpathVideosDir).split(' '))
        copyCommand = 'cp ' + ' '.join(pathsOnDVD) +  ' ' + destinationCommandPath
        print()
        print('Executing bash command below.')
        print(copyCommand)

        os.system(copyCommand) #Does the actual copying from DVD to external HDD.

        copyTime =  elapsedTime(round(time.time() - start))
        print()
        print(f'Elapsed time: {copyTime}')

        eject = 'eject /media/fit/DVD\ Video\ Recording'
        os.system(eject)
        print()
        print('Successfully completed')

    else:
        print('Could not find media. Check if there is a DVD in player.')

if __name__ == '__main__':
    print('Written using Ubuntu 18.04 and Python 3.6')
    print()
    
    archiveDir = '/media/fit/Home Movies'
    archiveMovie(archiveDir)
