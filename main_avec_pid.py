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

Enco_droit = ENCODEUR.ENCODEUR("P18", "P11", Moteur_Droit)
Enco_gauche = ENCODEUR.ENCODEUR("P15", "P13", Moteur_Gauche)
Pid_Droit = CORRECTEUR_PID(1.85, 0.26, 0.0, 50, Enco_droit, Moteur_Droit)
Pid_Gauche = CORRECTEUR_PID(1.85, 0.26, 0.0, 50, Enco_gauche, Moteur_Gauche)




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




def test(d, i):
    while True:
        Arret()
        Avancer(i)
        time.sleep(d)
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
