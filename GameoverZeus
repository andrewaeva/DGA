import os, datetime, time, hashlib, socket

family = "GameoverZeus"
utility = family + "-DGA"
os.system("title " + utility)


def hasher(data, algorithm="md5"):
    h = hashlib.new(algorithm)
    h.update(data)
    return h.hexdigest()


def getDate():
    dt = str(datetime.datetime.now()).split(' ')[0]
    dstash = dt.split('-')
    dd = dstash[2]
    mm = dstash[1]
    yyyy = dstash[0]
    return int(dd), int(mm), int(yyyy)


def seeder(index, salt):
    ############
    edi = salt + index
    edx = 0
    ecx = 0x03E8
    eax = edi
    edx = eax % ecx
    eax = eax / ecx
    print "eax : %x edx : %x salt : %x" % (eax, edx, salt)
    day, month, year = getDate()
    h = hashlib.new("md5")
    dx = ("%08x" % socket.htonl(edx)).decode("hex")
    print "\tedx : " + dx.encode("hex")
    h.update(dx)
    y = ("%x" % socket.htons(year)).decode("hex")
    print "\tyear : " + y.encode("hex")
    h.update(y)
    s = ("%08x" % socket.htonl(salt)).decode("hex")
    print "\tsalt : " + s.encode("hex")
    h.update(s)
    m = ("%04x" % socket.htons(month)).decode("hex")
    print "\tmonth : " + m.encode("hex")
    h.update(m)
    print "\tsalt : " + s.encode("hex")
    h.update(s)
    d = ("%x" % socket.htons(day)).decode("hex")
    print "\tday : " + d.encode("hex")
    h.update(d)
    print "\tsalt : " + s.encode("hex")
    h.update(s)
    seed = h.hexdigest()
    return seed, edx


def generateDomain(hashlet):
    print "Generating domain"
    result = []
    print "Hashlet : %x" % hashlet
    #0042fef6:
    ##########
    ecx = hashlet
    ##########
    cl = 0
    dl = 0
    bl = 0
    eax = 0
    ebx = 0
    edx = 0
    esi = len(result)
    edi = 0

    while (ecx & 0xFFFFFFFF):
        eax = ecx
        edx = 0
        ecx = 0x24
        edx = eax % ecx
        eax = eax / ecx
        esp14 = eax
        dl = edx & 0xFF
        #print "eax: %x ecx : %x edx : %x ebx : %x dl : %x" % (eax,ecx,edx,ebx, dl)
        eax = edx + 0x30
        ebx = edx + 0x57
        al = eax & 0xFF
        bl = ebx & 0xFF
        ecx = al
        eax = bl
        if dl > 9:
            ecx = eax
        cl = ecx & 0xFF
        result.append(chr(cl))
        ecx = esp14
        #time.sleep(1)

    esi = len(result)
    eax = esi
    print "result : %s, esi : %x cl %x" % ( ''.join(result), esi, cl)
    result[esi - 1] = chr(cl)
    eax = eax - edi
    esi -= 1
    while edi < esi:
        cl = result[edi]
        dl = result[esi]
        print "\tesi: %x edi : %x cl : %s dl : %s result  :%s" % (esi, edi, cl, dl, ''.join(result))
        result[esi] = cl
        esi -= 1
        result[edi] = dl
        edi += 1
    return ''.join(result)


def engine(salt=0x35190501, maxiter=1000):
    domains = []
    #salt = 0x35190501
    #maxiter = 1000
    for i in range(maxiter):
        hashit, edx = seeder(i, salt)
        print "hashit : " + hashit
        hashstash = [int(hashit[:8], 16), int(hashit[8:16], 16), int(hashit[16:24], 16), int(hashit[24:], 16)]
        domain = ''
        if True:
        #while len(domain) < 0x10 :
            index = 0
            for hashlet in hashstash:
                print "Hashlet : %x" % hashlet
                domain += generateDomain(socket.htonl(hashlet) & 0xFFFFFFFF)
                print "\t[%d] Domain : %s" % (index, domain)
                index += 1
        print "[%d] Domain : %s\n" % (i, domain)
        #########################
        if (edx & 3 == 0):
            domain += ".\x63\x6F\x6D"
        elif (edx % 3 != 0 ):
            if (edx & 1 != 0):
                domain += ".\x6E\x65\x74"
            else:
                domain += ".\x62\x69\x7A"
        else:
            domain += ".\x6F\x72\x67"
            #########################
        domains.append(domain)
    return domains


index = 0
dt = str(datetime.datetime.now()).split(' ')[0]
domains = engine()
fp = open("gzdga_domains_" + dt + ".txt", "w")
for domain in domains:
    a = dt + " | %d | %s\n" % (index, domain)
    fp.write(a)
    print a
    index += 1
fp.close()