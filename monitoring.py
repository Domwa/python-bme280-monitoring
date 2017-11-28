#!/usr/bin/python2.7
import smbus2
import bme280
from influxdb import InfluxDBClient
import argparse

parser = argparse.ArgumentParser(description='Script for getting temperature, humidity and pressure from BME280. And store it in InfluxDB')
parser.add_argument("-h", "--host", help="hostname", action="store")
parser.add_argument("-db", "--main_db", help="db name", action="store")
parser.add_argument("-u", "--user_db", help="db user name", action="store")
parser.add_argument("-p", "--pass_db", help="db password", action="store")
args = parser.parse_args()
hostname = args.host
main_db = args.main_db
user_db = args.user_db
pass_db = args.pass_db

temperature,pressure,humidity = bme280.readBME280All()
port = 1
address = 0x76
bus = smbus2.SMBus(port)

json_body = [
    {
        "measurement": "environment",
        "fields": {
            "temperature": temperature,
            "pressure": pressure,
            "humidity": humidity
        },
    }
]
client = InfluxDBClient(hostname, 8086, user_db, pass_db, main_db)
client.write_points(json_body)