# 🔍 MX-NET-SCANNER

<p align="center">
  <img src="https://img.shields.io/badge/version-1.0-blue.svg" alt="Version">
  <img src="https://img.shields.io/badge/Python-3.6+-green.svg" alt="Python">
  <img src="https://img.shields.io/badge/platform-Linux%20%7C%20Windows-lightgrey.svg" alt="Platform">
  <img src="https://img.shields.io/badge/license-MIT-brightgreen.svg" alt="License">
</p>

<p align="center">
  <strong>Herramienta de red con escaneo básico de puertos + servidor web integrado</strong><br>
  Ideal para auditorías rápidas en Linux y Windows
</p>

## 📋 Tabla de Contenidos
- [Características](#-características)
- [Requisitos](#-requisitos)
- [Instalación](#-instalación)
- [Uso Rápido](#-uso-rápido)
- [Opciones de Línea de Comandos](#-opciones-de-línea-de-comandos)
- [Ejemplos Prácticos](#-ejemplos-prácticos)
- [Interfaz Web](#-interfaz-web)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Solución de Problemas](#-solución-de-problemas)
- [Advertencia Legal](#️-advertencia-legal)
- [Licencia](#-licencia)

## ✨ Características

| Característica | Descripción |
|----------------|-------------|
| 🚀 **Escaneo Multi-hilo** | Escaneo rápido usando hilos concurrentes |
| 🌐 **Servidor Web Integrado** | Visualiza resultados en tiempo real desde el navegador |
| 🔧 **Detección de Servicios** | Reconoce más de 40 servicios comunes por puerto |
| 📊 **Reporte en JSON** | Exporta resultados para análisis posteriores |
| 💻 **Multiplataforma** | Funciona en Linux y Windows sin modificaciones |
| ⚡ **Sin Dependencias** | Usa solo librerías estándar de Python |
| 🎨 **Interfaz Web Moderna** | Diseño responsive con auto-actualización |
| 🔄 **Auto-apertura** | Abre automáticamente el navegador con los resultados |

## 📦 Requisitos

- **Python 3.6 o superior**
- **Permisos de administrador/root** (recomendado para puertos bajos)
- Sin librerías externas requeridas

## 🛠️ Instalación

### Desde GitHub
```bash
# Clonar el repositorio
git clone https://github.com/Falconmx1/MX-NET-SCANNER.git
cd MX-NET-SCANNER

# Dar permisos de ejecución (Linux/Mac)
chmod +x mx_net_scanner.py

Descarga directa
# Usando wget
wget https://raw.githubusercontent.com/Falconmx1/MX-NET-SCANNER/main/mx_net_scanner.py

# Usando curl
curl -O https://raw.githubusercontent.com/Falconmx1/MX-NET-SCANNER/main/mx_net_scanner.py

🚀 Uso Rápido
# Escaneo básico (puertos 1-1000)
python3 mx_net_scanner.py --target 192.168.1.1

# Escaneo con rango personalizado
python3 mx_net_scanner.py --target google.com --start 1 --end 5000

# En Linux (requiere sudo para puertos privilegiados)
sudo python mx_net_scanner.py --target localhost

# En Windows (como administrador)
python3 mx_net_scanner.py --target 192.168.1.1

📝 Ejemplos Prácticos
1. Escaneo rápido de red local
python mx_net_scanner.py --target 192.168.1.1 --end 500 --threads 200

2. Escaneo completo de puertos comunes
python3 mx_net_scanner.py --target scanme.nmap.org --start 1 --end 1000

3. Escaneo con servidor web en puerto diferente
python3 mx_net_scanner.py --target 10.0.0.1 --web-port 9000

4. Escaneo lento pero preciso (timeout alto)
python3 mx_net_scanner.py --target 192.168.1.100 --timeout 3 --threads 50

🌐 Interfaz Web
Una vez iniciado el escaneo, la herramienta:

Inicia automáticamente un servidor web

Abre el navegador con el reporte en tiempo real

Actualiza los resultados automáticamente mientras escanea

Acceso web:
http://localhost:8080          # Puerto por defecto
http://localhost:9000          # Puerto personalizado
http://tu-ip:8080             # Desde otros dispositivos

🔧 Solución de Problemas
Error: Permission denied en Linux
# Solución: Ejecutar con sudo
sudo python mx_net_scanner.py --target localhost

Error: No se pudo resolver el dominio
# Verifica la conexión DNS
ping google.com
# O usa IP directamente
python3 mx_net_scanner.py --target 8.8.8.8

Error: Puerto 8080 ya está en uso
# Usa un puerto diferente
python3 mx_net_scanner.py --target 192.168.1.1 --web-port 8888

En Windows: python no se reconoce como comando
# Usa python3 o la ruta completa
python3 mx_net_scanner.py --target 192.168.1.1
# O usa py
py mx_net_scanner.py --target 192.168.1.1
