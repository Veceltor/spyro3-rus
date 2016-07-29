fpath = input('Укажите путь к файлу SPEECH.STR: ')

if (fpath[0] == '"') or (fpath[0] == "'"):
	fpath = fpath[1:len(fpath)-1]

ifile = open(fpath, 'rb')
ofile = open('emptySPEECH.STR', 'wb')

emptysector = bytes.fromhex('00')*2048

sectorcount = int(len(ifile.read())/2352)

for x in range(sectorcount):
	ofile.write(emptysector)

ifile.close()
ofile.close()
print('ОК!')
