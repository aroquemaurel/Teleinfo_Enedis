#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Sébastien Reuiller"
# __licence__ = "Apache License 2.0"

# Python 3, prerequis : pip install pySerial influxdb
#
# Exemple de trame:
# {
#  'OPTARIF': 'HC..',        # option tarifaire
#  'IMAX': '007',            # intensité max
#  'HCHC': '040177099',      # index heure creuse en Wh
#  'IINST': '005',           # Intensité instantanée en A
#  'PAPP': '01289',          # puissance Apparente, en VA
#  'MOTDETAT': '000000',     # Mot d'état du compteur
#  'HHPHC': 'A',             # Horaire Heures Pleines Heures Creuses
#  'ISOUSC': '45',           # Intensité souscrite en A
#  'ADCO': '000000000000',   # Adresse du compteur
#  'HCHP': '035972694',      # index heure pleine en Wh
#  'PTEC': 'HP..'            # Période tarifaire en cours
# }


import serial
import logging
import time
import requests
from datetime import datetime
import models
from settings import Settings

# clés téléinfo
int_measure_keys = ['IMAX', 'HCHC', 'IINST', 'PAPP', 'ISOUSC', 'ADCO', 'HCHP']

# création du logguer
logging.basicConfig(filename='/var/log/teleinfo/releve.log', level=logging.INFO, format='%(asctime)s %(message)s')
logging.info("Teleinfo starting..")

def main():
    with serial.Serial(port='/dev/ttyAMA0', baudrate=1200, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE,
                       bytesize=serial.SEVENBITS, timeout=1) as ser:

        logging.info("Teleinfo is reading on /dev/ttyAMA0..")

        # boucle pour partir sur un début de trame
        line = ser.readline()
        while b'\x02' not in line:  # recherche du caractère de début de trame
            line = ser.readline()

        # lecture de la première ligne de la première trame
        line = ser.readline()

        consumption = None
        last_consumption = None
        while True:
            line_str = line.decode("utf-8")
            ar = line_str.split(" ")
            try:
                key = ar[0]
                if key == 'ADCO': # Begining of block 
                    if consumption is not None:
                        if last_consumption is None or not last_consumption.has_same_indexes(consumption) or (consumption.datetime - last_consumption.datetime).seconds > 30:
                            Settings.singleton().db.session.add(consumption)
                            Settings.singleton().db.session.commit()

                        last_consumption = consumption

                    consumption = models.Consumption()
                elif consumption is None:
                    logging.warning("We search the beginning of first trame")
                    line = ser.readline()
                    continue

                if key in int_measure_keys :
                    value = int(ar[1])
                else:
                    value = ar[1]

                checksum = ar[2]

                if key == 'HCHP':
                    consumption.index_hp = value
                elif key == 'HCHC':
                    consumption.index_hc = value
                elif key == 'IINST':
                    consumption.intensite_inst = value
                elif key == 'PAPP':
                    consumption.puissance_apparente = value
                elif key == 'PTEC':
                    if value == "HC..":
                        consumption.periode = 2

            except Exception as e:
                logging.error("Exception : %s" % e)

            line = ser.readline()
            

