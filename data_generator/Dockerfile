FROM python:3.9-slim

WORKDIR /app

# Install required packages
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy application files
COPY generate_dummy_data_write_2_influxdb.py .
COPY config.yaml .

# Run the script
CMD ["python", "generate_dummy_data_write_2_influxdb.py", "config.yaml"]
