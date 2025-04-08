FROM python:3.9-slim

WORKDIR /app

# Install required packages
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy application files
COPY generate_dummy_data_write_2_influxdb.py .
COPY config.yaml .
COPY env/.env.influx .env

# Run the script with env file
CMD ["sh", "-c", "source ./.env && python generate_dummy_data_write_2_influxdb.py"]
