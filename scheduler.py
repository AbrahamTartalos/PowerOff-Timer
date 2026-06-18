"""
PowerOff-Timer - Módulo de programación y ejecución de acciones del sistema
Maneja la lógica de temporización y ejecución de comandos
"""

import subprocess
import threading
import time
from datetime import datetime, timedelta
from typing import Callable, Optional


class SystemScheduler:
    """
    Clase para programar y ejecutar acciones del sistema (apagar, hibernar, suspender)
    """
    
    # Tipos de acciones disponibles
    ACTION_SHUTDOWN = "Apagar"
    ACTION_HIBERNATE = "Hibernar"
    ACTION_SUSPEND = "Suspender"
    
    # Comandos de Windows para cada acción
    COMMANDS = {
        ACTION_SHUTDOWN: ["shutdown", "/s", "/t", "0"],
        ACTION_HIBERNATE: ["shutdown", "/h"],
        ACTION_SUSPEND: ["rundll32.exe", "powrprof.dll,SetSuspendState", "0", "1", "0"]
    }
    
    def __init__(self):
        """Inicializar el programador"""
        self.scheduled_thread: Optional[threading.Thread] = None
        self.cancel_event = threading.Event()
        self.target_time: Optional[datetime] = None
        self.action_type: Optional[str] = None
        self.warning_callback: Optional[Callable] = None
        self.completion_callback: Optional[Callable] = None
        self.is_running = False
    
    def schedule_action(
        self, 
        target_time: str, 
        action_type: str,
        warning_callback: Optional[Callable] = None,
        completion_callback: Optional[Callable] = None
    ) -> tuple[bool, str]:
        """
        Programar una acción del sistema para una hora específica
        
        Args:
            target_time: Hora en formato "HH:MM" (24 horas)
            action_type: Tipo de acción (Apagar, Hibernar, Suspender)
            warning_callback: Función a llamar 60 segundos antes de la acción
            completion_callback: Función a llamar cuando se complete o cancele
            
        Returns:
            tuple: (éxito: bool, mensaje: str)
        """
        # Validar que no haya una acción ya programada
        if self.is_running:
            return False, "Ya hay una acción programada. Cancélala primero."
        
        # Validar el tipo de acción
        if action_type not in self.COMMANDS:
            return False, f"Tipo de acción inválido: {action_type}"
        
        # Parsear y validar la hora
        try:
            hour, minute = map(int, target_time.split(":"))
            if not (0 <= hour <= 23 and 0 <= minute <= 59):
                return False, "Hora inválida. Usa formato HH:MM (00:00 - 23:59)"
        except (ValueError, AttributeError):
            return False, "Formato de hora inválido. Usa HH:MM"
        
        # Calcular la hora objetivo
        now = datetime.now()
        target = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
        
        # Si la hora ya pasó hoy, programar para mañana
        if target <= now:
            target += timedelta(days=1)
        
        # Guardar configuración
        self.target_time = target
        self.action_type = action_type
        self.warning_callback = warning_callback
        self.completion_callback = completion_callback
        self.cancel_event.clear()
        self.is_running = True
        
        # Iniciar el hilo de programación
        self.scheduled_thread = threading.Thread(
            target=self._run_scheduler,
            daemon=True
        )
        self.scheduled_thread.start()
        
        # Calcular tiempo de espera
        wait_seconds = (target - now).total_seconds()
        wait_time = self._format_wait_time(wait_seconds)
        
        return True, f"Acción programada para {target.strftime('%H:%M:%S')} ({wait_time})"
    
    def cancel_scheduled_action(self) -> tuple[bool, str]:
        """
        Cancelar la acción programada
        
        Returns:
            tuple: (éxito: bool, mensaje: str)
        """
        if not self.is_running:
            return False, "No hay ninguna acción programada"
        
        # Señalar cancelación
        self.cancel_event.set()
        self.is_running = False
        
        # Esperar a que el hilo termine (máximo 2 segundos)
        if self.scheduled_thread and self.scheduled_thread.is_alive():
            self.scheduled_thread.join(timeout=2.0)
        
        # Llamar al callback de completación si existe
        if self.completion_callback:
            try:
                self.completion_callback(cancelled=True)
            except Exception as e:
                print(f"Error en completion_callback: {e}")
        
        return True, "Acción cancelada exitosamente"
    
    def _run_scheduler(self):
        """
        Función principal del hilo de programación
        Espera hasta la hora objetivo y ejecuta la acción
        """
        try:
            while self.is_running and not self.cancel_event.is_set():
                now = datetime.now()
                
                # Verificar que target_time no sea None
                if self.target_time is None:
                    break
                
                remaining_seconds = (self.target_time - now).total_seconds()
                
                # Si ya pasó la hora (por algún error de sincronización)
                if remaining_seconds <= 0:
                    self._execute_action()
                    break
                
                # Si faltan 60 segundos o menos, mostrar advertencia
                if remaining_seconds <= 60 and self.warning_callback:
                    try:
                        self.warning_callback(int(remaining_seconds))
                    except Exception as e:
                        print(f"Error en warning_callback: {e}")
                    
                    # Esperar el tiempo restante en intervalos pequeños
                    # para poder cancelar rápidamente si es necesario
                    while remaining_seconds > 0 and not self.cancel_event.is_set():
                        time.sleep(min(1, remaining_seconds))
                        now = datetime.now()
                        remaining_seconds = (self.target_time - now).total_seconds()
                    
                    # Si no se canceló, ejecutar la acción
                    if not self.cancel_event.is_set():
                        self._execute_action()
                    break
                
                # Esperar en intervalos de 1 segundo para poder cancelar rápidamente
                time.sleep(min(1, remaining_seconds))
            
        except Exception as e:
            print(f"Error en el programador: {e}")
        finally:
            self.is_running = False
            
            # Llamar al callback de completación si no fue cancelado
            if not self.cancel_event.is_set() and self.completion_callback:
                try:
                    self.completion_callback(cancelled=False)
                except Exception as e:
                    print(f"Error en completion_callback: {e}")
    
    def _execute_action(self):
        """
        Ejecutar el comando del sistema correspondiente a la acción programada
        """
        if not self.action_type or self.action_type not in self.COMMANDS:
            print(f"Error: Tipo de acción inválido: {self.action_type}")
            return
        
        command = self.COMMANDS[self.action_type]
        
        try:
            print(f"Ejecutando acción: {self.action_type}")
            print(f"Comando: {' '.join(command)}")
            
            # Ejecutar el comando
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode != 0:
                print(f"Error al ejecutar comando: {result.stderr}")
            else:
                print(f"Comando ejecutado exitosamente")
                
        except subprocess.TimeoutExpired:
            print("Error: El comando tardó demasiado en ejecutarse")
        except FileNotFoundError:
            print(f"Error: Comando no encontrado: {command[0]}")
        except Exception as e:
            print(f"Error al ejecutar acción: {e}")
    
    def _format_wait_time(self, seconds: float) -> str:
        """
        Formatear el tiempo de espera en un formato legible
        
        Args:
            seconds: Segundos de espera
            
        Returns:
            str: Tiempo formateado (ej: "2h 30m")
        """
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        
        if hours > 0:
            return f"{hours}h {minutes}m"
        elif minutes > 0:
            return f"{minutes}m"
        else:
            return "menos de 1m"
    
    def get_remaining_time(self) -> Optional[str]:
        """
        Obtener el tiempo restante hasta la acción programada
        
        Returns:
            str: Tiempo restante formateado, o None si no hay acción programada
        """
        if not self.is_running or not self.target_time:
            return None
        
        now = datetime.now()
        remaining_seconds = (self.target_time - now).total_seconds()
        
        if remaining_seconds <= 0:
            return "Ejecutando..."
        
        hours = int(remaining_seconds // 3600)
        minutes = int((remaining_seconds % 3600) // 60)
        seconds = int(remaining_seconds % 60)
        
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    
    def is_action_scheduled(self) -> bool:
        """
        Verificar si hay una acción programada
        
        Returns:
            bool: True si hay una acción programada
        """
        return self.is_running

# Made with Bob
