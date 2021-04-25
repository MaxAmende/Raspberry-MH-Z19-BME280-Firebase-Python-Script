# Raspberry-MH-Z19-BME280-Firebase-Python-Script
Raspberry MH-Z19 BME280 Firebase Python Script

The script relies on three other projects:
@UedaTakeyuki‘s mh-z19 Python library https://github.com/UedaTakeyuki/mh-z19
@thijstriemstra bme280 library https://github.com/rm-hull/bme280
Google‘s Firebase Admin SDK for Python https://firebase.google.com/docs/admin/setup/#python

To run this script, follow the installation and cabling guides from the three different libraries, and add your Firebase credentials.
Be aware, you must run the Python script with admin rights.
On my Raspberries I did not implement the increase of Baud rate as proposed by thijstriemstra, but make sure that you activate I2C on your Raspberry.

For scheduled sensor read outs I propose to create a Crontab job.

ToDo:
Replace the current mh-z19 library with maintained alternative.
