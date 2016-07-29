fpath = input('Укажите путь к файлу SPEECH.STR: ')
opath = input('Укажите путь к файлу образа диска (.BIN): ')

if (fpath[0] == '"') or (fpath[0] == "'"):
	fpath = fpath[1:len(fpath)-1]

if (opath[0] == '"') or (opath[0] == "'"):
	opath = opath[1:len(opath)-1]

ifile = open(fpath, 'rb')
tfile = open(opath, 'rb')

lba = int(input('File LBA: '))
filestart = lba*2352
sectorcount = int(len(ifile.read())/2352)

ifile.seek(0)
tfile.seek(0)

filedata = tfile.read()
tfile.close()

ofile = open(opath, 'wb')
ofile.seek(0)
ofile.write(filedata)
ofile.seek(filestart)
filedata = ifile.read()
ofile.write(filedata)


ifile.close()
ofile.close()
print('ОК!')
