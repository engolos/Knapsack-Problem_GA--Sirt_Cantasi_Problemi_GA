# coding=utf8
import math 
from matplotlib import pyplot as plt
from copy import deepcopy
import sys
f=open(sys.argv[1])
icerik=f.read()

degerler=list()    
esyadegerleri=list()
esyaagirliklari=list()
rastgelelistesi=list()
populasyon=list()
sayac=0
c=0
for satir in icerik.split('\n'):
    degerler.append(list(satir.split(';')))             #degerler=txt icerisinde
    c+=1
    if c==8:
        break
IND_SIZE=len(degerler)
print("input.txt'nin icerisi:",degerler)

for degisken in degerler[-1][0].split(','):             #elemanlarinn degerleri
    esyadegerleri.append(float(degisken))
esyasayisi=len(esyadegerleri)
print("Esya degerleri",esyadegerleri)
print("Esya sayisi:",esyasayisi)

for degisken in degerler[-2][0].split(','):             #elemanlarin agirliklari
    esyaagirliklari.append(float(degisken))
print("Esya Agırliklari",esyaagirliklari)

cantaboyutu=int(degerler[-3][0])
print("Canta Boyutu",cantaboyutu)

for i in degerler[0][0].split(','):                     #Rastgele listesini ayirma
    rastgelelistesi.append(float(i))
global rlistebuyuklugu
rlistebuyuklugu=len(rastgelelistesi)
print("Rastgele listesi eleman sayisi:",rlistebuyuklugu)

populasyonboyutu=int(degerler[1][0])

def rastgelecek():
    global sayac
    rastsayisi=rastgelelistesi[sayac%rlistebuyuklugu]
    sayac+=1
    return rastsayisi

def ebeveynolustur():
    global esyasayisi
    global esyaagirliklari
    global esyadegerleri
    global cantaboyutu
    ebeveyn=''
    l=0
    i=0
    deger=0
    deger2=0
    while i<int(populasyonboyutu):
        while l<esyasayisi:  
            if rastgelecek()<0.5:
                ebeveyn+='0'
            else:
                ebeveyn+='1'
                deger+=esyadegerleri[l]
                deger2+=esyaagirliklari[l]
            l+=1
        if deger2>cantaboyutu:
            deger=0
        populasyon.append((ebeveyn,deger))
        deger=0
        deger2=0
        ebeveyn=''
        i+=1
        l=0
    return populasyon
    #print("Populasyon boyutu",len(populasyon))
    #print("Populasyon",populasyon)
print("Ilk ebeveynler",ebeveynolustur())
#print("Populasyon",len(ebeveynolustur())


def ebeveynsecim(secimlistesi):
    global populasyon
    ebeveynler=list()
    #print("secimlistesi:",secimlistesi)
    for eleman in secimlistesi:
        ebeveynler.append(populasyon[eleman])
    ebeveynler.sort(key=lambda tup: tup[1])
    
    #print("Secilen Ebeveynler:",ebeveynler)
    secilenebeveyn=list()
    secilenebeveyn.append(ebeveynler[-1])
    #secilenebeveynler.append(ebeveynler[-2])
    #print("En buyuk fitness ebeveyn",secilenebeveyn)
    return secilenebeveyn

def turnuvasecim():
    konumlar=list()
    l=0
    while l<int(degerler[2][0]):
        konum=math.ceil(rastgelecek()*populasyonboyutu)-1
        konumlar.append(konum)
        l+=1    
    #print("Konumlar:",konumlar)
    return ebeveynsecim(konumlar)

def yenipopulasyon():
    global populasyonboyutu
    i=0
    yenipopulasyonlistesi=list()
    if populasyonboyutu%2==1:
        populasyonboyutu-=1
    while i<populasyonboyutu:
        a=turnuvasecim()[0][0]
        yenipopulasyonlistesi.append(a)
        i+=1
    #print("yenipopulasyonlistesi:",yenipopulasyonlistesi)
    #print("yenipopulasyonlistesi boyutu",len(yenipopulasyonlistesi))
    return yenipopulasyonlistesi

#yenipopulasyon()

def caprazlama():
    yeniList = list()
    children = list()
    yeniList=deepcopy(yenipopulasyon())
    
    # print("buraa",yeniList)
    # for i in range(len(yeniList)):
    #     print(i)
    #     print(yeniList[i])
    i=0
    while i<len(yeniList):
        caprazlamanoktasi=math.ceil(esyasayisi*rastgelecek())-1   #Burada da -1 koyduk
        p1=yeniList[i]
        #print("p1=",p1)
        p2=yeniList[i+1]
        #print("p2=",p2)
        c1=p1[:caprazlamanoktasi]+p2[caprazlamanoktasi:]
        c2=p2[:caprazlamanoktasi]+p1[caprazlamanoktasi:]
        children.extend([c1,c2])
        i+=2
        #children.append(c1,c2)
    #print("children",children)
    #print("c1",c1)
    #print("c2",c2)
    return children
        

def mutasyon():
    yedek=list()
    yeniListe=list()
    yeniListe=deepcopy(caprazlama())
    yedek=yeniListe
    # for i in range(len(yeniListe)):
    #     print("yeniliste:",yeniListe[i])
    #print(len(yeniListe))
    #yedek[0][7]='0'
    #print("yedek:",yedek[0][7])
    
    i=0
    while i<len(yeniListe):
        l=0
        while l<esyasayisi:
            secim=rastgelecek()
            if secim<float(degerler[3][0]):
                if yeniListe[i][l]=="0":
                    yedek[i]=yeniListe[i][:l]+"1"+yeniListe[i][l+1:]
                else:   
                    yedek[i]=yeniListe[i][:l]+"0"+yeniListe[i][l+1:]
            l+=1
        i+=1
    #print("mutasyon sonucu:",yedek)
    return yedek
def survivor():
   # print("Populasyon:",populasyon)
    global populasyon
    yedekpopulasyon=deepcopy(mutasyon())
    yenipopulasyon=list()
    #print("yeni pop:",yedekpopulasyon)

    l=0
    i=0
    deger=0
    deger2=0
    while i<int(populasyonboyutu):
        while l<esyasayisi:  
            if int(yedekpopulasyon[i][l])==1:
                deger+=esyadegerleri[l]
                deger2+=esyaagirliklari[l]
            l+=1
        if deger2>cantaboyutu:
            deger=0
        ebeveyn=yedekpopulasyon[i]
        yenipopulasyon.append((ebeveyn,deger))
        deger=0
        deger2=0 
        i+=1
        l=0
    #print("yeni Populasyonum:",yenipopulasyon)
    yeniliste=populasyon+yenipopulasyon

    #print("yenipop:",yeniliste)
    #print("Yeni liste uzunlugu:",len(yeniliste))
    yeniliste.sort(key=lambda tup: tup[1])
    #b=reversed(a)
    #print("ilk 30:",b[:30])
    #print("yeni listemm=",yeniliste)
    yeniliste.reverse()
    sonuc=yeniliste[:populasyonboyutu]
    #print("Survivor List:",sonuc)
    return sonuc
i=0
ortalamalist=list()
kucuklist=list()
buyuklist=list()
while i<int(degerler[4][0]):
    print("Generation: ",i)
    populasyon=survivor()
    print("Populasyon Son hali:",populasyon)
    yedek=list()
    yedek=deepcopy(populasyon)
    yedek.sort(key=lambda tup: tup[1])
    toplam=0
    for l in range(len(yedek)):
        toplam=toplam+yedek[l][1]
    ortalama=toplam/len(yedek)
    enbuyuk=yedek[-1][1]
    enkucuk=yedek[0][1]
    print("Ortalama Fitness:",ortalama)
    print("En Buyuk Fitness:",enbuyuk)
    print("En Kucukk Fitness:",enkucuk)
    ortalamalist.append(ortalama)
    kucuklist.append(enkucuk)
    buyuklist.append(enbuyuk)
    i+=1

plt.title("Engin YILMAZ")
plt.grid()
plt.scatter(range(0,int(degerler[4][0])),kucuklist,c="blue")
plt.scatter(range(0,int(degerler[4][0])),ortalamalist,c="red")
plt.scatter(range(0,int(degerler[4][0])),buyuklist,c="brown")
plt.plot(range(0,int(degerler[4][0])),kucuklist,c="blue")
plt.plot(range(0,int(degerler[4][0])),ortalamalist,c="red")
plt.plot(range(0,int(degerler[4][0])),buyuklist,c="brown")
plt.legend(["min","ortalama","max"])
plt.xlabel("Iterasyon")
plt.ylabel("Fitness")
plt.show()


f.close()
