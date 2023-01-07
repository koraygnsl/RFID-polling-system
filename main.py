import csv
import serial
import datetime

today = datetime.date.today()
day = today.strftime("%b-%d-%Y")
day_str = "yoklama-" + day + ".csv"
print(day_str)

dosya = open(day_str, "a")
dosya.write("Ad, Tarih , Giris Saati, Cikis Saati")
dosya.close()

def rfid():
    ser = serial.Serial()
    ser.baudrate = 9600
    try:
        ser.port = 'COM3'
    except:
        ser.port = 'COM3'

    ser.open()
    RFID_Data = ser.readline()
    if RFID_Data:
        RFID_Data = RFID_Data.decode()  # Decode arduino Serial
        RFID_Data = RFID_Data.strip()  # Strip Arduino Data to remove string
        #RFID_Data = int(RFID_Data);  # Convert the Data to Int
        return (RFID_Data)


def yoklamayaYaz(name):
    #with open('yoklama.csv','r+') as f:
    with open(day_str, 'r+') as f:
        myDataList = f.readlines()
        nameList = []
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])

        if name not in nameList:
            now = datetime.datetime.now()
            dtString = now.strftime('%H.%M')
            global girissaati
            girissaati = dtString
            f.writelines(f'\n{name},{day},{dtString}')

        if name in nameList:
            now = datetime.datetime.now()
            dtString = now.strftime('%H.%M')
            f.writelines((f'\n{name},{day},{girissaati},{dtString}'))

def idKontrol():
    id = rfid()
    with open('kisiListesi.csv', 'r+') as s:
        csvFile = csv.reader(s)

        for lines in csvFile:
            if lines[0] == str(id):
                return (yoklamayaYaz(lines[1]))

while True:
    idKontrol()