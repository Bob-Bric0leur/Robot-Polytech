from DRV8833_V2 import *
import ENCODEUR
from BME280 import *
from CORRECTEUR_PID import *
from ODOMETRIE import *
from BME280 import *
from machine import I2C
from machine import SD
from machine import RTC
from machine import Timer
from VL6180X import *
import os
import time
from math import pi
import _thread

#Ini RTC (year, month, day[, hour[, minute[, second[, microsecond[, tzinfo]]]]])
Time_Rtc = RTC()
Time_Rtc.init((2019, 11, 16, 15, 14, 0, 0, 0))


#ini carte sd
sd = SD()
os.mount(sd, "/sd")

f = open("/sd/test.csv", "w")
f.write("heure; minute; seconde; x; y ; angle; temperature; humidite; pression; luminosite; Distance;\r\n")
f.close()

#ini Bus I2c
bus_i2c = I2C()
bus_i2c.init(I2C.MASTER, baudrate = 400000)
print(bus_i2c.scan())

#Ini Bme280
Id_BME280 = bus_i2c.readfrom_mem(BME280_I2C_ADR, BME280_CHIP_ID_ADDR, 1)
capteur_BME = BME280(BME280_I2C_ADR, bus_i2c)
capteur_BME.Calibration_Param_Load()

#ini capteurs Distances
Distance = [-1, -1]
Luminosite = [-1.0, -1.0]

N_VL6180X = const(2)

VL6180X_CE_Pin = ('P6', 'P3')
VL6180X_I2C_adr_defaut = const(0x29)
VL6180X_I2C_Adr = (const(0x2A), const(0x2B))

VL6180X_GPIO_CE_Pin = []
for pin in VL6180X_CE_Pin :
    VL6180X_GPIO_CE_Pin.append(Pin(pin, mode=Pin.OUT))
    VL6180X_GPIO_CE_Pin[-1].value(0)

capteur_VL6180X = []

for i in range (N_VL6180X) :
    VL6180X_GPIO_CE_Pin[i].value(1)
    time.sleep(0.002)
    capteur_VL6180X.append(VL6180X(VL6180X_I2C_adr_defaut, bus_i2c))
    capteur_VL6180X[i].Modif_Adr_I2C(VL6180X_GPIO_CE_Pin[i], VL6180X_I2C_Adr[i], VL6180X_I2C_adr_defaut)


#Ini moteur
DRV8833_Sleep_pin ='P20'#PinSLEEP

DRV8833_AIN1 ='P22'#EntreePWMmoteurgauche:AIN1
DRV8833_AIN2 ='P21'#EntreePWMmoteurgauche:AIN2

DRV8833_BIN1 = "P12"
DRV8833_BIN2 = "P19"

Moteur_Gauche = DRV8833_V2 ("P22", "P21", "P20" , 1, 500, 0, 1,
MOTEUR_GAUCHE_Flag )

Moteur_Droit = DRV8833_V2 ("P12", "P19", "P20", 1, 500, 2, 3,
MOTEUR_DROIT_Flag)

#Ini encodeur
Enco_droit = ENCODEUR.ENCODEUR("P18", "P11", Moteur_Droit)
Enco_gauche = ENCODEUR.ENCODEUR("P15", "P13", Moteur_Gauche)

#Ini Pid
Pid_Droit = CORRECTEUR_PID(1.85, 0.26, 0.0, 50, Enco_droit, Moteur_Droit)
Pid_Gauche = CORRECTEUR_PID(1.85, 0.26, 0.0, 50, Enco_gauche, Moteur_Gauche)

#Ini Odometrie
Odometrie = ODOMETRIE(0.0, 0.0, 0.0, 15, Enco_droit, Enco_gauche)

#Def Fonction mouvement
def Reculer(i):
    Moteur_Gauche.Cmde_moteur(SENS_HORAIRE, i)
    Moteur_Droit.Cmde_moteur(SENS_HORAIRE, i)
    Pid_Gauche.consigne = i
    Pid_Droit.consigne= i

def Avancer(i):
    Moteur_Gauche.Cmde_moteur(SENS_ANTI_HORAIRE, i)
    Moteur_Droit.Cmde_moteur(SENS_ANTI_HORAIRE, i)
    Pid_Gauche.consigne = i
    Pid_Droit.consigne= i


def Pivoter_Droite(i):
    Moteur_Gauche.Cmde_moteur(SENS_HORAIRE, i)
    Moteur_Droit.Cmde_moteur(SENS_ANTI_HORAIRE, i)
    Pid_Gauche.consigne = i
    Pid_Droit.consigne= i


def Pivoter_Gauche(i):
    Moteur_Gauche.Cmde_moteur(SENS_ANTI_HORAIRE, i)
    Moteur_Droit.Cmde_moteur(SENS_HORAIRE, i)
    Pid_Gauche.consigne = i
    Pid_Droit.consigne= i


def Arret():
    Pid_Gauche.consigne = 0
    Pid_Droit.consigne= 0
    Moteur_Gauche.Arret_moteur()
    Moteur_Droit.Arret_moteur()

def Get_BME():
    return str(capteur_BME.read_temp())+';'+str(capteur_BME.read_humidity())+';'+str(capteur_BME.read_pression())+";"

def Get_Time():
    time = str(Time_Rtc.now()[3:6])
    return time[1:len(time)-1].replace(",", ";")+";"

def Get_Odo():
    return str(Odometrie.x_pos)+";"+str(Odometrie.y_pos)+";"+str(Odometrie.theta)+";"




def update_Distance():
    for i in range (N_VL6180X) :
        Distance[i] = capteur_VL6180X[i].range_mesure ()
        time.sleep(0.002)

def update_Luminosite():
    for i in range (N_VL6180X) :
        Luminosite[i] = capteur_VL6180X[i].ambiant_light_mesure ()
        time.sleep(0.002)


def Flag () :
    global test
    while True:
        test = True
        time.sleep(4)

_thread.start_new_thread(Flag, ())
time.sleep(0.4)



while True:

    if test  == True:
        Arret()
        update_Luminosite()
        update_Distance()
        test = False
        lumi = str(Luminosite).replace(";", ",")
        dist = str(Distance).replace(";", ",")
        f = open("/sd/test.csv", "a")
        f.write(Get_Time()+Get_Odo()+Get_BME()+lumi+";"+dist+"\r\n")
        f.close()

    update_Distance()



    if min(Distance) <= 100:
        Arret()
        Reculer(0.4)
        time.sleep(0.5)
        Pivoter_Droite(0.4)
        time.sleep(0.2)
        Arret()
    else:
        Arret()
        Avancer(0.5)
        time.sleep(0.2)
