# Gestion des encodeurs moteurs
# Définition des ressources associés à chaque Encodeurs
# Définition des modalités d'acquisition des données des Encodeurs
# Validé le 02.04.2019

from DRV8833_V2 import SENS_HORAIRE
from DRV8833_V2 import SENS_ANTI_HORAIRE
from DRV8833_V2 import MOTEUR_DROIT_Flag
from DRV8833_V2 import MOTEUR_GAUCHE_Flag
from micropython import const
from machine import Pin
from machine import Timer

# Enc_voieA_pin : broche de la carte WiPy qui reçoit les ticks de la voie A de l'encodeur
# Enc_voieB_pin : broche de la carte WiPy qui reçoit les ticks de la voie B de l'encodeur
# Pont_H_moteur : ressources du pont en H du DRV8833 associé au moteur
# Attributs :
# ticks_voieA : compteur de ticks voie A encodeur
# ticks_voieB: compteur de ticks voie B encodeur
# ticks_voieA_pid : compteur de ticks voie A encodeur pour correcteur pid
# ticks_voieB_pid : compteur de ticks voie B encodeur pour correcteur pid
# ticks_voieA_odometrie : compteur de ticks voie A encodeur pour odométrie
# ticks_voieB_odometrie : compteur de ticks voie B encodeur pour odométrie

RESOLUTION_CODEUR = const(1400) # Moteur : rapport de réduction 100:1
                                # Codeur : 14 ticks pour un tour d'arbre moteur
#---------------------------------------------------------------------------

class ENCODEUR :
    def __init__ (self, Enc_voieA_pin, Enc_voieB_pin, Pont_H_moteur) :

        # Affectation des broches des encodeurs
        self.Enc_voieA_pin = Enc_voieA_pin
        self.Enc_voieB_pin = Enc_voieB_pin
        self.Pont_H_moteur = Pont_H_moteur
        self.EncodeurA = Pin(self.Enc_voieA_pin, mode = Pin.IN, pull=Pin.PULL_UP)
        self.EncodeurB = Pin(self.Enc_voieB_pin, mode = Pin.IN, pull=Pin.PULL_UP)
        # Définition des modalités d'IT et d'appel des routines d'IT associées aux encodeurs
        self.EncodeurA.callback(Pin.IRQ_RISING | Pin.IRQ_FALLING, self.IT_EncodeurA) # Interruption sur fronts montant et descendant
        self.EncodeurB.callback(Pin.IRQ_RISING | Pin.IRQ_FALLING, self.IT_EncodeurB) # Interruption sur fronts montant et descendant

        self.ticks_voieA = 0
        self.ticks_voieB = 0
        self.ticks_voieA_pid = 0
        self.ticks_voieB_pid = 0
        self.ticks_voieA_odometrie = 0
        self.ticks_voieB_odometrie = 0

#---------------------------------------------------------------------------
# Fonction de gestion des encodeurs moteurs : gestion par IT
    def IT_EncodeurA (self, arg) :
        self.ticks_voieA +=1
        self.ticks_voieA_pid +=1
        if (self.Pont_H_moteur.sens == SENS_HORAIRE and self.Pont_H_moteur.moteur_dg == MOTEUR_DROIT_Flag) or (self.Pont_H_moteur.sens == SENS_ANTI_HORAIRE and self.Pont_H_moteur.moteur_dg == MOTEUR_GAUCHE_Flag) :
            self.ticks_voieA_odometrie += 1
        elif (self.Pont_H_moteur.sens == SENS_HORAIRE and self.Pont_H_moteur.moteur_dg == MOTEUR_GAUCHE_Flag) or (self.Pont_H_moteur.sens == SENS_ANTI_HORAIRE and self.Pont_H_moteur.moteur_dg == MOTEUR_DROIT_Flag) :
            self.ticks_voieA_odometrie -= 1

    def IT_EncodeurB (self, arg) :
        self.ticks_voieB +=1
        self.ticks_voieB_pid +=1
        if (self.Pont_H_moteur.sens == SENS_HORAIRE and self.Pont_H_moteur.moteur_dg == MOTEUR_DROIT_Flag) or (self.Pont_H_moteur.sens == SENS_ANTI_HORAIRE and self.Pont_H_moteur.moteur_dg == MOTEUR_GAUCHE_Flag) :
            self.ticks_voieB_odometrie += 1
        elif (self.Pont_H_moteur.sens == SENS_HORAIRE and self.Pont_H_moteur.moteur_dg == MOTEUR_GAUCHE_Flag) or (self.Pont_H_moteur.sens == SENS_ANTI_HORAIRE and self.Pont_H_moteur.moteur_dg == MOTEUR_DROIT_Flag) :
            self.ticks_voieB_odometrie -= 1
