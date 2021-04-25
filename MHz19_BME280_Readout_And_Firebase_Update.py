#Import of required libraries
import mh_z19
import firebase_admin
from time import gmtime, strftime
from firebase_admin import credentials
from firebase_admin import db
import smbus2
import bme280

#Definition of ports
port = 1
address = 0x76
bus = smbus2.SMBus(port)
bme280.load_calibration_params(bus,address)

#Definition of Firebase RTDB credentials
cred = credentials.Certificate("Path to Firebase Credentials JSON")
firebase_admin.initialize_app(cred, {'databaseURL': 'URL of Firebase RTDB'})
ref = db.reference()

#Function to check MH-Z19 Co2 values
def avgCO2():
    #In my experience sometimes the values of the MH-Z19 and BME280 are not consisten. Thus we read out the sensor multiple times
    numberOfReadouts=8
    werteListe=[]
    while numberOfReadouts>0:
        readOut = mh_z19.read()
        formattedReadout = list(readOut.values())[0]
        werteListe.append(formattedReadout)
        numberOfReadouts = numberOfReadouts-1
    else :
        for v in range(2):
            werteListe.remove(max(werteListe))
            werteListe.remove(min(werteListe))
        ubergabeCO2= round((sum(werteListe) / len(werteListe)),2)
        return(ubergabeCO2)

#Function to check BME280 Temperature, Humidity and AirPressure values
def avgBME280():
    #In my experience sometimes the values of the MH-Z19 and BME280 are not consisten. Thus we read out the sensor multiple times
    numberOfReadouts=10
    listeTemp=[]
    listeHum=[]
    listePres=[]
    while numberOfReadouts>0:
        bmeData=bme280.sample(bus,address)
        listeTemp.append(bmeData.temperature)
        listeHum.append(bmeData.humidity)
        listePres.append(bmeData.pressure)
        numberOfReadouts = numberOfReadouts-1
    else:
        for x in range(3):
            listeTemp.remove(max(listeTemp))
            listeHum.remove(max(listeHum))
            listePres.remove(max(listePres))
            listeTemp.remove(min(listeTemp))
            listeHum.remove(min(listeHum))
            listePres.remove(min(listePres))
        ubergabeTemp =round((sum(listeTemp) / len(listeTemp)),2)
        ubergabeHum =round((sum(listeHum) / len(listeHum)),2)
        ubergabePres =round((sum(listePres) / len(listePres)),2)
        return ubergabeTemp, ubergabeHum, ubergabePres

#As a last step we call the functions
te, hu, pr = avgBME280()
co2 = avgCO2()
#And update the values in our Firebase RTDB
ref.update({'CO2': co2})
ref.update({'TempGarage2': te})
ref.update({'HumGarage2': hu})
ref.update({'AltGarage2': pr})