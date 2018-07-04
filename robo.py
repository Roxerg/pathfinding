import random
import pygame
import sys
import time
import serial


kryptis = 100


""" 

reiktu viska perrasyti kad butu tvarkingai.
funkcijos ima daugiau argumentu nei joms reikia nes jos naudoja kitas funkcijas 
kurias idejau velai. 


"""







#["North", "East", "South", "West"]
# grazina krypti i kuria yra siena arba 100 jeigu sienos nera 
# taip pat atsizvelgia i finiso blokeli
# siena tikrinama tik pagal tai ar koordinates neisleinda uz ribu

def tikrintisiena(x, y, xx, yy, width, height):

    # tikrina ar koordinate kurioje ieskoma siena nera isejimas
    comparex = y != yy
    comparey = x != xx

    # grazina kuria kryptimi yra siena. jei sienos nera, grazina 100
    if (x > width-2 and comparex):
        return 1
    if (x < 1 and comparex):
        return 3
    if (y > height-2 and comparey):
        return 2
    if (y < 1 and comparey):
        return 0
    return 100

#kryptys = ["North", "East", "South", "West"]
def rastikrypti(screen, x, y, xa, ya):
    n = 100
    if (xa > x):
        n = 1
    elif (xa < x):
        n = 3
    elif (y < ya):
        n = 2
    elif (y > ya):
        n = 0
    else:
        n = 100
    drawdirection(screen, n, x, y)
    return n

# patobulinta su sienos tikrinimu. jei siena sutinkama, einama per kitas imanomas kryptis (kurios vis dar naudingos)
# kol randama neblokuojama kryptis.

def rastisukima(kryptis, x, y, xx, yy, width, height):
    if (x < xx and tikrintisiena(x+1, y, xx, yy, width, height) != 1):
        return 1
    elif (x > xx and tikrintisiena(x-1, y, xx, yy, width, height) != 3):
        return 3
    elif (y < yy and tikrintisiena(x, y+1, xx, yy, width, height) != 2):
        return 2
    elif (y > yy and tikrintisiena(x, y-1, xx, yy, width, height) != 0):
        return 0


# pasirenka i kuria puse sukti, kad atliktu kuo maziau posukiu
# cia visa priezastis del kurios kryptys yra sarase.

def sukti(kryptis, x, y, xx, yy, screen, width, height):
    reikia = rastisukima(kryptis, x, y, xx, yy, width, height)

    # jei sukantis i viena puse uztenka vieno judesio, o i kita reikia suktis tris kartus
    # si dalis pasirenka viena pasisukima
    if (kryptis != reikia):
        if (abs(reikia-kryptis)==3):
            if (reikia>kryptis):
                print ('i kaire')
                ser.write('l')
            else:
                print ("i desine")
                ser.write('r')
            kryptis, reikia = reikia, kryptis
            return kryptis

        # o cia visi kiti atvejai - jei reikia 1, 2 posukiu, sie parenka geriausia kelia
        elif (reikia > kryptis):
            print ("i desine")
            ser.write('r')
            return kryptis+1
        elif (reikia < kryptis):
            print ("i kaire")
            ser.write('l')
            return kryptis-1
    else:
        # jei jau pasisukta teisinga kryptimi, nesisukame
        return kryptis

#kryptys = ["North", "East", "South", "West"]
# judina robotuka i leidziama koordinate artejant prie tikslo
def eiti(kryptis, x, y, xx, yy, screen, width, height):
    reikia = rastisukima(kryptis,x, y, xx, yy, width, height)
    
    if (kryptis == reikia):
        ser.write('f')
        pygame.draw.rect(screen, (0, 0, 128), (x*64, y*64, 64, 64), 0)
        drawdirection(screen, kryptis, x, y)

        if (kryptis == 0 and 100 == tikrintisiena(x, y-1, xx, yy, width, height)):
            return x, y-1
        if (kryptis == 1 and 100 == tikrintisiena(x+1, y, xx, yy, width, height)):
            return x+1, y
        if (kryptis == 2 and 100 == tikrintisiena(x, y+1, xx, yy, width, height)):
            return x, y+1
        if (kryptis == 3 and 100 == tikrintisiena(x-1, y, xx, yy, width, height)):
            return x-1, y
        else:
            return x, y
    else:
        return x, y


#["North", "East", "South", "West"]

# vizualizacijai skirtas kodas.
# nupiesia i kuria puse pasisukes robotukas kiekvienu momentu
def drawdirection(screen, n, x, y):
    if (n==0):
        pygame.draw.lines(screen, (0, 0, 0), False, [(0+64*x, 64+64*y), (32+64*x, 64*y), (64+64*x, 64+64*y), 3])
    if (n==1):
        pygame.draw.lines(screen, (0, 0, 0), False, [(0+64*x, 0+64*y), (64+64*x, 32+64*y), (0+64*x, 64+64*y), 3])
    if (n==2):
        pygame.draw.lines(screen, (0, 0, 0), False, [(0+64*x, 0+64*y), (32+64*x, 64+64*y), (64+64*x, 0+64*y), 3])
    if (n==3):
        pygame.draw.lines(screen, (0, 0, 0), False, [(64+64*x, 0+64*y), (0+64*x, 32+64*y), (64+64*x, 64+64*y), 3])
    pygame.display.update()



def gauti_langeli():
    global ser

    langelis = ser.readline().strip().decode()

   # langelis = eilute.split()[3]

    return int(langelis[0]), int(langelis[1])




# pagr. funkcija. 
# galima reguliuoti width ir height jei norit didesnio laukelio 
# finish parenka kurioje vietoje bus .. na... finisas.
# finish gali buti: 1, 2, 3, 4
def main(width=5, height=5, finish=3):
    global ser

    # viskas paruosiama vizualizacijai.
    # jei pakeistumem vietas kur yra 64 su tiesiog kintamuoju
    # butu galima keisti langeliu matmenis labai lengvai.
    # tada butu galima padaryti koki 100x100 dalyka
    # bet butu nuobodu nes kliutys tik sonuose.
    
    pygame.init()
    screen = pygame.display.set_mode((width*64, height*64))
    screen.fill((255, 255, 255))

    for i in range(1, width):
        pygame.draw.lines(screen, (0,0,0), False, [(0, 64*i), (64*width, 64*i)], 1)
    for i in range(1, height):
        pygame.draw.lines(screen, (0,0,0), False, [(64*i, 0), (64*i, 64*height)], 1)

    pygame.draw.rect(screen, (0, 0, 0), (0, 0, width*64, 64), 0)
    pygame.draw.rect(screen, (0, 0, 0), (0, (height-1)*64, width*64, 64), 0)
    pygame.draw.rect(screen, (0, 0, 0), (0, 0, 64, height*64), 0)
    pygame.draw.rect(screen, (0, 0, 0), (64*(width-1), 0, 64, 64*height), 0)

    """
    pygame.draw.lines(screen, (0,0,0), False, [(0, 64), (320, 64)], 1)
    pygame.draw.lines(screen, (0,0,0), False, [(0, 128), (320, 128)], 1)
    pygame.draw.lines(screen, (0,0,0), False, [(0, 192), (320, 192)], 1)
    pygame.draw.lines(screen, (0,0,0), False, [(0, 256), (320, 256)], 1)

    pygame.draw.lines(screen, (0,0,0), False, [(64, 0), (64, 320)], 1)
    pygame.draw.lines(screen, (0,0,0), False, [(128, 0), (128, 320)], 1)
    pygame.draw.lines(screen, (0,0,0), False, [(192, 0), (192, 320)], 1)
    pygame.draw.lines(screen, (0,0,0), False, [(256, 0), (256, 320)], 1)
    """






    # pradines kordinates
    #x = random.randrange(1,width-2)
    #y = random.randrange(1,height-2)

    
    #liepiam atsiust spalva
    ser.write('s'.encode())

    buf = ser.read_all()

    try:
        x, y = gauti_langeli()
    except:
        print("exception")
    #nupiesia pradine vieta
    pygame.draw.rect(screen, (0, 255, 0), (x*64, y*64, 64, 64), 0)
    
    ser.write('f'.encode())
    
    time.sleep(3)

    ser.write('s'.encode())

    time.sleep(5)

    buf = ser.read_all()
    
    time.sleep(2)

    xa, ya = gauti_langeli()

    #tikslas
    xx = random.randrange(1,width-1)
    yy = random.randrange(1,height-1)
    
    # priskiria koordinates finisui.
    # jei finish parinktas neteisingai, anksciau esantis kodas finisa padeda belekur.
    if (finish == 1):
        xx = width/2
        yy = 0
    elif(finish == 2):
        xx = width/2
        yy = height-1
    elif (finish == 3):
        xx = width-1
        yy = height/2
    elif (finish == 4):
        xx = 0
        yy = height/2

    # nupiesia tiksla
    pygame.draw.rect(screen, (255, 0, 0), (xx*64, yy*64, 64, 64), 0)

    print(("({}, {}) ----> ({}, {})").format(x, y, xx, yy))

    # atsitiktinai parenka kuria koordinate pakeisti pirmo paejimo langeliui
    #which = random.choice(["x", "y"])
#
    #if (which == "x"):
    #    xa += random.choice([-1, 1])
    #else:
    #    ya += random.choice([-1, 1])

    # tikrinama ar pirmas zingsnis ne i siena
    # praktikoje jei galima matyti tik po savimi neimamona
    # (arba nesugalvoju) budo neieiti i siena bent kartais 
    # su pirmu zingsniu
    siena = tikrintisiena(xa,ya, xx, yy, width, height)
    if (siena == 100):
        kryptis = rastikrypti(screen, x, y, xa, ya)
        x = xa
        y = ya
    else:
        kryptis = siena

        


    

    pygame.draw.rect(screen, (0, 0, 255), (x*64, y*64, 64, 64), 0)

    kryptys = ["North", "East", "South", "West"]

    print(kryptis)
    print("kryptis: {}".format(kryptys[kryptis]))

    print("----")

    #pagrindinis "loopas". sleep naudojamas del vizualizacijos, kad butu matomas kiekvienas roboto daromas zingsnis.
    while (xx != x or yy != y):
        time.sleep(1) # pauze del vaizdo
        drawdirection(screen, kryptis, x, y) # nupiesiam kur robotas ziuri
        kryptis = sukti(kryptis, x, y, xx, yy, screen, width, height) # pasukama link tikslo jei nera pasisuke
        print("kryptis: {}".format(kryptys[kryptis])) # parasome kur pasisukome
        x, y = eiti(kryptis, x, y, xx, yy, screen, width, height) # judame jeigu esame pasisuke link tikslo
        drawdirection(screen, kryptis, x, y) # vel piesiame kur robotas ziuri
        print("x: {}, y: {}".format(x, y)) # parasome koordinates


    # del vizualizacijos palaukiam truputi kad butu galima paziureti i nueita kelia
    pygame.display.update()
    time.sleep(3)

    print("done!")


if __name__ == "__main__":
    ser = serial.Serial('COM9', baudrate=115200)
    # rekomenduojama max 20x20
    main(7, 7)
    ser.close()




#while(not ser.in_waiting()):
    #laukti kol gauni info is arduino

#square = ser.readline().strip().decode()  #cia mazdaug gauni 'A1' 'A2' ...

#dabar kai turiu start koordinates, reik vaziuot

#ser.write('r'.encode())

#laukiam atsakymo... duodam laiko arduino nuvaziuot ir atsiust naujo langelio RGB

# pradines kordinates
#x = 1 
#y = 1

#ser.write('r'.encode())
#ser.write('k'.encode())
#ser.write('k'.encode())
#ser.write('r'.encode())

#ser.write("rrslllrrr".encode())

ser.close()

