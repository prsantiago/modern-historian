import os
import yaml
import random
import time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

def cargar_configuracion(archivo_config):
    """Carga la configuración desde un archivo YAML."""
    with open(archivo_config, 'r') as file:
        config = yaml.safe_load(file)
    return config

def generar_valor(min_val, max_val, es_entero=False):
    """Genera un valor aleatorio entre min_val y max_val."""
    valor = random.randint(min_val, max_val) if es_entero else random.uniform(min_val, max_val)
    return valor

def escribir_a_influxdb(config):
    """Genera y escribe datos a InfluxDB basados en la configuración."""
    token = os.getenv('INFLUXDB_TOKEN')
    org = os.getenv('INFLUXDB_ORG')
    url = os.getenv('INFLUXDB_URL')
    bucket = os.getenv('INFLUXDB_BUCKET')

    # Crear cliente de escritura
    write_client = InfluxDBClient(url=url, token=token, org=org)
    write_api = write_client.write_api(write_options=SYNCHRONOUS)

    num_registros = config['num_registros']
    intervalo_segundos = config['intervalo_segundos']
    counter = 0

    try:
        while num_registros == -1 or counter < num_registros:
            timestamp = int(time.time())
            
            for medicion in config['mediciones']:
                # Generar valores
                pv = generar_valor(medicion['pv']['min'], medicion['pv']['max'])
                sp = generar_valor(medicion['sp']['min'], medicion['sp']['max'])
                cv = generar_valor(medicion['cv']['min'], medicion['cv']['max'], es_entero=True)

                # Crear punto
                point = (
                    Point(medicion['measurement'])
                    .tag("unidad", medicion['unidad'])
                    .tag("maquina", medicion['maquina'])
                    .tag("subarea", medicion['subarea'])
                    .field("pv", round(pv, 2))
                    .field("sp", round(sp, 2))
                    .field("cv", int(cv))
                    .time(timestamp, WritePrecision.S)
                )

                try:
                    write_api.write(bucket=bucket, record=point)
                    print(f"Escribiendo: {medicion['measurement']} - PV: {pv:.2f}, SP: {sp:.2f}, CV: {cv}")
                except Exception as e:
                    print(f"Error al escribir punto: {e}")
            
            counter += 1
            time.sleep(intervalo_segundos)

    except KeyboardInterrupt:
        print("\nDetención solicitada por el usuario")
    finally:
        write_client.close()
        print("Conexión cerrada")

def main():
    config = cargar_configuracion('config.yaml')
    escribir_a_influxdb(config)

if __name__ == "__main__":
    # Add initial delay to ensure InfluxDB is ready
    time.sleep(10)
    main()
