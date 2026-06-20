"""
PowerOff-Timer - Módulo de control de tiempo de apagado de pantalla
Maneja la configuración del tiempo de apagado automático de la pantalla en Windows
"""

import subprocess
import re
from typing import Optional, Tuple


class ScreenController:
    """
    Clase para gestionar la configuración del tiempo de apagado de pantalla en Windows
    """
    
    # Opciones de tiempo disponibles (en minutos)
    TIME_OPTIONS = {
        "1 minuto": 1,
        "5 minutos": 5,
        "10 minutos": 10,
        "15 minutos": 15,
        "30 minutos": 30,
        "40 minutos": 40,
        "1 hora": 60,
        "Nunca": 0
    }
    
    def __init__(self):
        """Inicializar el controlador de pantalla"""
        pass
    
    def get_current_timeout(self) -> Tuple[bool, Optional[int], Optional[int], str]:
        """
        Obtener el tiempo actual de apagado de pantalla para AC y DC
        
        Returns:
            tuple: (éxito: bool, timeout_ac: int|None, timeout_dc: int|None, mensaje: str)
                   Los timeouts están en minutos
        """
        try:
            # Ejecutar comando para obtener la configuración actual
            result = subprocess.run(
                ["powercfg", "/query", "SCHEME_CURRENT", "SUB_VIDEO", "VIDEOIDLE"],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode != 0:
                return False, None, None, f"Error al consultar configuración: {result.stderr}"
            
            # Parsear la salida para obtener los valores AC y DC
            output = result.stdout
            
            # Buscar valores en hexadecimal (segundos)
            # Buscar específicamente las líneas de "índice de configuración" para AC y DC
            # Patrón más específico que busca "índice" + "corriente alterna/AC" + "actual" + valor hex
            ac_match = re.search(r'(?:ndice|index).*?(?:corriente alterna|AC).*?(?:actual|current).*?:\s*0x([0-9a-fA-F]+)', output, re.IGNORECASE | re.DOTALL)
            dc_match = re.search(r'(?:ndice|index).*?(?:corriente continua|DC).*?(?:actual|current).*?:\s*0x([0-9a-fA-F]+)', output, re.IGNORECASE | re.DOTALL)
            
            if not ac_match or not dc_match:
                return False, None, None, "No se pudo parsear la configuración actual"
            
            # Convertir de hexadecimal a decimal (segundos) y luego a minutos
            ac_seconds = int(ac_match.group(1), 16)
            dc_seconds = int(dc_match.group(1), 16)
            
            ac_minutes = ac_seconds // 60
            dc_minutes = dc_seconds // 60
            
            return True, ac_minutes, dc_minutes, "Configuración obtenida exitosamente"
            
        except subprocess.TimeoutExpired:
            return False, None, None, "Timeout al consultar configuración"
        except FileNotFoundError:
            return False, None, None, "Comando powercfg no encontrado"
        except Exception as e:
            return False, None, None, f"Error inesperado: {str(e)}"
    
    def set_screen_timeout(self, minutes: int) -> Tuple[bool, str]:
        """
        Aplicar nuevo tiempo de apagado de pantalla (para AC y DC)
        
        Args:
            minutes: Tiempo en minutos (0 para nunca)
            
        Returns:
            tuple: (éxito: bool, mensaje: str)
        """
        try:
            # Aplicar configuración para AC (conectado a corriente)
            result_ac = subprocess.run(
                ["powercfg", "/change", "monitor-timeout-ac", str(minutes)],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result_ac.returncode != 0:
                return False, f"Error al configurar AC: {result_ac.stderr}"
            
            # Aplicar configuración para DC (batería)
            result_dc = subprocess.run(
                ["powercfg", "/change", "monitor-timeout-dc", str(minutes)],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result_dc.returncode != 0:
                return False, f"Error al configurar DC: {result_dc.stderr}"
            
            # Mensaje de éxito
            if minutes == 0:
                message = "Pantalla configurada para nunca apagarse automáticamente"
            elif minutes == 60:
                message = "Pantalla configurada para apagarse después de 1 hora"
            elif minutes > 60:
                hours = minutes // 60
                remaining = minutes % 60
                if remaining == 0:
                    message = f"Pantalla configurada para apagarse después de {hours} hora{'s' if hours > 1 else ''}"
                else:
                    message = f"Pantalla configurada para apagarse después de {hours} hora{'s' if hours > 1 else ''} y {remaining} minuto{'s' if remaining > 1 else ''}"
            else:
                message = f"Pantalla configurada para apagarse después de {minutes} minuto{'s' if minutes > 1 else ''}"
            
            return True, message
            
        except subprocess.TimeoutExpired:
            return False, "Timeout al aplicar configuración"
        except FileNotFoundError:
            return False, "Comando powercfg no encontrado"
        except Exception as e:
            return False, f"Error inesperado: {str(e)}"
    
    def get_timeout_description(self, minutes: int) -> str:
        """
        Obtener descripción legible del timeout
        
        Args:
            minutes: Tiempo en minutos
            
        Returns:
            str: Descripción del tiempo
        """
        if minutes == 0:
            return "Nunca"
        elif minutes == 1:
            return "1 minuto"
        elif minutes == 60:
            return "1 hora"
        elif minutes >= 60:
            hours = minutes // 60
            remaining_minutes = minutes % 60
            if remaining_minutes == 0:
                return f"{hours} hora{'s' if hours > 1 else ''}"
            else:
                return f"{hours} hora{'s' if hours > 1 else ''} y {remaining_minutes} minuto{'s' if remaining_minutes > 1 else ''}"
        else:
            return f"{minutes} minutos"

# Made with Bob