#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MX-NET-SCANNER - Herramienta de red con escaneo de puertos + servidor web
Autor: Falconmx1
Licencia: MIT
"""

import socket
import threading
import json
import argparse
import time
import sys
import os
from http.server import HTTPServer, SimpleHTTPRequestHandler
import webbrowser

# Configuración global
SCAN_RESULTS = {
    "target": "",
    "start_time": "",
    "end_time": "",
    "open_ports": [],
    "total_ports_scanned": 0,
    "status": "scanning"
}

# Servicios comunes (puerto -> nombre)
SERVICES = {
    20: "FTP-DATA", 21: "FTP", 22: "SSH", 23: "TELNET", 25: "SMTP",
    53: "DNS", 80: "HTTP", 110: "POP3", 111: "RPC", 135: "RPC",
    139: "NETBIOS", 143: "IMAP", 443: "HTTPS", 445: "SMB", 993: "IMAPS",
    995: "POP3S", 1433: "MSSQL", 1521: "ORACLE", 1723: "PPTP",
    3306: "MYSQL", 3389: "RDP", 5432: "POSTGRES", 5900: "VNC",
    6379: "REDIS", 8080: "HTTP-ALT", 8443: "HTTPS-ALT", 27017: "MONGODB"
}

def get_service_name(port):
    """Retorna el nombre del servicio para un puerto dado"""
    return SERVICES.get(port, "UNKNOWN")

def scan_port(target, port, timeout=1):
    """Escanea un puerto individual"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((target, port))
        sock.close()
        
        if result == 0:
            service = get_service_name(port)
            return {"port": port, "service": service, "status": "open"}
        return None
    except:
        return None

def scan_ports(target, start_port, end_port, max_threads=100):
    """Escanea un rango de puertos usando hilos"""
    global SCAN_RESULTS
    
    print(f"\n[+] Iniciando escaneo de {target}")
    print(f"[+] Rango de puertos: {start_port} - {end_port}")
    print(f"[+] Usando {max_threads} hilos concurrentes\n")
    
    open_ports = []
    threads = []
    results_lock = threading.Lock()
    
    def worker(port):
        result = scan_port(target, port)
        if result:
            with results_lock:
                open_ports.append(result)
                print(f"[+] Puerto {port} -> {result['service']} (ABIERTO)")
    
    # Crear y lanzar hilos
    for port in range(start_port, end_port + 1):
        t = threading.Thread(target=worker, args=(port,))
        threads.append(t)
        t.start()
        
        # Limitar número de hilos concurrentes
        if len(threads) >= max_threads:
            for t in threads:
                t.join()
            threads = []
    
    # Esperar hilos restantes
    for t in threads:
        t.join()
    
    SCAN_RESULTS["open_ports"] = open_ports
    SCAN_RESULTS["total_ports_scanned"] = end_port - start_port + 1
    SCAN_RESULTS["status"] = "completed"
    
    return open_ports

class WebHandler(SimpleHTTPRequestHandler):
    """Manejador personalizado para el servidor web"""
    
    def do_GET(self):
        if self.path == '/' or self.path == '/index.html':
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(generate_html_report().encode('utf-8'))
        elif self.path == '/results.json':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(SCAN_RESULTS, indent=2).encode('utf-8'))
        else:
            super().do_GET()
    
    def log_message(self, format, *args):
        """Silenciar logs del servidor web"""
        pass

def generate_html_report():
    """Genera el reporte HTML con los resultados del escaneo"""
    html = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>MX-NET-SCANNER - Reporte de Escaneo</title>
        <style>
            * {{ margin: 0; padding: 0; box-sizing: border-box; }}
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                padding: 20px;
            }}
            .container {{
                max-width: 1200px;
                margin: 0 auto;
                background: white;
                border-radius: 10px;
                box-shadow: 0 20px 60px rgba(0,0,0,0.3);
                overflow: hidden;
            }}
            .header {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 30px;
                text-align: center;
            }}
            .header h1 {{ font-size: 2.5em; margin-bottom: 10px; }}
            .header p {{ font-size: 1.1em; opacity: 0.9; }}
            .content {{ padding: 30px; }}
            .info-box {{
                background: #f0f0f0;
                padding: 20px;
                border-radius: 8px;
                margin-bottom: 30px;
            }}
            .info-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 15px;
                margin-top: 15px;
            }}
            .info-item {{
                background: white;
                padding: 15px;
                border-radius: 5px;
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            }}
            .info-label {{ font-weight: bold; color: #667eea; }}
            .info-value {{ font-size: 1.2em; margin-top: 5px; }}
            table {{
                width: 100%;
                border-collapse: collapse;
                margin-top: 20px;
            }}
            th, td {{
                padding: 12px;
                text-align: left;
                border-bottom: 1px solid #ddd;
            }}
            th {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
            }}
            tr:hover {{ background: #f5f5f5; }}
            .status-open {{ color: #4CAF50; font-weight: bold; }}
            .footer {{
                background: #333;
                color: white;
                text-align: center;
                padding: 20px;
                font-size: 0.9em;
            }}
            .badge {{
                display: inline-block;
                padding: 3px 8px;
                border-radius: 3px;
                font-size: 0.85em;
                font-weight: bold;
            }}
            .badge-open {{ background: #4CAF50; color: white; }}
            .refresh-btn {{
                background: #667eea;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                cursor: pointer;
                margin-bottom: 20px;
                font-size: 1em;
            }}
            .refresh-btn:hover {{ background: #764ba2; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🔍 MX-NET-SCANNER</h1>
                <p>Reporte de Escaneo de Puertos</p>
            </div>
            <div class="content">
                <button class="refresh-btn" onclick="location.reload()">🔄 Actualizar</button>
                
                <div class="info-box">
                    <h3>📊 Información del Escaneo</h3>
                    <div class="info-grid">
                        <div class="info-item">
                            <div class="info-label">Target</div>
                            <div class="info-value">{SCAN_RESULTS.get('target', 'N/A')}</div>
                        </div>
                        <div class="info-item">
                            <div class="info-label">Estado</div>
                            <div class="info-value">{SCAN_RESULTS.get('status', 'unknown').upper()}</div>
                        </div>
                        <div class="info-item">
                            <div class="info-label">Puertos Escaneados</div>
                            <div class="info-value">{SCAN_RESULTS.get('total_ports_scanned', 0)}</div>
                        </div>
                        <div class="info-item">
                            <div class="info-label">Puertos Abiertos</div>
                            <div class="info-value">{len(SCAN_RESULTS.get('open_ports', []))}</div>
                        </div>
                    </div>
                </div>
                
                <h3>🔓 Puertos Abiertos Detectados</h3>
    """
    
    if SCAN_RESULTS.get('open_ports') and len(SCAN_RESULTS['open_ports']) > 0:
        html += """
                <table>
                    <thead>
                        <tr><th>Puerto</th><th>Servicio</th><th>Estado</th></tr>
                    </thead>
                    <tbody>
        """
        for port_info in SCAN_RESULTS['open_ports']:
            html += f"""
                        <tr>
                            <td><strong>{port_info['port']}</strong></td>
                            <td>{port_info['service']}</td>
                            <td><span class="badge badge-open">ABIERTO</span></td>
                        </tr>
            """
        html += """
                    </tbody>
                </table>
        """
    else:
        html += """
                <div style="text-align: center; padding: 40px; color: #999;">
                    ⚠️ No se encontraron puertos abiertos
                </div>
        """
    
    html += """
            </div>
            <div class="footer">
                <p>MX-NET-SCANNER v1.0 | Herramienta de red para pentesting ético</p>
                <p>Usa esta herramienta solo en redes con autorización</p>
            </div>
        </div>
        <script>
            // Auto-refresh cada 3 segundos si el escaneo está en progreso
            if ({json.dumps(SCAN_RESULTS.get('status') == 'scanning')}) {{
                setTimeout(() => {{ location.reload(); }}, 3000);
            }}
        </script>
    </body>
    </html>
    """
    return html

def start_web_server(port=8080):
    """Inicia el servidor web en un hilo separado"""
    server = HTTPServer(('', port), WebHandler)
    print(f"\n[+] Servidor web iniciado en http://localhost:{port}")
    print("[+] Abriendo navegador automáticamente...")
    webbrowser.open(f'http://localhost:{port}')
    server.serve_forever()

def main():
    parser = argparse.ArgumentParser(
        description='MX-NET-SCANNER - Escáner de puertos con interfaz web',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Ejemplos:
  python mx_net_scanner.py --target 192.168.1.1
  python mx_net_scanner.py --target google.com --start 20 --end 1000
  python mx_net_scanner.py --target 127.0.0.1 --threads 200 --web-port 9090
        '''
    )
    
    parser.add_argument('--target', '-t', required=True, help='IP o dominio a escanear')
    parser.add_argument('--start', '-s', type=int, default=1, help='Puerto inicial (default: 1)')
    parser.add_argument('--end', '-e', type=int, default=1000, help='Puerto final (default: 1000)')
    parser.add_argument('--threads', '-th', type=int, default=100, help='Hilos concurrentes (default: 100)')
    parser.add_argument('--web-port', '-wp', type=int, default=8080, help='Puerto del servidor web (default: 8080)')
    parser.add_argument('--timeout', '-to', type=float, default=1.0, help='Timeout por puerto en segundos (default: 1.0)')
    
    args = parser.parse_args()
    
    # Validar rango de puertos
    if args.start < 1 or args.end > 65535 or args.start > args.end:
        print("[!] Error: Rango de puertos inválido (1-65535)")
        sys.exit(1)
    
    # Resolver dominio si es necesario
    target = args.target
    try:
        # Intentar resolver a IP
        ip = socket.gethostbyname(target)
        if ip != target:
            print(f"[+] Resolviendo {target} -> {ip}")
            target = ip
    except:
        print(f"[!] Error: No se pudo resolver {target}")
        sys.exit(1)
    
    # Guardar target en resultados globales
    SCAN_RESULTS["target"] = target
    SCAN_RESULTS["start_time"] = time.strftime("%Y-%m-%d %H:%M:%S")
    SCAN_RESULTS["status"] = "scanning"
    
    # Iniciar servidor web en hilo separado
    web_thread = threading.Thread(target=start_web_server, args=(args.web_port,), daemon=True)
    web_thread.start()
    
    # Pequeña pausa para que el servidor web arranque
    time.sleep(2)
    
    # Realizar escaneo
    try:
        open_ports = scan_ports(target, args.start, args.end, args.threads)
        
        SCAN_RESULTS["end_time"] = time.strftime("%Y-%m-%d %H:%M:%S")
        SCAN_RESULTS["status"] = "completed"
        
        # Guardar resultados a archivo
        with open("scan_results.json", "w") as f:
            json.dump(SCAN_RESULTS, f, indent=2)
        
        print(f"\n[+] Escaneo completado!")
        print(f"[+] Puertos abiertos encontrados: {len(open_ports)}")
        print(f"[+] Reporte guardado en scan_results.json")
        print(f"[+] Web disponible en http://localhost:{args.web_port}")
        print(f"[+] Presiona Ctrl+C para detener el servidor web\n")
        
        # Mantener el servidor web vivo
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n[!] Deteniendo servidor web...")
        sys.exit(0)

if __name__ == "__main__":
    # Verificar permisos (warning si no es root/admin)
    if sys.platform.startswith('win'):
        import ctypes
        if not ctypes.windll.shell32.IsUserAnAdmin():
            print("[!] ADVERTENCIA: En Windows, ejecuta como ADMINISTRADOR para mejores resultados")
    else:
        if os.geteuid() != 0:
            print("[!] ADVERTENCIA: En Linux, ejecuta con sudo para escaneos completos")
    
    main()
