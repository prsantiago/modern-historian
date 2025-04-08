import os
import time
import influxdb_client
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

token = os.getenv('INFLUXDB_TOKEN')
org = "planta_tecate"
url = "http://localhost:8086"
bucket = "home"

write_client = InfluxDBClient(
    url=url,
    token=token,
    org=org
)

write_api = write_client.write_api(write_options=SYNCHRONOUS)

for value in range(5):
    point = (
        Point("mem")
        .tag("host", "host1")
        .field("used_percent", value)
        .time(int(time.time()), WritePrecision.S)
    )
    write_api.write(bucket=bucket, record=point)
    time.sleep(1)