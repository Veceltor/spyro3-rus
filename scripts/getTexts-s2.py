import os
import struct
import string

es_addr = 0
path = os.getcwd() + '/sf/S2_sf_20.bin'

jumps = 9 ## 9/13
offset = 44 ## 44/48
level = 16 ## 16/17/98 (2/2J/3)
lastlevel = 72 ## 72/73/170 (2/2J/3)
tenc = 'cp1251' ##cp932 or 1251
g_errcount = 0

ptr_list = list()
dat_list = list()
ta_list = list()
tl_list = list()
ts_list = list()
txt_list = list()

nta_list = list()
ntxt_list = list()

if not os.access('txt', os.F_OK, dir_fd=None, effective_ids=False, follow_symlinks=True):
     os.mkdir('txt', mode=0o777, dir_fd=None)

def isUppercase(tSym):
    retVal = False
    compStr = string.ascii_uppercase
    for symbol in compStr:
        if tSym == symbol:
            
            retVal = True
    return retVal

def logger(wstr):
    ofile = open('txt/' + str(level) + '.txt', 'a')
    ofile.write(wstr+'\n')
    ofile.close()

def es3s(wad_path, sf):
    es_value = 0
    
    wad = open(wad_path, 'rb')
    wad.seek((sf-1)*8)
    print(wad_path)
    print((sf-1)*8)
    tmp = struct.unpack('<I', wad.read(4))[0]
    wad.seek(tmp)
    esTrigger = True
    escnt = 1
    while esTrigger:
        wad.seek(tmp-escnt)
        bytes7 = wad.read(1)
        if not bytes7[0] == 0:
            es_value = escnt-1
            esTrigger = False

        escnt += 1
        
    es_value = tmp-es_value
    es_ret = list()
    es_ret.append(es_value)
    es_ret.append(escnt-1)
    wad.close()
        	
    return es_ret

def symbolschanger(textline):
    import configparser
    config = configparser.ConfigParser()
    config.read('sc.ini', encoding = 'cp1251')
    txt = ''
    for symbol in textline:
        bytes0 = symbol.encode(encoding='cp1251', errors='ignore')
        try:
            txt = txt + (int(config['BYTES'][str(bytes0[0])]).to_bytes(1, byteorder='big')).decode(encoding='cp1251', errors='strict')
        except KeyError:
            txt = txt + symbol
    return txt

def getPointersAddr():
    vardat_list = list()
    varlen_list = list()
    
    wad = open(path, 'rb')
    wad.seek(8*3)
    bytes0 = wad.read(8)
    filestart = struct.unpack('<I', bytes0[0:4])[0]
    sf_size = struct.unpack('<I', bytes0[4:8])[0]
    jumpbuf = 0
    objlist = list()
    for n in range(jumps):
        wad.seek(filestart+offset+jumpbuf)
        bytes0 = wad.read(4)
        jumpbuf += struct.unpack('<I', bytes0)[0]

        if n == jumps-1:	
            rbuf = wad.read(4)
            objcount = struct.unpack('<I', rbuf)[0]
            objaddr = wad.tell()

    for x in range(objcount):
        wad.seek(objaddr+x*88)
        obuf = wad.read(88)
        varaddr = struct.unpack('<I', obuf[0:4])[0]
		
        wad.seek(filestart+varaddr)
        lbuf = wad.read(64)

        lentest = True

        if x < objcount-1:
            wad.seek(objaddr+(x+1)*88)
            obuf = wad.read(88)
            varaddr2 = struct.unpack('<I', obuf[0:4])[0]
            if (varaddr2 - varaddr) < 20:
                lentest = False
	
            if lentest:
                varlen_list.append(varaddr2 - varaddr)
                objlist.append(objaddr+x*88)

    ##print(objlist)
    rlist = list()
    for x in range(len(objlist)):
        wad.seek(objlist[x])
        obuf = wad.read(88)
        varaddr = struct.unpack('<I', obuf[0:4])[0]
        wad.seek(filestart+varaddr)
        lbuf = wad.read(256)
		
        onum = int((objlist[x]-objaddr)/88)
        lstart = struct.unpack('<I', lbuf[12:16])[0]
        if lstart > varaddr and lstart < sf_size:
            wad.seek(filestart+lstart)
            idbyte = wad.read(1)[0]
            etest = wad.read(1)
            wad.seek(filestart+lstart+1)
            if not idbyte == 255 and len(etest) == 1:
                lTrig = True
                lsize = 0
                while lTrig:
                    if etest[0] == 0:
                        lTrig = False
                    else:
                        lsize += 1
                    etest = wad.read(1)
					
                if lsize > 2:
                    ptr_list.append(varaddr+12)
                    ts_list.append(0)

        wad.seek(filestart+varaddr)
        llist = list()
        plist = list()
        errcount = 0

        varlen = varlen_list[x]
        
        for v in range(int(varlen/4)-4):
            lstart = struct.unpack('<I', lbuf[16+v*4:20+v*4])[0]
            errcount = 0
            if not lstart > varaddr:
                break
            elif not lstart < sf_size:
                break
            else:
                plist.append(varaddr+16+v*4)
                llist.append(lstart)	

        for tl in range(len(llist)):
            wad.seek(filestart+llist[tl])
            idbyte = wad.read(1)[0]
            if not idbyte == 255:
                txt = filestart+llist[tl]+idbyte
                wad.seek(txt)

                lTrig = True
                lsize = 0
                while lTrig:
                    if wad.read(1)[0] == 0:
                        lTrig = False
                    else:
                        lsize += 1

                wad.seek(txt)
                tbuf = wad.read(lsize)
                if (lsize > 2):
                    ptr_list.append(plist[tl])
                    ts_list.append(1)
    wad.close()

def getTexts():
          
    wad = open(path, 'rb')
    wad.seek(8*3)
    bytes0 = wad.read(8)
    filestart = struct.unpack('<I', bytes0[0:4])[0]
    sf_size = struct.unpack('<I', bytes0[4:8])[0]
    for t in range(len(ptr_list)):
        wad.seek(filestart+ptr_list[t])
        txtbuf = wad.read(4)
        lstart = struct.unpack('<I', txtbuf)[0]
        wad.seek(filestart+lstart)
        lTrig = True
        lsize = 0
        txtstart = filestart+lstart
        if ts_list[t] == 1:
            wad.seek(filestart+lstart)
            txtbuf = wad.read(1)
            txtstart = (filestart+lstart+txtbuf[0])
            wad.seek(filestart+lstart)
            txtbuf = wad.read(txtbuf[0])
            
        wad.seek(txtstart)
        while lTrig:
            if wad.read(1)[0] == 0:
                lTrig = False
            else:
                lsize += 1
        wad.seek(txtstart)
        etbuf = wad.read(lsize)
        
        dat_list.append(txtbuf)
        txt_list.append(etbuf.decode(tenc, 'ignore'))
        tl_list.append(lsize)
        ta_list.append(txtstart)
        
    wad.close()


def textFormatter(tfilepath):
    txtfile = open(tfilepath, 'a')

    namesList = list()

    charNum = 0
    
    for tf in range(len(ts_list)):
        if ts_list[tf] == 0:
            charNum += 1
            txtfile.write(str(charNum) + '] ' + txt_list[tf] + '\n')

    txtfile.write('\n')
    charNum = 0
    lineNum = 1
    for tf in range(len(ts_list)):
        if ts_list[tf] == 0:
            charNum += 1
            lineNum = 1
        elif ts_list[tf] == 1:
            txtfile.write(str(charNum) + '-' + str(lineNum) + '] ' + txt_list[tf] + '\n')
            lineNum += 1

    txtfile.close()

def additionalCleaning():
    ptr_l = list()
    dat_l = list()
    ta_l = list()
    tl_l = list()
    ts_l = list()
    txt_l = list()

    for cl in range (len(ptr_list)):
        ptr_l.append(ptr_list[cl])
        dat_l.append(dat_list[cl])
        ta_l.append(ta_list[cl])
        tl_l.append(tl_list[cl])
        ts_l.append(ts_list[cl])
        txt_l.append(txt_list[cl])

    for cl in range (len(ptr_list)):
        ptr_list.pop(0)
        dat_list.pop(0)
        ta_list.pop(0)
        tl_list.pop(0)
        ts_list.pop(0)
        txt_list.pop(0)

    wad = open(path, 'rb')
    wad.seek(8*3)
    bytes0 = wad.read(8)
    filestart = struct.unpack('<I', bytes0[0:4])[0]
    sf_size = struct.unpack('<I', bytes0[4:8])[0]
    for ac in range(len(ptr_l)):
        acTrig = False
        if not isUppercase((txt_l[ac])[0]):
            acTrig = True
            
        if not acTrig:
            ptr_list.append(ptr_l[ac])
            dat_list.append(dat_l[ac])
            ta_list.append(ta_l[ac])
            tl_list.append(tl_l[ac])
            ts_list.append(ts_l[ac])
            txt_list.append(txt_l[ac])

    wad.close()

##def getNewTexts():
##    continue
##
##def setNewText():
##    continue
##
##def setNewPointers():
##    continue
##
##def createNewLevelFile():
##    continue

for ml in range(int((lastlevel-level)/2)+1):
    path = os.getcwd() + '/sf/S2_sf_' + str(level) + '.bin'
    print(path)
    ptr_list = list()
    dat_list = list()
    ta_list = list()
    tl_list = list()
    ts_list = list()
    txt_list = list()
    getPointersAddr()
    getTexts()
    additionalCleaning()
    textFormatter(os.getcwd() + '/txt/' + str(level) + '.txt')
    level += 2
