/**
 * WebSocket Manager para Energy Hub
 * Maneja la conexión WebSocket para actualizaciones en tiempo real
 * de gráficas y datos de monitoreo.
 */

class WebSocketManager {
    constructor(wsUrl) {
        this.wsUrl = wsUrl;
        this.ws = null;
        this.reconnectAttempts = 0;
        this.maxReconnectAttempts = 5;
        this.reconnectDelay = 3000;
        this.listeners = {};
    }

    /**
     * Conecta con el servidor WebSocket
     */
    connect() {
        try {
            this.ws = new WebSocket(this.wsUrl);

            this.ws.onopen = () => {
                console.log('WebSocket conectado');
                this.reconnectAttempts = 0;
                this.emit('connected');
            };

            this.ws.onmessage = (event) => {
                try {
                    const data = JSON.parse(event.data);
                    this.emit('message', data);
                    
                    // Emitir eventos específicos según el tipo
                    if (data.type) {
                        this.emit(data.type, data);
                    }
                } catch (error) {
                    console.error('Error procesando mensaje WebSocket:', error);
                }
            };

            this.ws.onerror = (error) => {
                console.error('Error en WebSocket:', error);
                this.emit('error', error);
            };

            this.ws.onclose = () => {
                console.log('WebSocket desconectado');
                this.emit('disconnected');
                this.attemptReconnect();
            };
        } catch (error) {
            console.error('Error conectando WebSocket:', error);
            this.attemptReconnect();
        }
    }

    /**
     * Intenta reconectar con backoff exponencial
     */
    attemptReconnect() {
        if (this.reconnectAttempts < this.maxReconnectAttempts) {
            this.reconnectAttempts++;
            const delay = this.reconnectDelay * Math.pow(2, this.reconnectAttempts - 1);
            console.log(`Intentando reconectar en ${delay}ms (intento ${this.reconnectAttempts})`);
            
            setTimeout(() => {
                this.connect();
            }, delay);
        } else {
            console.error('Máximo de intentos de reconexión alcanzado');
            this.emit('reconnect-failed');
        }
    }

    /**
     * Envía un mensaje al servidor
     */
    send(data) {
        if (this.ws && this.ws.readyState === WebSocket.OPEN) {
            this.ws.send(JSON.stringify(data));
        } else {
            console.warn('WebSocket no está abierto');
        }
    }

    /**
     * Se suscribe a un evento
     */
    on(eventType, callback) {
        if (!this.listeners[eventType]) {
            this.listeners[eventType] = [];
        }
        this.listeners[eventType].push(callback);
    }

    /**
     * Desuscribe de un evento
     */
    off(eventType, callback) {
        if (this.listeners[eventType]) {
            this.listeners[eventType] = this.listeners[eventType].filter(cb => cb !== callback);
        }
    }

    /**
     * Emite un evento a todos los listeners
     */
    emit(eventType, data) {
        if (this.listeners[eventType]) {
            this.listeners[eventType].forEach(callback => {
                callback(data);
            });
        }
    }

    /**
     * Desconecta del servidor WebSocket
     */
    disconnect() {
        if (this.ws) {
            this.ws.close();
            this.ws = null;
        }
    }

    /**
     * Obtiene el estado de la conexión
     */
    isConnected() {
        return this.ws && this.ws.readyState === WebSocket.OPEN;
    }
}

// Instancia global del WebSocket Manager
let wsManager = null;

/**
 * Inicializa el gestor de WebSocket
 */
function initWebSocketManager() {
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const wsUrl = `${protocol}//${window.location.host}/ws/`;
    
    wsManager = new WebSocketManager(wsUrl);
    wsManager.connect();

    // Configurar listeners de eventos
    setupWebSocketListeners();
}

/**
 * Configura los listeners para eventos del WebSocket
 */
function setupWebSocketListeners() {
    // Evento cuando se conecta
    wsManager.on('connected', () => {
        console.log('Sistema conectado a actualizaciones en tiempo real');
        updateConnectionStatus(true);
    });

    // Evento cuando se desconecta
    wsManager.on('disconnected', () => {
        console.log('Sistema desconectado de actualizaciones');
        updateConnectionStatus(false);
    });

    // Evento para datos de energía
    wsManager.on('energy_data', (data) => {
        console.log('Datos de energía recibidos:', data);
        updateEnergyChart(data);
    });

    // Evento para alertas
    wsManager.on('alert', (data) => {
        console.log('Alerta recibida:', data);
        showAlert(data);
    });

    // Evento para estado de dispositivos
    wsManager.on('device_status', (data) => {
        console.log('Estado de dispositivo:', data);
        updateDeviceStatus(data);
    });

    // Evento para datos de monitoreo
    wsManager.on('monitoring_data', (data) => {
        console.log('Datos de monitoreo:', data);
        updateMonitoringDashboard(data);
    });
}

/**
 * Actualiza el indicador de estado de conexión en la UI
 */
function updateConnectionStatus(isConnected) {
    const statusElement = document.getElementById('ws-status');
    if (statusElement) {
        if (isConnected) {
            statusElement.textContent = 'En línea';
            statusElement.className = 'status-connected';
        } else {
            statusElement.textContent = 'Offline';
            statusElement.className = 'status-disconnected';
        }
    }
}

/**
 * Actualiza la gráfica de energía (ejemplo)
 */
function updateEnergyChart(data) {
    // Implementación específica según tu librería de gráficos (Chart.js, D3, etc.)
    // Ejemplo con Chart.js:
    /*
    if (window.energyChart) {
        window.energyChart.data.labels.push(data.timestamp);
        window.energyChart.data.datasets[0].data.push(data.consumption);
        window.energyChart.update();
    }
    */
}

/**
 * Muestra una alerta en la UI
 */
function showAlert(alertData) {
    // Implementación específica para mostrar alertas
    console.warn('Alerta:', alertData.message);
}

/**
 * Actualiza el estado de dispositivos
 */
function updateDeviceStatus(data) {
    // Implementación específica para actualizar estado de dispositivos
    console.log('Actualizando dispositivo:', data.device_id, 'Estado:', data.status);
}

/**
 * Actualiza el dashboard de monitoreo
 */
function updateMonitoringDashboard(data) {
    // Implementación específica para actualizar dashboard
    console.log('Actualizando monitoreo:', data);
}

// Inicializar cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', () => {
    initWebSocketManager();
});

// Limpiar conexión al cerrar página
window.addEventListener('beforeunload', () => {
    if (wsManager) {
        wsManager.disconnect();
    }
});
