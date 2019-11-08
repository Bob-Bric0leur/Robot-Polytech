# Implémation d'un correcteur PID
# Kp : coefficient proportionnel
# Ki : coefficient intégral
# Kd : coefficient dérivé
# Delta_T : période d'échantillonnage du correcteur en ms
# Encodeur_Mot : encodeurs associés aux moteurs pour la gestion du correcteur PID
# Moteur_Pont_H : associé au circuit pont en H utilisé pour piloter le moteur (ici le DRV8833)
# Validé le 02.04.2019

from machine import Timer
from ENCODEUR import RESOLUTION_CODEUR

class CORRECTEUR_PID () :

    def __init__ (self, Kp, Ki, Kd, Delta_T, Encodeur_Mot, Moteur_Pont_H) :
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.Delta_T = Delta_T
        self.Encodeur_Mot = Encodeur_Mot
        self.Moteur_Pont_H = Moteur_Pont_H

        self.ticks_voieA = 0 # Retour encodeur voie A
        self.ticks_voieB = 0 # Retour encodeur voie B
        self.somme_erreur = 0.0
        self.erreur_precedente = 0.0
        self.delta_erreur = 0.0
        self.consigne = 0.0 # Consigne initiale de vitesse de rotation du moteur

        self.alarm = Timer.Alarm(self.IT_Moteur_correcteur_pid, ms = self.Delta_T, periodic = True)
#------------------------------------------------------------------------
    def IT_Moteur_correcteur_pid(self, alarm) :
        # Récupérer les données des Encodeurs
        self.ticks_voieA = self.Encodeur_Mot.ticks_voieA_pid
        self.ticks_voieB = self.Encodeur_Mot.ticks_voieB_pid
        self.Encodeur_Mot.ticks_voieA_pid = 0
        self.Encodeur_Mot.ticks_voieB_pid = 0

        # Calculer la valeur de feddback
        feedback = ((self.ticks_voieA + self.ticks_voieB) / 2.0 / RESOLUTION_CODEUR / self.Delta_T) * 1000.0

        # Calculer la valeur de l'erreur
        erreur = self.consigne - feedback # Pour terme proportionnel
        self.somme_erreur += erreur # Pour théme intégral
        self.delta_erreur = erreur - self.erreur_precedente # Pour terme dérivé
        self.erreur_precedente = erreur

        # Calculer la valeur de la commande en tours par seconde
        commande = self.Kp * erreur + self.Ki * self.somme_erreur + self.Kd * self.delta_erreur

        # Envoyer la commande le moteur
        self.Moteur_Pont_H.Cmde_moteur(self.Moteur_Pont_H.sens, commande)
