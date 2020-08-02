from enum import Enum


class Keyword(Enum):
    ADCO = 1  # Identifiant du compteur
    OPTARIF = 2  # Option tarifaire (type d’abonnement)
    ISOUSC = 3  # Intensité souscrite
    BASE = 4  # Index si option = base (en Wh)
    HCHC = 5  # Index heures creuses si option = heures creuses (en Wh)
    HCHP = 6  # Index heures pleines si option = heures creuses (en Wh)
    EJP_HN = 7  # Index heures normales si option = EJP (en Wh)
    EJP_HPM = 8  # Index heures de pointe mobile si option = EJP (en Wh)
    BBR_HC_JB = 9  # Index heures creuses jours bleus si option = tempo (en Wh)
    BBR_HP_JB = 10  # Index heures pleines jours bleus si option = tempo (en Wh)
    BBR_HC_JW = 11  # Index heures creuses jours blancs si option = tempo (en Wh)
    BBR_HC_JR = 12  # Index heures creuses jours rouges si option = tempo  (en Wh)
    BBR_HP_JR = 13  # Index heures pleines jours rouges si option = tempo (en Wh)
    PEJP = 14  # Préavis EJP si option = EJP 30mn avant période EJP
    PTEC = 15  # Période tarifaire en cours
    DEMAIN = 16  # Couleur du lendemain si option = tempo
    IINST = 17  # Intensité instantanée (en ampères)
    ADPS = 18  # Avertissement de dépassement de puissance souscrite (en ampères)
    IMAX = 19  # Intensité maximale (en ampères)
    PAPP = 20  # Puissance apparente (en Volt.ampères)
    HHPHC = 21  # Groupe horaire si option = heures creuses ou tempo
    MOTDETAT = 22  # Mot d’état (autocontrôle)

    def name(self):
        return self._name_

    def is_int_value(self):
        # 'IMAX', 'HCHC', 'IINST', 'PAPP', 'ISOUSC', 'ADCO', 'HCHP'
        return self == Keyword.HCHC or \
               self == Keyword.HCHP or \
               self == Keyword.IINST or \
               self == Keyword.PAPP or \
               self == Keyword.ISOUSC or \
               self == Keyword.ADCO

    def is_unsupported_keyword(self):
        return "_" in self.name()

    @staticmethod
    def value_of(name):
        for keyword in Keyword:
            if keyword.name() == name:
                if keyword.is_unsupported_keyword():
                    raise Exception("Keyword with space are currently not supported")
                
                return keyword

        return None
