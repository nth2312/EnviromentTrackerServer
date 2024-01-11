import paho.mqtt.client as mqtt
from SQLQuery import *
from datetime import datetime
from EmailSender import SendEmail
from WeatherAPI import GetWeather
import json
import csv

delay = 5
def SaveData(filename):
    data = QueryData()
    data = tuple(list(data)[:-1])
    with open(filename, "w", newline = '') as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(["ID", "Locaion", "Temperator", "Humidity", "Lux", "Weather Status", "time"])
        csv_writer.writerows(data)
def BackupData(data):
    with open("backup_log.txt", "r") as f:
        currentData = f.read()
        currentData = json.loads(currentData)
        currentDate = int(currentData.get('date').split('-')[1])

    dataLength = len(data)
    dataDate = int(str(data[-1][-1]).split('-')[1])
    if (dataDate != currentDate):
        newDate = str(data[-1][-1]).split(" ")[0]
        dataToWrite = ("{\n"
                f'"date": "{newDate}",\n'
                f'"dataLength": {dataLength}\n'
                "}")
        with open("backup_log.txt", "w") as f:
            f.write(dataToWrite)
        #filename = f"{str(data[-1][-1]).split('-')[1]}{str(data[-1][-1]).split('-')[0]}.csv"
        backupdate = currentData.get('date')
        filename = f"{str(backupdate).split('-')[1]}{str(backupdate).split('-')[0]}.csv"
        SaveData(filename)
        DropTable()
        CreateTable()
        print(f"Backup success in {filename}")
        return True
    return False

dCount = delay

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("ET")

def on_message(client, userdata, msg):
    global dCount
    data = msg.payload.decode().split(" ")
    locationID, temp, hud, lux = data
    ID = int(locationID[-1])
    time = str(datetime.now())[:19]
    status = ["rain", "snow", "clouds", "sunny", "clear"]
    weatherStatus = str(GetWeather("2b1ee2e2dbb1cf55b213fa28591db615", "Hanoi").split(" ")[-1])
    for i in status:
        if i in weatherStatus:
            weatherStatus = i
            break
    if len(weatherStatus) == 2:
        weatherStatus = 'clear'
    print(f"{dCount} UnSave: ID {ID} - At location {locationID}: temp={temp}, hud={hud}, lux={lux}, time={time}, status={weatherStatus}")
    dCount += 1
    if (dCount >= delay):
        print(
            f"Save: ID {ID} - At location {locationID}: temp={temp}, hud={hud}, lux={lux}, time={time}, status={weatherStatus}")
        InsertData(ID, locationID, temp, hud, lux, weatherStatus)
        data = QueryData()
        BackupData(data)
        if (BackupData(data)):
            InsertData(ID, locationID, temp, hud, lux, weatherStatus)
        dCount = 1
    if (float(temp) >= 37):
        SendEmail("Cảnh báo", f"Thông báo từ hệ thống quan trắc môi trường\n"
                              f"Nhiệt độ ngoài trời hiện tại là {temp}\n"
                              f"Vui lòng không ra ngoài nếu không có việc gì quan trọng.\n")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

broker = "broker.hivemq.com"
port = 1883

client.connect(broker, port, 60)
client.loop_forever()
