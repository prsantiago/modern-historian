import os
import yaml
import random
import time
import logging
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

def load_configuration(config_file):
    """
    Load configuration from a YAML file.
    
    Args:
        config_file (str): Path to the YAML configuration file
    
    Returns:
        dict: Configuration parameters
    """
    try:
        with open(config_file, 'r') as file:
            config = yaml.safe_load(file)
            logger.info(f"Configuration loaded successfully from {config_file}")
            return config
    except Exception as e:
        logger.error(f"Failed to load configuration: {str(e)}")
        raise

def generate_value(min_val, max_val, is_integer=False):
    """
    Generate a random value between min_val and max_val.
    
    Args:
        min_val (float): Minimum value
        max_val (float): Maximum value
        is_integer (bool): Whether to generate an integer value
    
    Returns:
        float or int: Generated value
    """
    value = random.randint(min_val, max_val) if is_integer else random.uniform(min_val, max_val)
    return value

def write_to_influxdb(config):
    """
    Generate and write data to InfluxDB based on configuration.
    
    Args:
        config (dict): Configuration parameters
    """
    token = os.getenv('INFLUXDB_TOKEN')
    org = os.getenv('INFLUXDB_ORG')
    url = os.getenv('INFLUXDB_URL')
    bucket = os.getenv('INFLUXDB_BUCKET')

    logger.info(f"Connecting to InfluxDB at {url}")
    logger.debug(f"Using organization: {org}, bucket: {bucket}")

    # Create write client
    try:
        write_client = InfluxDBClient(url=url, token=token, org=org)
        write_api = write_client.write_api(write_options=SYNCHRONOUS)
        logger.info("Successfully connected to InfluxDB")
    except Exception as e:
        logger.error(f"Failed to connect to InfluxDB: {str(e)}")
        raise

    num_records = config['num_registros']
    interval_seconds = config['intervalo_segundos']
    counter = 0

    logger.info(f"Starting data generation. Records to generate: {'infinite' if num_records == -1 else num_records}")
    logger.info(f"Data generation interval: {interval_seconds} seconds")

    try:
        while num_records == -1 or counter < num_records:
            timestamp = int(time.time())
            
            for measurement in config['mediciones']:
                # Generate values
                pv = generate_value(measurement['pv']['min'], measurement['pv']['max'])
                sp = generate_value(measurement['sp']['min'], measurement['sp']['max'])
                cv = generate_value(measurement['cv']['min'], measurement['cv']['max'], is_integer=True)

                # Create point
                point = (
                    Point(measurement['measurement'])
                    .tag("unit", measurement['unidad'])
                    .tag("machine", measurement['maquina'])
                    .tag("subarea", measurement['subarea'])
                    .field("pv", round(pv, 2))
                    .field("sp", round(sp, 2))
                    .field("cv", int(cv))
                    .time(timestamp, WritePrecision.S)
                )

                try:
                    write_api.write(bucket=bucket, record=point)
                    logger.info(
                        f"Written: {measurement['measurement']} - "
                        f"Machine: {measurement['maquina']} - "
                        f"PV: {pv:.2f}, SP: {sp:.2f}, CV: {cv}"
                    )
                except Exception as e:
                    logger.error(f"Failed to write point: {str(e)}")

            counter += 1
            if num_records != -1:
                logger.debug(f"Progress: {counter}/{num_records} records")
            time.sleep(interval_seconds)

    except KeyboardInterrupt:
        logger.warning("User requested shutdown")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
    finally:
        write_client.close()
        logger.info("Connection closed")

def main():
    logger.info("Starting data generator application")
    logger.info("Waiting for InfluxDB to be ready...")
    time.sleep(10)
    
    try:
        config = load_configuration('config.yaml')
        write_to_influxdb(config)
    except Exception as e:
        logger.error(f"Application failed: {str(e)}")
        exit(1)

if __name__ == "__main__":
    main()
