import os
import configparser

config = configparser.ConfigParser()
config.read('WADunpacker.ini')
config.read('configs/' + config['Settings']['Game'] + '_' + config['Settings']['Version'] + '.ini')
game = config['Settings']['ShortName']

print('##v020215##')
workfolder = os.getcwd()
path = '/sf'
filelist = os.listdir(workfolder + path)
wad = open('WAD.WAD', 'wb')
offset = 2048
counter0 = 0
for x in range(len(filelist)):
    ##print(counter0)
    subfile = open(workfolder + path + '/' + game + '_sf_' + str(x+1) + '.bin', 'rb')

    bytes0 = subfile.read()
    sfsize = len(bytes0)
    ##print(sfsize)
    wad.seek(counter0*8)
    wad.write(offset.to_bytes(4, byteorder='little'))
    
    wad.seek(counter0*8+4)
    wad.write(sfsize.to_bytes(4, byteorder='little'))
    counter0 = counter0+1
    wad.seek(offset)
    wad.write(bytes0)
    offset = offset + sfsize
    subfile.close()
    
wad.close()
print('Создание WAD файла завершено!')
input('Нажмите ENTER чтобы выйти...')
