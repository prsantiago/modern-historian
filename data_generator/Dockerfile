FROM python:3.9-slim

WORKDIR /app

# Copy and install required packages
COPY . .
RUN pip install -r requirements.txt

# Use bash instead of sh
SHELL ["/bin/bash", "-c"]

# Run the script with env file
CMD ["bash", "-c", "set -a && . ./env/.env && set +a && python generate_dummy_data_write_2_influxdb.py"]
