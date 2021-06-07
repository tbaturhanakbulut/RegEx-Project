import re
import sys
a = open("calc.out","w")
def exitFunc():
    a.write("Dont Let Me Down")
    a.close()
    sys.exit()
f = open("calc.in")
yeniDegHolder=0
sonucDegHolder=0
lineCounter=0
anaDegHolder=0
vars= dict()
logicvars= dict()
arithvars=dict()
indices=[]
l=[]
keywords = {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'sifir', 'bir', 'iki', 'uc', 'dort', 'bes', 'alti', 'yedi', 'sekiz', 'dokuz', 'dogru', 'yanlis', '+', '-', '*', 'arti', 'eksi', 'carpi', 've', 'veya', '(', ')', 'ac-parantez', 'kapa-parantez', 'AnaDegiskenler', 'YeniDegiskenler', 'Sonuc', 'degeri', 'olsun', 'nokta'}
midL_sp=[]
lwithSpace=[]
atermPattern='(\d\.\d|\d|(((sifir)|(bir)|(iki)|(uc)|(dort)|(bes)|(alti)|(yedi)|(sekiz)|(dokuz))\s+(nokta)\s+((sifir)|(bir)|(iki)|(uc)|(dort)|(bes)|(alti)|(yedi)|(sekiz)|(dokuz))|(sifir)|(bir)|(iki)|(uc)|(dort)|(bes)|(alti)|(yedi)|(sekiz)|(dokuz)))'
logtermPattern='(dogru|yanlis)'
initPattern='[a-zA-Z0-9]{0,10}\s+(degeri)\s+(\d\.\d|\d|((sifir)|(bir)|(iki)|(uc)|(dort)|(bes)|(alti)|(yedi)|(sekiz)|(dokuz))|(((sifir)|(bir)|(iki)|(uc)|(dort)|(bes)|(alti)|(yedi)|(sekiz)|(dokuz))\s+(nokta)\s+((sifir)|(bir)|(iki)|(uc)|(dort)|(bes)|(alti)|(yedi)|(sekiz)|(dokuz)))|dogru|yanlis)\s+(olsun)'
midArithPatternParan: str='(?=(\(|\((ac-parantez)).*(\)|(kapa-parantez)))'
sonucController=False
for line in f:
    # temp2=[]
    line = line.rstrip("\n")
    lineCounter=lineCounter+1
    temp=re.findall('^[a-zA-Z0-9].*',line)
    temp2=re.findall('^[^a-zA-Z0-9]+\S',line)
    temp3=re.findall('^\s*\S.*',line)
    if(sonucController):
        lineCounter-=1
        if(temp3!=[]):
            lineCounter+=1
            l.append(temp3[0])
    if(temp!=[] and sonucController==False):
        l.append(temp[0])
    elif(temp==[] and sonucController==False):
        lineCounter-=1
    if(temp2!=[] and sonucController==False):
        lineCounter=lineCounter-1
    if (line == "Sonuc"):
        sonucController = True


if(lineCounter!=len(l)):
    exitFunc()
try:
    anaDegHolder=l.index("AnaDegiskenler")
    yeniDegHolder=l.index("YeniDegiskenler")
    sonucDegHolder=l.index("Sonuc")
except:
    exitFunc()
#INITSTATEMENT
#region

for i in range(anaDegHolder+1,yeniDegHolder):
    pattern=initPattern
    lineTemp = re.search(pattern, l[i])
    if(lineTemp==None or lineTemp[0]!=l[i]):
        exitFunc()
    # if(lineTemp!=[] and lineTemp[0]==l[i]):
    # print(lineTemp)


for i in range(anaDegHolder+1,yeniDegHolder):
    l_sp = l[i].split()
    #ilk degiskenlerin keyword olup olmadigini kontrol et.
    if(l_sp[0] in keywords):
        exitFunc()
    #dictionary ye yollama degiskenleri

    x = vars.get(l_sp[0])
    if(x!=None):
        exitFunc()
    vars[l_sp[0]]=l_sp[2:-1]
    if(l_sp[2:-1]==['yanlis'] or l_sp[2:-1]==['dogru']):
        logicvars[l_sp[0]] = l_sp[2:-1]
    else:
        arithvars[l_sp[0]] = l_sp[2:-1]
    #dictionary ye yollama bitti.
#endregion
#MIDSTATEMENT

for i in range(yeniDegHolder+1,sonucDegHolder):
    pattern='[a-zA-Z0-9]{0,10}\s+(degeri)\s+.+\s+(olsun)'
    lineTemp=re.search(pattern,l[i])
    if(lineTemp==None or lineTemp[0]!=l[i]):
        exitFunc()

for i in range(yeniDegHolder+1,sonucDegHolder):
    paranCounter=0
    midL_sp=l[i].split()
    temp_midL_sp=l[i].split()
    if(temp_midL_sp[0] in keywords):
        exitFunc()
    midL_sp.pop(len(midL_sp)-1)
    midL_sp.pop(0)
    midL_sp.pop(0)
    aritlogicBOOL = True
    for j in midL_sp:
        if (j == "dogru" or j == "yanlis" or j=="ve" or j=="veya"):
            aritlogicBOOL = False
        for k in logicvars:
            if (k == j):
                aritlogicBOOL = False
    if(aritlogicBOOL==True):
        m = arithvars.get(temp_midL_sp[0])
        if(m!=None):
            exitFunc()
        else:
            arithvars[temp_midL_sp[0]]=3
    else:
        m=logicvars.get(temp_midL_sp[0])
        if(m!=None):
            exitFunc()
        else:
            logicvars[temp_midL_sp[0]]="dogru"
    # print(logicvars)
    # print(arithvars)


    # ORTAK ALAN
    # parantez kontrol baslangic
    for j in range(len(midL_sp)):
        if (midL_sp[j] == "ac-parantez" or midL_sp[j] == "("):
            paranCounter += 1
        elif (midL_sp[j] == "kapa-parantez" or midL_sp[j] == ")"):
            paranCounter -= 1
        if (paranCounter < 0):
            exitFunc()
        # ()KONTROL
        if (midL_sp[j] == ")" or midL_sp[j] == "kapa-parantez"):
            if (midL_sp[j - 1] == "(" or midL_sp[j - 1] == "ac-parantez"):
                exitFunc()
        # ()KONTROL BITTI
    if (paranCounter != 0):
        exitFunc()
    # prantez kontrol bitis
    #ORTAK ALAN Bitti--------------
    if ("nokta" in midL_sp):
        try:
            try:
                while (True):
                    noktaIndex = midL_sp.index("nokta")
                    midL_sp[noktaIndex] = midL_sp[noktaIndex - 1] + " " + midL_sp[noktaIndex] + " " + midL_sp[
                        noktaIndex + 1]
                    midL_sp.pop(noktaIndex - 1)
                    midL_sp.pop(noktaIndex)
            except:
                pass
        except:
            exitFunc()

    if(aritlogicBOOL):
        for j in midL_sp:
            if(j!="ac-parantez" and j!="kapa-parantez" and j!="(" and j!=")" and j!="+" and j!="-" and j!="*" and j!="eksi" and j!="carpi" and j!="arti"):
                yeniDegTemp = re.search(atermPattern,j)
                if(yeniDegTemp==None or yeniDegTemp[0]!=j):
                    y=arithvars.get(j)
                    if(y==None):
                        exitFunc()
        #basta ve sonda + var mi kontrol
        if (midL_sp[0] == "+" or midL_sp[0] == "-" or midL_sp[0] == "*" or midL_sp[len(midL_sp) - 1] == "+" or midL_sp[len(midL_sp) - 1] == "-" or midL_sp[len(midL_sp) - 1] == "*"):
            exitFunc()
        if (midL_sp[0] == "arti" or midL_sp[0] == "eksi" or midL_sp[0] == "carpi" or midL_sp[len(midL_sp) - 1] == "arti" or midL_sp[len(midL_sp) - 1] == "eksi" or midL_sp[len(midL_sp) - 1] == "carpi"):
            exitFunc()
        #basta ve sonda + var mi kontrol bitti.
        for j in range(len(midL_sp)):
            # iki (+  +) su durumu engelleme ve ++ gelmesini engelleme
            if(midL_sp[j]=="+" or midL_sp[j]=="-" or midL_sp[j]=="*" or midL_sp[j]=="arti" or midL_sp[j]=="eksi" or midL_sp[j]=="carpi"):
                if(midL_sp[j-1]=="ac-parantez" or midL_sp[j-1]=="(" or midL_sp[j+1]=="kapa-parantez" or midL_sp[j+1]==")"):
                    exitFunc()
                if(midL_sp[j-1]=="+" or midL_sp[j+1]=="+" or midL_sp[j-1]=="-" or midL_sp[j+1]=="-" or midL_sp[j-1]=="*" or midL_sp[j+1]=="*" or midL_sp[j-1]=="arti" or midL_sp[j+1]=="arti" or midL_sp[j-1] =="eksi" or midL_sp[j+1]=="eksi" or midL_sp[j-1]=="carpi" or midL_sp[j+1]=="carpi"):
                    exitFunc()
            # iki (+ su durumu engelleme ve ++ gelmesini engelleme bitti
                # iki degisken yan yana mi?
            if (j >= 1):
                # iki degisken yan yana mi
                #bir degisken bir sayi yan yana mi
                if (midL_sp[j] in arithvars.keys()):
                    degiskenTemp5 = re.search(atermPattern, midL_sp[j - 1])
                    if (midL_sp[j - 1] in arithvars.keys()):
                        exitFunc()
                    elif (degiskenTemp5 != None and degiskenTemp5[0] == midL_sp[j - 1]):
                        exitFunc()
                    if (j < len(midL_sp) - 1):
                        degiskenTemp6 = re.search(atermPattern, midL_sp[j + 1])
                        if (degiskenTemp6 != None and degiskenTemp6[0] == midL_sp[j + 1]):
                            exitFunc()
                # iki sayi yan yana mi
                if (midL_sp[j] != "ac-parantez" and midL_sp[j] != "kapa-parantez" and midL_sp[j] != "(" and midL_sp[j] != ")" and midL_sp[j] != "+" and midL_sp[j] != "-" and midL_sp[j] != "*" and midL_sp[j] != "arti" and midL_sp[j] != "eksi" and midL_sp[j] != "carpi"):
                    degiskenTemp = re.search(atermPattern, midL_sp[j])
                    degisken2Temp = re.search(atermPattern, midL_sp[j - 1])
                    if (degiskenTemp != None and degiskenTemp[0] == midL_sp[j]):
                        if (degisken2Temp != None and degisken2Temp[0] == midL_sp[j - 1]):
                            exitFunc()
                # parantezin sagindakiler ve solundakiler kontrol
                if (midL_sp[j] == "(" or midL_sp[j] == "ac-parantez"):
                    degiskenTemp3 = re.search(atermPattern, midL_sp[j - 1])
                    if (degiskenTemp3 != None and degiskenTemp3[0] == midL_sp[j - 1]):
                        exitFunc()
                    elif (midL_sp[j - 1] in arithvars.keys()):
                        exitFunc()
                    elif (midL_sp[j - 1] == ")" or midL_sp[j - 1] == "kapa-parantez"):
                        exitFunc()
                    else:
                        pass
                elif (midL_sp[j] == ")" or midL_sp[j] == "kapa-parantez"):
                    if (j < len(midL_sp) - 1):
                        degiskenTemp4 = re.search(atermPattern, midL_sp[j + 1])
                        if (degiskenTemp4 != None and degiskenTemp4[0] == midL_sp[j + 1]):
                            exitFunc()
                        elif (midL_sp[j + 1] in arithvars.keys()):
                            exitFunc()
                        else:
                            pass
                # parantezin sagindakiler ve solundakiler kontrol bitis
    #LOGICPART --------------------------------------------------------------------------------------------------------

    elif(aritlogicBOOL==False):
        indexControl=0
        sideIndexControl=0
        tempSideIndexControl=0
        for j in midL_sp:
            #ARITHKONTROL
            arithDegTemp = re.search(atermPattern, j)
            if(j=="+" or j =="-" or j=="*" or j=="carpi" or j=="eksi" or j=="arti"):
                exitFunc()
            if(arithDegTemp!=None and arithDegTemp[0]==j):
                exitFunc()
            y=arithvars.get(j)
            if(y!=None):
                exitFunc()
            #ARITHKONTROL BITTI
            #ayni degiskeni degisterme kontrol
            if (j != "ac-parantez" and j != "kapa-parantez" and j != "(" and j != ")" and j != "ve" and j != "veya"):
                yeniDegTemp = re.search(logtermPattern, j)
                if (yeniDegTemp == None or yeniDegTemp[0] != j):
                    y = logicvars.get(j)
                    if (y == None):
                        exitFunc()
            # ayni degiskeni degistrieme Bitti kontrol
        #basta sonda ve veya vaar mi
        if(midL_sp[0]=="ve" or midL_sp[0]=="veya" or midL_sp[len(midL_sp)-1]=="ve" or midL_sp[len(midL_sp)-1]=="veya"):
            exitFunc()
        #basta sonda ve veya var mi bitti
        for j in range(len(midL_sp)):
            # iki (ve , ve)  durumlarini engelleme ve veya veya durumunu engelleme
            if(midL_sp[j]=="ve" or midL_sp[j]=="veya"):
                if (midL_sp[j - 1] == "ac-parantez" or midL_sp[j - 1] == "(" or midL_sp[j + 1] == "kapa-parantez" or midL_sp[j + 1] == ")"):
                    exitFunc()
                if(midL_sp[j-1]=="ve" or midL_sp[j+1]=="ve" or midL_sp[j-1]=="veya" or midL_sp[j+1]=="veya"):
                    exitFunc()
            # iki (ve ve) su durumu engelleme ve veya veya durumunu engelleme bitti
            #iki degisken yan yana mi?
            if (j >= 1):
                if (midL_sp[j] in logicvars.keys()):
                    degiskenTemp5 = re.search(logtermPattern, midL_sp[j - 1])
                    if (midL_sp[j - 1] in logicvars.keys()):
                        exitFunc()
                    elif (degiskenTemp5 != None and degiskenTemp5[0] == midL_sp[j - 1]):
                        exitFunc()
                    if (j < len(midL_sp) - 1):
                        degiskenTemp6 = re.search(logtermPattern, midL_sp[j + 1])
                        if (degiskenTemp6 != None and degiskenTemp6[0] == midL_sp[j + 1]):
                            exitFunc()
                if (midL_sp[j] != "ac-parantez" and midL_sp[j] != "kapa-parantez" and midL_sp[j] != "(" and midL_sp[j] != ")" and midL_sp[j] != "ve" and midL_sp[j] != "veya"):
                    degiskenTemp = re.search(logtermPattern, midL_sp[j])
                    degisken2Temp = re.search(logtermPattern, midL_sp[j - 1])
                    if (degiskenTemp != None and degiskenTemp[0] == midL_sp[j]):
                        if (degisken2Temp != None and degisken2Temp[0] == midL_sp[j - 1]):
                            exitFunc()
                #parantezin sagindakiler ve solundakiler kontrol
                if(midL_sp[j]=="(" or midL_sp[j]=="ac-parantez"):
                    degiskenTemp3 = re.search(logtermPattern, midL_sp[j-1])
                    if(degiskenTemp3!=None and degiskenTemp3[0]==midL_sp[j-1]):
                        exitFunc()
                    elif(midL_sp[j-1] in logicvars.keys()):
                        exitFunc()
                    elif(midL_sp[j-1]==")" or midL_sp[j-1]=="kapa-parantez"):
                        exitFunc()
                    else:
                        pass
                elif(midL_sp[j]==")" or midL_sp[j]=="kapa-parantez"):
                    if(j<len(midL_sp)-1):
                        degiskenTemp4=re.search(logtermPattern,midL_sp[j+1])
                        if(degiskenTemp4!=None and degiskenTemp4[0]==midL_sp[j+1]):
                            exitFunc()
                        elif(midL_sp[j+1] in logicvars.keys()):
                            exitFunc()
                        else:
                            pass
                #parantezin sagindakiler ve solundakiler kontrol bitis
#SONUC
for i in range(sonucDegHolder+1,len(l)):
    paranCounter = 0
    midL_sp = l[i].split()
    temp_midL_sp = l[i].split()
    aritlogicBOOL = True
    for j in midL_sp:
        if (j == "dogru" or j == "yanlis" or j == "ve" or j == "veya"):
            aritlogicBOOL = False
        for k in logicvars:
            if (k == j):
                aritlogicBOOL = False
    # ORTAK ALAN
    # parantez kontrol baslangic
    for j in range(len(midL_sp)):
        if (midL_sp[j] == "ac-parantez" or midL_sp[j] == "("):
            paranCounter += 1
        elif (midL_sp[j] == "kapa-parantez" or midL_sp[j] == ")"):
            paranCounter -= 1
        if (paranCounter < 0):
            exitFunc()
        # ()KONTROL
        if (midL_sp[j] == ")" or midL_sp[j] == "kapa-parantez"):
            if (midL_sp[j - 1] == "(" or midL_sp[j - 1] == "ac-parantez"):
                exitFunc()
        # ()KONTROL BITTI
    if (paranCounter != 0):
        exitFunc()
    # prantez kontrol bitis
    # ORTAK ALAN BITTTTTTTTTIIIIIIIIIIIII-------
    if ("nokta" in midL_sp):
        try:
            try:
                while (True):
                    noktaIndex = midL_sp.index("nokta")
                    midL_sp[noktaIndex] = midL_sp[noktaIndex - 1] + " " + midL_sp[noktaIndex] + " " + midL_sp[
                        noktaIndex + 1]
                    midL_sp.pop(noktaIndex - 1)
                    midL_sp.pop(noktaIndex)
            except:
                pass
        except:
            exitFunc()
    if (aritlogicBOOL):
        for j in midL_sp:
            if (j != "ac-parantez" and j != "kapa-parantez" and j != "(" and j != ")" and j != "+" and j != "-" and j != "*" and j != "eksi" and j != "carpi" and j != "arti"):
                yeniDegTemp = re.search(atermPattern, j)
                if (yeniDegTemp == None or yeniDegTemp[0] != j):
                    y = arithvars.get(j)
                    if (y == None):
                        exitFunc()
        # basta ve sonda + var mi kontrol
        if (midL_sp[0] == "+" or midL_sp[0] == "-" or midL_sp[0] == "*" or midL_sp[len(midL_sp) - 1] == "+" or midL_sp[
            len(midL_sp) - 1] == "-" or midL_sp[len(midL_sp) - 1] == "*"):
            exitFunc()
        if (midL_sp[0] == "arti" or midL_sp[0] == "eksi" or midL_sp[0] == "carpi" or midL_sp[
            len(midL_sp) - 1] == "arti" or midL_sp[len(midL_sp) - 1] == "eksi" or midL_sp[len(midL_sp) - 1] == "carpi"):
            exitFunc()
        # basta ve sonda + var mi kontrol bitti.
        for j in range(len(midL_sp)):

            # iki (+  +) su durumu engelleme ve ++ gelmesini engelleme
            if (midL_sp[j] == "+" or midL_sp[j] == "-" or midL_sp[j] == "*" or midL_sp[j] == "arti" or midL_sp[
                j] == "eksi" or midL_sp[j] == "carpi"):
                if (midL_sp[j - 1] == "ac-parantez" or midL_sp[j - 1] == "(" or midL_sp[j + 1] == "kapa-parantez" or
                        midL_sp[j + 1] == ")"):
                    exitFunc()
                if (midL_sp[j-1]=="+" or midL_sp[j+1]=="+" or midL_sp[j-1]=="-" or midL_sp[j+1]=="-" or midL_sp[j-1]=="*" or midL_sp[j+1]=="*" or midL_sp[j-1]=="arti" or midL_sp[j+1]=="arti" or midL_sp[j-1] =="eksi" or midL_sp[j+1]=="eksi" or midL_sp[j-1]=="carpi" or midL_sp[j+1]=="carpi"):
                    exitFunc()
            # iki (+ su durumu engelleme ve ++ gelmesini engelleme bitti
            if (j >= 1):
                #iki degisken yan yana mi
                #bir sayi bir degisken yan yana mi
                if (midL_sp[j] in arithvars.keys()):
                    degiskenTemp5 = re.search(atermPattern, midL_sp[j - 1])
                    if (midL_sp[j - 1] in arithvars.keys()):
                        exitFunc()
                    elif (degiskenTemp5 != None and degiskenTemp5[0] == midL_sp[j - 1]):
                        exitFunc()
                    if (j < len(midL_sp) - 1):
                        degiskenTemp6 = re.search(atermPattern, midL_sp[j + 1])
                        if (degiskenTemp6 != None and degiskenTemp6[0] == midL_sp[j + 1]):
                            exitFunc()
                #iki sayi yan yana mi
                if (midL_sp[j] != "ac-parantez" and midL_sp[j] != "kapa-parantez" and midL_sp[j] != "(" and midL_sp[j] != ")" and midL_sp[j] != "+" and midL_sp[j] != "-" and midL_sp[j] != "*" and midL_sp[j] != "arti" and midL_sp[j] != "eksi" and midL_sp[j] != "carpi"):
                    degiskenTemp = re.search(atermPattern, midL_sp[j])
                    degisken2Temp = re.search(atermPattern, midL_sp[j - 1])
                    if (degiskenTemp != None and degiskenTemp[0] == midL_sp[j]):
                        if (degisken2Temp != None and degisken2Temp[0] == midL_sp[j - 1]):
                            exitFunc()
                #parantezin sagindakiler ve solundakiler kontrol
                if(midL_sp[j]=="(" or midL_sp[j]=="ac-parantez"):
                    degiskenTemp3 = re.search(atermPattern, midL_sp[j-1])
                    if(degiskenTemp3!=None and degiskenTemp3[0]==midL_sp[j-1]):
                        exitFunc()
                    elif(midL_sp[j-1] in arithvars.keys()):
                        exitFunc()
                    elif(midL_sp[j-1]==")" or midL_sp[j-1]=="kapa-parantez"):
                        exitFunc()
                    else:
                        pass
                elif(midL_sp[j]==")" or midL_sp[j]=="kapa-parantez"):
                    if(j<len(midL_sp)-1):
                        degiskenTemp4=re.search(atermPattern,midL_sp[j+1])
                        if(degiskenTemp4!=None and degiskenTemp4[0]==midL_sp[j+1]):
                            exitFunc()
                        elif(midL_sp[j+1] in arithvars.keys()):
                            exitFunc()
                        else:
                            pass
                #parantezin sagindakiler ve solundakiler kontrol bitis





            # iki degisken yan yana gelemz

    # LOGICPART --------------------------------------------------------------------------------------------------------
    elif (aritlogicBOOL == False):
        for j in midL_sp:
            # ARITHKONTROL
            arithDegTemp = re.search(atermPattern, j)
            if (j == "+" or j == "-" or j == "*" or j == "carpi" or j == "eksi" or j == "arti"):
                exitFunc()
            if (arithDegTemp != None and arithDegTemp[0] == j):
                exitFunc()
            y = arithvars.get(j)
            if (y != None):
                exitFunc()
            # ARITHKONTROL Bitti
            # ayni degiskeni degisterme kontrol
            if (j != "ac-parantez" and j != "kapa-parantez" and j != "(" and j != ")" and j != "ve" and j != "veya"):
                yeniDegTemp = re.search(logtermPattern, j)
                if (yeniDegTemp == None or yeniDegTemp[0] != j):
                    y = logicvars.get(j)
                    if (y == None):
                        exitFunc()
            # ayni degiskeni degistrieme BITTI kontrol
        # basta sonda ve veya vaar mi
        if (midL_sp[0] == "ve" or midL_sp[0] == "veya" or midL_sp[len(midL_sp) - 1] == "ve" or midL_sp[
            len(midL_sp) - 1] == "veya"):
            exitFunc()
        # basta sonda ve veya var mi bitti
        # iki (ve , ve)  durumlarini engelleme ve veya veya durumunu engelleme
        for j in range(len(midL_sp)):
            if (midL_sp[j] == "ve" or midL_sp[j] == "veya"):
                if (midL_sp[j - 1] == "ac-parantez" or midL_sp[j - 1] == "(" or midL_sp[j + 1] == "kapa-parantez" or
                        midL_sp[j + 1] == ")"):
                    exitFunc()
                if (midL_sp[j - 1] == "ve" or midL_sp[j + 1] == "ve" or midL_sp[j - 1] == "veya" or midL_sp[
                    j + 1] == "veya"):
                    exitFunc()
        # iki (ve ve) su durumu engelleme ve veya veya durumunu engelleme bitti
            if (j >= 1):
                if (midL_sp[j] in logicvars.keys()):
                    degiskenTemp5=re.search(logtermPattern,midL_sp[j-1])
                    if (midL_sp[j - 1] in logicvars.keys()):
                        exitFunc()
                    elif(degiskenTemp5!=None and degiskenTemp5[0]==midL_sp[j-1]):
                        exitFunc()
                    if(j<len(midL_sp)-1):
                        degiskenTemp6 = re.search(logtermPattern, midL_sp[j + 1])
                        if(degiskenTemp6!=None and degiskenTemp6[0]==midL_sp[j+1]):
                            exitFunc()

                if (midL_sp[j] != "ac-parantez" and midL_sp[j] != "kapa-parantez" and midL_sp[j] != "(" and midL_sp[j] != ")" and midL_sp[j] != "ve" and midL_sp[j] != "veya"):
                    degiskenTemp = re.search(logtermPattern, midL_sp[j])
                    degisken2Temp = re.search(logtermPattern, midL_sp[j - 1])
                    if (degiskenTemp != None and degiskenTemp[0] == midL_sp[j]):
                        if (degisken2Temp != None and degisken2Temp[0] == midL_sp[j - 1]):
                            exitFunc()
                #parantezin sagindakiler ve solundakiler kontrol
                if(midL_sp[j]=="(" or midL_sp[j]=="ac-parantez"):
                    degiskenTemp3 = re.search(logtermPattern, midL_sp[j-1])
                    if(degiskenTemp3!=None and degiskenTemp3[0]==midL_sp[j-1]):
                        exitFunc()
                    elif(midL_sp[j-1] in logicvars.keys()):
                        exitFunc()
                    elif(midL_sp[j-1]==")" or midL_sp[j-1]=="kapa-parantez"):
                        exitFunc()
                    else:
                        pass
                elif(midL_sp[j]==")" or midL_sp[j]=="kapa-parantez"):
                    if(j<len(midL_sp)-1):
                        degiskenTemp4=re.search(logtermPattern,midL_sp[j+1])
                        if(degiskenTemp4!=None and degiskenTemp4[0]==midL_sp[j+1]):
                            exitFunc()
                        elif(midL_sp[j+1] in logicvars.keys()):
                            exitFunc()
                        else:
                            pass
                #parantezin sagindakiler ve solundakiler kontrol bitis

#degisken baslangici rakam olamaz full rakam da olamaz BUNU DUZELT ENSON
# soldaki ve sagdaki indexleri kontrol et

a.write("Here Comes The Sun")

a.close()