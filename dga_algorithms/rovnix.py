__author__ = 'andrewa'
import datetime

usdeclar = open("../usdeclar.txt", 'r').read().strip().split()
for i in xrange(0, len(usdeclar)):
    usdeclar[i] = ''.join(e for e in usdeclar[i] if e.isalnum())


def getDate():
    dt = str(datetime.datetime.now()).split(' ')[0]
    dstash = dt.split('-')
    dd = dstash[2]
    mm = dstash[1]
    yyyy = dstash[0]
    return int(dd), int(mm), int(yyyy)


def generateSeed(a1, a2, a3):
    result = ''
    v4 = ''
    v5 = 0
    v6 = 0
    v7 = 0
    v8 = "1F1C1F1E1F1E1F1F1E1F1E1F"
    v8 = v8.decode("hex")
    result = 0
    if ( a1 > 0 ):
        if ( (a2 - 1) <= 0xB ):
            if ((a3 - 1) <= 0x1E ):
                v4 = (a1 & 0x80000003) == 0
                if ( (a1 & 0x80000003) < 0 ):
                    v4 = (((a1 & 0x80000003) - 1) | 0xFFFFFFFC) == -1
                if ( v4 ):
                    v8[11] = chr(0x1D)
                v5 = 0
                if ( a2 > 1 ):
                    v7 = v8
                    v6 = a2 - 1
                    i7 = 0
                    while (v6):
                        v5 += ord(v7[i7])
                        i7 += 1
                        v6 -= 1
                ecx = 365 * (a1 - (a1 / 4))
                eax = 366 * (a1 / 4)
                result = a3 + v5 + ecx + eax

    return result

day, month, year = getDate()
seed = generateSeed(year, month, day)
next_domain = 1
const1 = 0xDEAD
const2 = 0xBEEF


def generate_domain():
    domain = ''
    while len(domain) < 20:
        domain += choose_word(usdeclar)
    domain += '.com'
    return domain


def choose_word(word_list):
    global seed
    global next_domain
    global const1
    global const2
    seed = (((((((((((seed & 0xFFFF) * const1) & 0xFFFF) * getDate()[0]) & 0xFFFF) * const2) & 0xFFFF) * next_domain) &
              0xFFFF) ^ const1) & 0xFFFF)
    rem = seed % len(usdeclar)
    return usdeclar[rem]

for i in xrange(0, 100000):
    print generate_domain()
