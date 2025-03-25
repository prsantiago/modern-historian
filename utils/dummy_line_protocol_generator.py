import yaml
import random
import argparse


def cargar_configuracion(archivo_config):
    """Carga la configuración desde un archivo YAML."""
    with open(archivo_config, 'r') as file:
        config = yaml.safe_load(file)
    return config

def generar_valor(min_val, max_val, es_entero=False):
    """Genera un valor aleatorio entre min_val y max_val."""
    valor = random.randint(min_val, max_val) if es_entero else random.uniform(min_val, max_val)
    return valor

def generar_datos_line_protocol(config):
    """Genera datos en formato Line Protocol basados en la configuración proporcionada."""
    num_registros = config['num_registros']
    intervalo_segundos = config['intervalo_segundos']
    timestamp_inicio = config['timestamp_inicio'] * 1_000_000_000  # Convertir a nanosegundos

    lineas = []

    for i in range(num_registros):
        timestamp = timestamp_inicio + (i * intervalo_segundos * 1_000_000_000)
        for medicion in config['mediciones']:
            pv = generar_valor(medicion['pv']['min'], medicion['pv']['max'])
            sp = generar_valor(medicion['sp']['min'], medicion['sp']['max'])
            cv = generar_valor(medicion['cv']['min'], medicion['cv']['max'], es_entero=True)

            linea = (
                f"{medicion['measurement']},"
                f"unidad={medicion['unidad']},"
                f"maquina={medicion['maquina']},"
                f"subarea={medicion['subarea']} "
                f"pv={pv:.2f},"
                f"sp={sp:.2f},"
                f"cv={cv}i "
                f"{timestamp}"
            )
            lineas.append(linea)

    return lineas

def guardar_datos(archivo_salida, lineas):
    """Guarda las líneas generadas en un archivo de texto."""
    with open(archivo_salida, 'w') as file:
        for linea in lineas:
            file.write(f"{linea}\n")

def main():
    # Configurar parser de argumentos
    parser = argparse.ArgumentParser(description='Generador de datos dummy para InfluxDB')
    parser.add_argument('config', help='Ruta al archivo de configuración YAML')
    parser.add_argument('-o', '--output', default='influxdb_dummy_data.line', 
                        help='Ruta de salida para el archivo de datos (default: influxdb_dummy_data.line)')
    
    args = parser.parse_args()

    config = cargar_configuracion(args.config)
    lineas = generar_datos_line_protocol(config)
    guardar_datos(args.output, lineas)
    print(f"Datos generados y guardados en '{args.output}'.")

if __name__ == "__main__":
    main()
