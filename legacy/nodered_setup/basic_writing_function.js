// Definir los tags que queremos simular
const tags = [
  {id: 'TT101', name: 'Temperatura Tanque 1', min: 20, max: 80, unit: '°C'},
  {id: 'PT101', name: 'Presión Tanque 1', min: 1, max: 5, unit: 'bar'},
  {id: 'FT101', name: 'Flujo Línea 1', min: 0, max: 100, unit: 'm³/h'},
  {id: 'LT101', name: 'Nivel Tanque 1', min: 0, max: 100, unit: '%'},
  {id: 'TT201', name: 'Temperatura Tanque 2', min: 20, max: 90, unit: '°C'},
  {id: 'PT201', name: 'Presión Tanque 2', min: 1, max: 6, unit: 'bar'},
  {id: 'VB101', name: 'Vibración Bomba 1', min: 0, max: 10, unit: 'mm/s'},
  {id: 'ST101', name: 'Velocidad Motor 1', min: 0, max: 1800, unit: 'RPM'}
];

// Generar valores aleatorios para cada tag
const timestamp = new Date();
const readingTime = timestamp.toISOString();

let readings = [];
let messages = [];

for (let tag of tags) {
  // Generar un valor aleatorio dentro del rango definido
  const randomValue = tag.min + (Math.random() * (tag.max - tag.min));
  const value = parseFloat(randomValue.toFixed(2));
  
  // Generar un valor de calidad (0-100, donde 100 es perfecto)
  const quality = Math.random() > 0.05 ? 100 : Math.floor(Math.random() * 50);
  
  // Crear una lectura
  const reading = {
      tag_id: tag.id,
      tag_name: tag.name,
      value: value,
      unit: tag.unit,
      quality: quality,
      timestamp: readingTime
  };
  
  readings.push(reading);
  
  // Crear mensajes individuales para cada tag (útil para InfluxDB)
  let msg = {
      measurement: tag.id,
      payload: {
          tag_id: tag.id,
          tag_name: tag.name,
          unit: tag.unit,
          value: value,
          quality: quality,
          timestamp: readingTime
      },
      topic: tag.id
  };
  messages.push(msg);
}

// Mensaje para TimescaleDB (todos los datos juntos)
let timescaleMsg = {
  payload: readings,
  topic: "batch_readings"
};

// Pasar los datos a las salidas
return [timescaleMsg, messages];
