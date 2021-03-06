import os
from pprint import pprint
import shutil
import time
import subprocess
from humanfriendly import format_size

def elapsedTime(elapsedSeconds): #I dunno why I made this.
    elapsedMinutes = elapsedSeconds // 60

    leftOverSeconds = elapsedSeconds - (60 * elapsedMinutes)
    if leftOverSeconds < 10:
        secondsString = '0' + str(leftOverSeconds)
    else:
        secondsString = str(leftOverSeconds)

    return(str(elapsedMinutes) + ':' + secondsString + ' (minutes:seconds)')


def countFolders(archiveDir): #Returns the correct folder in archiveDir.
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
    firstErrorFlag = True
    completed = False

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

    while not completed:

        if os.path.exists(vidDir):
            if not firstErrorFlag:
                print('DVD found - continuing program.')

            totalVidSizes = 0
            files = []
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

                    files.append(file)
                    fileSizes.append('\t' + f'{file}: {format_size(vidSize)}')

            print()
            print(f'Total size to copy: {format_size(totalVidSizes)}' )
            print(*fileSizes, sep='\n')

            print()
            print('Copying video files from DVD with, this may take some time.')

            start = time.time()
            destinationCommandPath = '\\ '.join( str(fullpathVideosDir).split(' '))
            copyCommand = 'cp -v ' + ' '.join(pathsOnDVD) +  ' ' + destinationCommandPath
            print()
            print(copyCommand)
            print()

            os.system(copyCommand) #Does the actual copying from DVD to external HDD.

            totalTime = round(time.time() - start)
            copyTime =  elapsedTime(totalTime)
            print()
            print(f'Copy time: {copyTime}')

            eject = 'eject /media/fit/DVD\ Video\ Recording'
            os.system(eject)

            MiBps = round( (totalVidSizes / 10**6) / totalTime, 2)

            print()
            print(f'Copying at: {MiBps} MiB/s')

            print()
            print('Successfully completed.')

            completed = True


        else:
            if firstErrorFlag:
                print()
                print('Could not find media. Check if there is a DVD in the player.')
                print()
                print('Program will wait until a DVD is inserted.')
                firstErrorFlag = False
            else:
                pass


if __name__ == '__main__':
    print('Written on Ubuntu 18.04 with Python 3.6')
    print()

    archiveDir = '/media/fit/Home Movies'

    archiveMovie(archiveDir)
