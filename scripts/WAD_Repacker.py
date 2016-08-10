import os

print('##v010516##')

path = input('Укажите путь до папки с субфайлами: ')

if (path[0] == '"') or (path[0] == "'"):
	path = path[1:len(path)-1]

workfolder = os.getcwd()
##path = '/sf'
filelist = os.listdir(path)
wad = open('new_WAD.WAD', 'wb')
offset = 2048
counter0 = 0
for x in range(len(filelist)):
    ##print(counter0)
    subfile = open(path + '/' + 'wad_sf_' + str(x+1) + '.bin', 'rb')

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
