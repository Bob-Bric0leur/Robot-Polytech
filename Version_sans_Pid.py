from DRV8833_V2 import *
import ENCODEUR
from CORRECTEUR_PID import *
import time

DRV8833_Sleep_pin ='P20'#PinSLEEP

DRV8833_AIN1 ='P22'#EntreePWMmoteurgauche:AIN1
DRV8833_AIN2 ='P21'#EntreePWMmoteurgauche:AIN2

DRV8833_BIN1 = "P12"
DRV8833_BIN2 = "P19"

Moteur_Gauche = DRV8833_V2 ("P22", "P21", "P20" , 1, 500, 0, 1,
MOTEUR_GAUCHE_Flag )

Moteur_Droit = DRV8833_V2 ("P12", "P19", "P20", 1, 500, 2, 3,
MOTEUR_DROIT_Flag)
"""
Enco_droit = ENCODEUR.ENCODEUR("P18", "P11", Moteur_Droit)
Enco_gauche = ENCODEUR.ENCODEUR("P11", "P18", Moteur_Gauche)
Pid_Droit = CORRECTEUR_PID(1.85, 0.26, 0.0, 20, Enco_droit, Moteur_Droit)
Pid_Gauche = CORRECTEUR_PID(1.85, 0.26, 0.0, 20, Enco_gauche, Moteur_Gauche)
"""
def Avancer(i):
    Moteur_Gauche.Cmde_moteur(SENS_HORAIRE, i)
    Moteur_Droit.Cmde_moteur(SENS_HORAIRE, i)
    #Pid_Gauche.consigne = 0.2

def Reculer(i):
    Moteur_Gauche.Cmde_moteur(SENS_ANTI_HORAIRE, i)
    Moteur_Droit.Cmde_moteur(SENS_ANTI_HORAIRE, i)

def Pivoter_Droite(i):
    Moteur_Gauche.Cmde_moteur(SENS_HORAIRE, i)
    Moteur_Droit.Cmde_moteur(SENS_ANTI_HORAIRE, i)

def Pivoter_Gauche(i):
    Moteur_Gauche.Cmde_moteur(SENS_ANTI_HORAIRE, i)
    Moteur_Droit.Cmde_moteur(SENS_HORAIRE, i)

def Arret():
    Moteur_Gauche.Arret_moteur()
    Moteur_Droit.Arret_moteur()

Avancer(0.7)
time.sleep(1)
Reculer(0.5)
time.sleep(1)
Pivoter_Droite(0.7)
time.sleep(1)
Pivoter_Gauche(0.7)
time.sleep(1)
Arret()
