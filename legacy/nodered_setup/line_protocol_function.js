// Lista de tags actualizada
const tags = [
    {measurement: 'FT010205', unidad: 'filtro_2', maquina: 'filtro', subarea: 'filtracion', min: 0.0, max: 100.0}
];

// Función para generar un timestamp Unix en nanosegundos
function generateTimestamp() {
    return Date.now() * 1000000; // Convierte milisegundos a nanosegundos
}

// Función para generar un valor aleatorio
function generateRandomValue(min, max) {
    return parseFloat((min + Math.random() * (max - min)).toFixed(2));
}

// Función para generar el Line Protocol
function generateLineProtocol(tag) {
    // Generar valores para PV, SP, y CV
    const pv = generateRandomValue(tag.min, tag.max);
    const sp = generateRandomValue(tag.min, tag.max);
    const cv = Math.round(Math.random()); // 0 o 1 para CV

    // Construir el Line Protocol
    const tagSet = `unidad=${tag.unidad},maquina=${tag.maquina},subarea=${tag.subarea}`;
    const fieldSet = `pv=${pv},sp=${sp},cv=${cv}i`;
    const timestamp = generateTimestamp();

    return `${tag.measurement},${tagSet} ${fieldSet} ${timestamp}`;
}

// Generar mensajes para cada tag
let messages = tags.map(tag => {
    return {
        payload: generateLineProtocol(tag),
        topic: tag.measurement
    };
});

// Devolver los mensajes
return messages;