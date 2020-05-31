import os
from pprint import pprint

def getTitles():

    print('DVD Titles')
    dvdNum = input('DVD number >> ')
    newVideosDir = os.path.join((os.getcwd()), 'DVD_' + dvdNum)
    titles = os.path.join(newVideosDir, 'Titles.txt')

    if not os.path.exists(newVideosDir):
        os.makedirs(newVideosDir)
        with open(titles, 'w+') as f:
            pass


    #if  os.path.exists(fullpathVideosDir):
    #    if os.path.exists(titles):

    titleList = open(titles, 'r+').read().splitlines()


    titlesContents = []
    if len(titleList) == 0:
        print('Enter titles on the tag (q to continue)')
        with open(titles, 'w+') as f:
            titleCt = 0
            while True:
                titleCt += 1
                userTitleInput = input('Title ' + str(titleCt) +' >> ')

                if userTitleInput == 'q':
                    break
                else:
                    titlesContents.append(userTitleInput)
                    f.write(userTitleInput + '\n')
        return titlesContents

    else:
        return titleList


print(getTitles())
