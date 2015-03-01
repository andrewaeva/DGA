import os, time



def tinbaDGA(idomain, seed):
    suffix = ".com"
    domains = []

    count = 100000
    eax = 0
    edx = 0
    for i in range(count):
        buf = ''
        esi = seed
        ecx = 0x10
        eax = 0
        edx = 0
        for s in range(len(seed)) :
            eax = ord(seed[s])
            edx += eax
        edi = idomain
        ecx = 0x0C
        d = 0
        while ( ecx > 0 ):
            al = eax & 0xFF
            dl = edx & 0xFF
            al = al + ord(idomain[d])
            al = al ^ dl
            al += ord(idomain[d+1])
            al = al & 0xFF
            eax = (eax & 0xFFFFFF00)+al
            edx = (edx & 0xFFFFFF00)+dl
            if al > 0x61 :
                if al < 0x7A :
                    eax = (eax & 0xFFFFFF00) +al
                    buf += chr(al)
                    d += 1
                    ecx -= 1
                    continue
            dl += 1
            dl = dl & 0xFF
            edx = (edx & 0xFFFFFF00)+dl
            
        domain = buf+suffix
        domains.append(domain)
        idomain = domain
    return domains        
                

def init():
    harddomain = "ssrgwnrmgrxe.com"
    seed = "oGkS3w3sGGOGG7oc"
    domains = tinbaDGA(harddomain, seed)
    index = 0
    fp = open("../tinba.txt", "w")
    for domain in domains:
        index += 1
        fp.write(domain + '\n')
    fp.close()
init()
