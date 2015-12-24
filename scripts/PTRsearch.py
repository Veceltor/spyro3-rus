
tpath = input('Table: ')

if not tpath == '':
    savefile = open('ptrscan.cfg', 'w', encoding = 'utf-8')
    savefile.write(tpath)
    savefile.close()
else:
    savefile = open('ptrscan.cfg', 'r', encoding = 'utf-8')
    tpath = str(savefile.read())
    savefile.close()

table = open(tpath, 'r', encoding = 'utf-8')

def nullifyFile(file_path):
    import os
    tfile = open(os.getcwd() + '\\' + file_path, 'w')
    tfile.close()

def textPointerScan(file_path, address):
    import os

    sfaddr = findsubfileaddr(file_path, 4)[0]
    
    sfile = open(os.getcwd() + '\\' + file_path, 'rb')
    sfile.seek(sfaddr+address-1)
    sbytes = sfile.read(2)
    if sbytes[0] == 0 and not sbytes[1] == 0:
        return True
    else:
        return False

def findsubfileaddr(file_path, subfile_num):
    import os
    ret_list = list()
    wad = open(file_path, 'rb')
    wad.seek((subfile_num-1)*8)
    bytes0 = wad.read(4)
    ret_list.append(bytes0[0] + bytes0[1]*256 + bytes0[2]*65536 + bytes0[3]*16777216)
    wad.seek((subfile_num-1)*8+4)
    bytes0 = wad.read(4)
    ret_list.append(ret_list[0] + bytes0[0] + bytes0[1]*256 + bytes0[2]*65536 + bytes0[3]*16777216)
    wad.close()
    return ret_list

def checkAddr(num, alist):
    ##print(alist)
    ctrigger = True
    for e in alist:
        if e == num:
            print('catch')
            ctrigger = False
    return ctrigger

def searchAddr(filepath, txt, addr_list):
    import os
    
    subfile = findsubfileaddr(os.getcwd() + '\\' + filepath, 4)
    ##print(txt)
    wad = open(os.getcwd() + '\\' + filepath, 'rb')
    wad.seek(subfile[0])
    flength = subfile[1] - subfile[0]
    llength = len(txt.encode())
    ##print(llength)
    addr = 0
    ptr_l = list()

    ##print(llength)
    
    for x in range(flength):
        wad.seek(subfile[0] + x)
        line0 = (wad.read(llength)).decode('cp1251', errors = 'ignore')
        if line0 == txt:
            if checkAddr(x, addr_list):
                addr = x
                break
        
    ptr_l.append(addr)
    
    if not addr == 0:
        for x in range(int(flength/4)):
            wad.seek(subfile[0] + x*4)
            bytes0 = wad.read(4)
            ptr0 = bytes0[0] + bytes0[1]*256 + bytes0[2]*65536 + bytes0[3]*16777216
            if ptr0 >= addr - 16 and ptr0 <= addr:
                ptr_l.append(ptr0)

    wad.close()
    return ptr_l

#------------------------------------------------

canRead = False

nullifyFile('ptr.txt')
ffile = open('ptr.csv', 'w', encoding = 'utf-8')
ffile.write('Субфайл,Адрес,Указатель,Номер строки\n')
ffile.close()

addr_list = list()

lcnt = 1

for line in table.readlines():
    ##print('.', end='')
    if canRead:
        rtrigger = True
        ccount = 0
        txtline = ''
        sf_num = ''
        for symbol in line:
            if symbol == '"':
                if rtrigger:
                    rtrigger = False
                else:
                    rtrigger = True
            if rtrigger:
                if symbol == ',':
                    ccount += 1
            if ccount == 4:
                if not symbol == '"':
                    txtline += symbol
            elif ccount == 1:
                if not symbol == ',':
                    sf_num += symbol

        txtline = txtline[1:len(txtline)]
        ofile = open('ptr.txt', 'a')
        ofile.write(txtline + '\n')
        
        asl = searchAddr('sf/S3GH_sf_' + sf_num + '.bin', txtline, addr_list)
        print(asl[0])
        if asl[0] > 0:
            addr_list.append(asl[0])
        else:
            print('testing...')
            txtline = txtline[0:20]
            asl = searchAddr('sf/S3GH_sf_' + sf_num + '.bin', txtline, addr_list)
            print(asl[0])
            if asl[0] > 0:
                addr_list.append(asl[0])

        p_result = 0
        if len(asl) > 2:
            for raddr in range(len(asl)-1):
                if textPointerScan('sf/S3GH_sf_' + sf_num + '.bin', asl[raddr+1]):
                    p_result = asl[raddr+1]
                    print('right pointer...')
        elif len(asl) == 2:
            p_result = asl[1]
        else:
            p_result = 0

        if p_result == 0:
            for entry in asl:
                ofile.write(str(entry) + '\n')
        else:
            ofile.write(str(asl[0])+ '\n')
            ofile.write(str(p_result)+ '\n')
            ffile = open('ptr.csv', 'a', encoding = 'utf-8')
            ffile.write(str(sf_num) + ',' + str(asl[0]) + ',' + str(p_result) + ',' + str(lcnt) + '\n')
            ffile.close()
        ofile.close()
        lcnt+=1
        
    canRead = True
