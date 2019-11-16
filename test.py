from DRV8833_V2 import *
import ENCODEUR
from BME280 import *
from CORRECTEUR_PID import *
from ODOMETRIE import *
from BME280 import *
from machine import I2C
from machine import SD
from machine import RTC
import os
import time

#Ini RTC (year, month, day[, hour[, minute[, second[, microsecond[, tzinfo]]]]])
Time_Rtc = RTC()
Time_Rtc.init((2019, 11, 16, 15, 14, 0, 0, 0))

#ini carte sd
sd = SD()
os.mount(sd, "/sd")


#ini BME280
bus_i2c = I2C()
bus_i2c.init(I2C.MASTER, baudrate = 400000)
print(bus_i2c.scan())

Id_BME280 = bus_i2c.readfrom_mem(BME280_I2C_ADR, BME280_CHIP_ID_ADDR, 1)
capteur_BME = BME280(BME280_I2C_ADR, bus_i2c)
capteur_BME.Calibration_Param_Load()


"""
for i in range(3):
    print(str(capteur_BME.read_temp())+"; "+str(capteur_BME.read_humidity())+"; "\
    +str(capteur_BME.read_pression())+"\r\n")
    f.write(str(capteur_BME.read_temp())+"; "+str(capteur_BME.read_humidity())+"; "\
    +str(capteur_BME.read_pression())+"\r\n")
    time.sleep(2)
"""


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
def Avancer(i):
    Moteur_Gauche.Cmde_moteur(SENS_HORAIRE, i)
    Moteur_Droit.Cmde_moteur(SENS_HORAIRE, i)
    Pid_Gauche.consigne = i
    Pid_Droit.consigne= i

def Reculer(i):
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
    return str(capteur_BME.read_temp())+';'+str(capteur_BME.read_humidity())+';'+str(capteur_BME.read_pression())




"""
def test(d, i):
    while True:
        Arret()
        Avancer(i)
        time.sleep(d)
        print(Odometrie.y_pos)
        Arret()
        Reculer(i)
        time.sleep(d)
        Arret()
        Pivoter_Droite(i)
        time.sleep(d)
        Arret()
        Pivoter_Gauche(i)
        time.sleep(d)
        Arret()
        time.sleep(d)

test(5, 0.2)
"""
