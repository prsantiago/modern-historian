import os
import yaml
import random
import argparse
import time
import influxdb_client
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
    """
    Genera y escribe datos a InfluxDB basados en la configuración.
    
    :param config: Diccionario de configuración
    """
    # Configuración de InfluxDB
    token = os.getenv('INFLUXDB_TOKEN')
    org = config.get('org', 'planta_tecate')
    url = config.get('url', 'http://localhost:8086')
    bucket = config.get('bucket', 'home')

    # Crear cliente de escritura
    write_client = InfluxDBClient(
        url=url,
        token=token,
        org=org
    )
    write_api = write_client.write_api(write_options=SYNCHRONOUS)

    # Parámetros de generación de datos
    num_registros = config['num_registros']
    intervalo_segundos = config['intervalo_segundos']
    timestamp_inicio = config['timestamp_inicio']

    # Generar y escribir puntos
    for i in range(num_registros):
        # Calcular timestamp actual
        timestamp_actual = timestamp_inicio + (i * intervalo_segundos)
        
        # Generar datos para cada medición
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
                .time(timestamp_actual, WritePrecision.S)
            )

            # Escribir punto
            try:
                write_api.write(bucket=bucket, record=point)
                print(f"Escribiendo: {point}")
            except Exception as e:
                print(f"Error al escribir punto: {e}")
        
        # Pequeña pausa entre iteraciones (opcional)
        time.sleep(0.1)

    # Cerrar cliente
    write_client.close()
    print("Escritura de datos completada.")

def main():
    # Configurar parser de argumentos
    parser = argparse.ArgumentParser(description='Generador y escritor de datos dummy para InfluxDB')
    parser.add_argument('config', help='Ruta al archivo de configuración YAML')
    
    args = parser.parse_args()

    # Cargar configuración
    config = cargar_configuracion(args.config)
    
    # Escribir a InfluxDB
    escribir_a_influxdb(config)

if __name__ == "__main__":
    main()