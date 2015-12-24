print('##v181015##')

path = input('Путь до основного WAD: ')
wad = open(path, 'rb')
trigger0 = False

import configparser
import os
config = configparser.ConfigParser()
config.read('WADunpacker.ini')
config.read('configs/' + config['Settings']['Game'] + '_' + config['Settings']['Version'] + '.ini')

game = config['Settings']['ShortName']
sf_list = list()
ssf_list = list()

for x in range(len(config['LevelsList'])):
    sf_list.append(int(config['LevelsList'][str(x)]))
for x in range(len(config['LevelsList'])):
    ssf_list.append(int(config['LevelsList'][str(x)]))
sf_list.sort()
ssf_list.sort()

if not os.access('sf', os.F_OK, dir_fd=None, effective_ids=False, follow_symlinks=True):
     os.mkdir('sf', mode=0o777, dir_fd=None)

sf_number = 1
trigger0 = True
print('Распаковка субфайлов...')
for x in range(256):
    trigger0 = True
    wad.seek(8*x)
    bytes0 = wad.read(8)
    sf_offset = bytes0[0]+bytes0[1]*256+bytes0[2]*65536+bytes0[3]*16777216
    sf_size = bytes0[4]+bytes0[5]*256+bytes0[6]*65536+bytes0[7]*16777216
    if sf_offset == 0:
        ##print('Обнаружен промежуток в таблице адресов между субфайлом ' + str(sf_number-1) + ' и субфайлом ' + str(sf_number) + '.')
        trigger0 = False
    else:
        print('(' + str(sf_number) + ')' + 'Смещение субфайла - ' + str(sf_offset) + ', размер субфайла - ' + str(sf_size) + ' байт.')
    if trigger0:
        wad.seek(sf_offset)
        bytes0 = wad.read(sf_size)
        binary = open('sf/' + game + '_sf_' + str(sf_number) + '.bin', 'wb')
        binary.write(bytes0)
        binary.close()
        sf_number = sf_number+1

wad.close()
print('Распаковка субфайлов завершена.')

sf_number = sf_number-1
print('Всего субфайлов: ' + str(sf_number))
input('Нажмите ENTER, чтобы выйти...')
