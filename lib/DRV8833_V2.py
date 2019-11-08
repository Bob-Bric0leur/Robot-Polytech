# Gestion des moteurs CC à l'aide du double pont en H DRV8833
# Validé le 12.09.2018 : DRV8833.py
# Modifications le 18.03.2019 : DRV8833_V2.py
# Validé le 02.04.2019

from micropython import const
from machine import Pin
from machine import PWM
import time

# Définition sens de rotation des moteurs
SENS_HORAIRE = const(1)
SENS_ANTI_HORAIRE = const(2)

# Définition des moteur droit et gauche
MOTEUR_DROIT_Flag = 1
MOTEUR_GAUCHE_Flag = 2

VITESSE_MAX = 1.78 # Vitesse de rotation max en tours par seconde

class DRV8833_V2 :
    def __init__  (self, In1_pin, In2_pin, sleep_pin, timer_number, freq, num_channel_pwm_In1, num_channel_pwm_In2, moteur_dg, **kwargs) :
        # IN1_pin : entrée PWM 1 DRV8833
        # IN2_pin : entrée PWM 2 DRV8833
        # sleep_pin : SLP pin pour désactiver les ponts en H du DRV8833
        # timer_number : dans [0,1,2,3]. Choix du timer utilisé pour générer le signal pwm
        # freq : fréquence du signal pwm
        # num_channel_pwm_In1 : numéro de l'Id du canal PWM associé à la broche In1_pin
        # num_channel_pwm_In2 : numéro de l'Id du canal PWM associé à la broche In2_pin
        # moteur_dg : permet de différencier le moteur droit du moteur gauche

        self.DRV883_Sleep_Pin = Pin(sleep_pin, mode = Pin.OUT) # Initialiser la broche sleep_pin pour gérer le DRV8833
        self.DRV883_Sleep_Pin.value(0) # Désactive le driver DRV8833
        if timer_number not in [0,1,2,3] :
            raise ValueError(
                'Unexpected timer_number value {0}.'.format(timer_number))
        self.pwm = PWM(timer_number, frequency = freq) # Utiliser le timer n° timer_number en PWM avec une fréquence de base de freq Hz
        self.DRV8833_Pwm_In1 = self.pwm.channel(num_channel_pwm_In1, pin = In1_pin, duty_cycle = 0.0)
        self.DRV8833_Pwm_In2 = self.pwm.channel(num_channel_pwm_In2, pin = In2_pin, duty_cycle = 0.0)
        self.consigne_rotation_roue = 0.0
        self.sens = SENS_HORAIRE
        self.moteur_dg = moteur_dg
        time.sleep(0.05)
#---------------------------------------------------------------------------
# Commande d'un moteur :
# paramètres :
#   sens  : sens de rotation
#   consigne_rotation_roue : en tours par seconde

    def Cmde_moteur (self, sens, consigne_rotation_roue) :
        self.DRV883_Sleep_Pin.value(0) # Désactive le driver DRV8833
        self.sens = sens
        if consigne_rotation_roue < 0.0 :
            self.consigne_rotation_roue = 0.0
        elif consigne_rotation_roue > VITESSE_MAX :
            self.consigne_rotation_roue = VITESSE_MAX
        else :
            self.consigne_rotation_roue = consigne_rotation_roue
        consigne_pwm_moteur = self.ToursParSeconde_vers_PWM (self.consigne_rotation_roue)
        self.DRV883_Sleep_Pin.value(1) # Activer le driver DRV8833.value(1) # Activer le driver DRV8833
        if self.sens == SENS_HORAIRE : # forward
            self.DRV8833_Pwm_In1.duty_cycle(consigne_pwm_moteur) # Rapport cyclique à vitesse % sur IN1
            self.DRV8833_Pwm_In2.duty_cycle(0.0) # Rapport cyclique à 0.0 sur IN2 (soit 0%)
            time.sleep (0.005)
        elif self.sens == SENS_ANTI_HORAIRE : # reverse
            self.DRV8833_Pwm_In1.duty_cycle(0.0) # Rapport cyclique à 0.0 sur IN1
            self.DRV8833_Pwm_In2.duty_cycle(consigne_pwm_moteur) # Rapport cyclique à vitesse % sur IN2
            time.sleep (0.005)
#---------------------------------------------------------------------------
# Définitions des mouvements de base de la plateforme robotique
    def Arret_moteur (self) :
        self.DRV883_Sleep_Pin.value(1) # Activer le driver DRV8833
        self.DRV8833_Pwm_In1.duty_cycle(0.0) # Rapport cyclique à 0.0 sur IN1
        self.DRV8833_Pwm_In2.duty_cycle(0.0) # Rapport cyclique à 0.0 sur IN2
        self.DRV883_Sleep_Pin.value(0) # Désactive le driver DRV8833
#---------------------------------------------------------------------------
    @staticmethod
    def ToursParSeconde_vers_PWM (consigne_rotation_roue) :
        # Permet de calculer le rapport cyclique de la PWM de commande d'un moteur
        # en fonction de la vitesse de rotation de la roue
        # consigne_rotation_roue dans [0.0 ; 1.78] tours/s
        # Valeur retournée : rapport cyclique dans [0.0 ; 1.0]
        # Interpolation polynomiale : y = ax^6+bx^5+cx^4+dx^3+ex^2+fx+g avec :
        #    a = -0.2903
        #    b = 1.9281
        #    c = -4.6062
        #    d = 5.2432
        #    e = -2.8844
        #    f = 0.8839
        #    g = 0.0611
        # Validé le 06.03.2019
        coeff = (-0.2903, 1.9281, -4.6062, 5.2432, -2.8844, 0.8839, 0.0611)

        y = consigne_rotation_roue * coeff[0] + coeff[1]
        for i in range (1, 6) :
            y = consigne_rotation_roue * y + coeff[i+1]
        return y
#------------------------------------------------------------------------
