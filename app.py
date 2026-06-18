"""
PowerOff-Timer - Interfaz gráfica de usuario
Maneja la interfaz Tkinter y la interacción con el usuario
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading
from scheduler import SystemScheduler


class PowerOffTimerApp:
    """
    Clase principal de la interfaz gráfica de la aplicación
    """
    
    def __init__(self, root: tk.Tk):
        """
        Inicializar la aplicación
        
        Args:
            root: Ventana principal de Tkinter
        """
        self.root = root
        self.scheduler = SystemScheduler()
        self.warning_window = None
        self.countdown_active = False
        
        # Configurar la ventana principal
        self._setup_window()
        
        # Crear la interfaz
        self._create_widgets()
        
        # Iniciar actualización del estado
        self._update_status()
    
    def _setup_window(self):
        """Configurar la ventana principal"""
        self.root.title("PowerOff-Timer")
        self.root.geometry("400x300")
        self.root.resizable(False, False)
        
        # Centrar la ventana en la pantalla
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
        # Configurar el cierre de la ventana
        self.root.protocol("WM_DELETE_WINDOW", self._on_closing)
    
    def _create_widgets(self):
        """Crear todos los widgets de la interfaz"""
        # Frame principal con padding
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=tk.W+tk.E+tk.N+tk.S)
        
        # Título
        title_label = ttk.Label(
            main_frame,
            text="Programar apagado del sistema",
            font=("Arial", 12, "bold")
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Label y entrada para la hora
        time_label = ttk.Label(main_frame, text="Hora (HH:MM):")
        time_label.grid(row=1, column=0, sticky=tk.W, pady=5)
        
        # Frame para la entrada de hora
        time_frame = ttk.Frame(main_frame)
        time_frame.grid(row=1, column=1, sticky=tk.W+tk.E, pady=5)
        
        # Entrada de hora con validación
        self.hour_var = tk.StringVar()
        self.minute_var = tk.StringVar()
        
        hour_entry = ttk.Entry(time_frame, textvariable=self.hour_var, width=5, justify="center")
        hour_entry.grid(row=0, column=0, padx=(0, 5))
        
        separator_label = ttk.Label(time_frame, text=":")
        separator_label.grid(row=0, column=1)
        
        minute_entry = ttk.Entry(time_frame, textvariable=self.minute_var, width=5, justify="center")
        minute_entry.grid(row=0, column=2, padx=(5, 0))
        
        # Placeholder text
        self.hour_var.set("00")
        self.minute_var.set("00")
        
        # Label y selector de acción
        action_label = ttk.Label(main_frame, text="Acción:")
        action_label.grid(row=2, column=0, sticky=tk.W, pady=5)
        
        self.action_var = tk.StringVar()
        action_combo = ttk.Combobox(
            main_frame,
            textvariable=self.action_var,
            values=[
                SystemScheduler.ACTION_SHUTDOWN,
                SystemScheduler.ACTION_HIBERNATE,
                SystemScheduler.ACTION_SUSPEND
            ],
            state="readonly",
            width=18
        )
        action_combo.grid(row=2, column=1, sticky=tk.W+tk.E, pady=5)
        action_combo.current(0)  # Seleccionar "Apagar" por defecto
        
        # Frame para los botones
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=20)
        
        # Botón Programar
        self.schedule_button = ttk.Button(
            button_frame,
            text="Programar",
            command=self._on_schedule_click,
            width=15
        )
        self.schedule_button.grid(row=0, column=0, padx=5)
        
        # Botón Cancelar
        self.cancel_button = ttk.Button(
            button_frame,
            text="Cancelar",
            command=self._on_cancel_click,
            state=tk.DISABLED,
            width=15
        )
        self.cancel_button.grid(row=0, column=1, padx=5)
        
        # Label de estado
        self.status_label = ttk.Label(
            main_frame,
            text="Estado: Esperando...",
            font=("Arial", 9),
            foreground="gray"
        )
        self.status_label.grid(row=4, column=0, columnspan=2, pady=(10, 0))
        
        # Label de tiempo restante
        self.time_remaining_label = ttk.Label(
            main_frame,
            text="",
            font=("Arial", 10, "bold"),
            foreground="blue"
        )
        self.time_remaining_label.grid(row=5, column=0, columnspan=2, pady=5)
        
        # Configurar el grid para que se expanda
        main_frame.columnconfigure(1, weight=1)
    
    def _on_schedule_click(self):
        """Manejar el clic en el botón Programar"""
        # Obtener los valores
        try:
            hour = int(self.hour_var.get())
            minute = int(self.minute_var.get())
            
            if not (0 <= hour <= 23):
                messagebox.showerror("Error", "La hora debe estar entre 00 y 23")
                return
            
            if not (0 <= minute <= 59):
                messagebox.showerror("Error", "Los minutos deben estar entre 00 y 59")
                return
            
            time_str = f"{hour:02d}:{minute:02d}"
            
        except ValueError:
            messagebox.showerror("Error", "Por favor ingresa valores numéricos válidos")
            return
        
        action = self.action_var.get()
        
        # Programar la acción
        success, message = self.scheduler.schedule_action(
            time_str,
            action,
            warning_callback=self._show_warning,
            completion_callback=self._on_completion
        )
        
        if success:
            # Actualizar la interfaz
            self.schedule_button.config(state=tk.DISABLED)
            self.cancel_button.config(state=tk.NORMAL)
            self.status_label.config(text=f"Estado: {message}", foreground="green")
            
            # Deshabilitar los campos de entrada
            self.hour_var.set(f"{hour:02d}")
            self.minute_var.set(f"{minute:02d}")
            
            messagebox.showinfo("Éxito", message)
        else:
            messagebox.showerror("Error", message)
    
    def _on_cancel_click(self):
        """Manejar el clic en el botón Cancelar"""
        # Confirmar cancelación
        if messagebox.askyesno("Confirmar", "¿Deseas cancelar la acción programada?"):
            success, message = self.scheduler.cancel_scheduled_action()
            
            if success:
                # Cerrar ventana de advertencia si está abierta
                if self.warning_window:
                    self.warning_window.destroy()
                    self.warning_window = None
                    self.countdown_active = False
                
                # Actualizar la interfaz
                self._reset_interface()
                messagebox.showinfo("Cancelado", message)
            else:
                messagebox.showerror("Error", message)
    
    def _show_warning(self, seconds_remaining: int):
        """
        Mostrar ventana de advertencia antes de ejecutar la acción
        
        Args:
            seconds_remaining: Segundos restantes hasta la ejecución
        """
        if self.warning_window is not None:
            return  # Ya hay una ventana de advertencia abierta
        
        self.countdown_active = True
        
        # Crear ventana de advertencia
        self.warning_window = tk.Toplevel(self.root)
        self.warning_window.title("⚠️ Advertencia")
        self.warning_window.geometry("350x200")
        self.warning_window.resizable(False, False)
        
        # Centrar la ventana
        self.warning_window.update_idletasks()
        width = self.warning_window.winfo_width()
        height = self.warning_window.winfo_height()
        x = (self.warning_window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.warning_window.winfo_screenheight() // 2) - (height // 2)
        self.warning_window.geometry(f'{width}x{height}+{x}+{y}')
        
        # Hacer que la ventana esté siempre al frente
        self.warning_window.attributes('-topmost', True)
        
        # Frame principal
        warning_frame = ttk.Frame(self.warning_window, padding="20")
        warning_frame.pack(fill=tk.BOTH, expand=True)
        
        # Icono y mensaje
        icon_label = ttk.Label(
            warning_frame,
            text="⚠️",
            font=("Arial", 40)
        )
        icon_label.pack(pady=(0, 10))
        
        action_text = self.action_var.get().lower()
        message_label = ttk.Label(
            warning_frame,
            text=f"El sistema se va a {action_text} en:",
            font=("Arial", 11)
        )
        message_label.pack()
        
        # Contador
        self.countdown_label = ttk.Label(
            warning_frame,
            text=f"{seconds_remaining} segundos",
            font=("Arial", 20, "bold"),
            foreground="red"
        )
        self.countdown_label.pack(pady=15)
        
        # Botón de cancelar
        cancel_warning_button = ttk.Button(
            warning_frame,
            text="Cancelar Acción",
            command=self._on_cancel_click
        )
        cancel_warning_button.pack()
        
        # Iniciar cuenta regresiva
        self._update_countdown(seconds_remaining)
        
        # Manejar el cierre de la ventana
        self.warning_window.protocol("WM_DELETE_WINDOW", lambda: None)  # Deshabilitar cierre con X
    
    def _update_countdown(self, seconds: int):
        """
        Actualizar la cuenta regresiva en la ventana de advertencia
        
        Args:
            seconds: Segundos restantes
        """
        if not self.countdown_active or self.warning_window is None:
            return
        
        if seconds > 0:
            self.countdown_label.config(text=f"{seconds} segundos")
            self.warning_window.after(1000, lambda: self._update_countdown(seconds - 1))
        else:
            self.countdown_label.config(text="Ejecutando...")
    
    def _on_completion(self, cancelled: bool):
        """
        Callback cuando se completa o cancela la acción
        
        Args:
            cancelled: True si fue cancelado, False si se ejecutó
        """
        # Cerrar ventana de advertencia si está abierta
        if self.warning_window:
            self.warning_window.destroy()
            self.warning_window = None
            self.countdown_active = False
        
        if not cancelled:
            # La acción se ejecutó, cerrar la aplicación
            self.root.after(100, self.root.quit)
    
    def _reset_interface(self):
        """Resetear la interfaz al estado inicial"""
        self.schedule_button.config(state=tk.NORMAL)
        self.cancel_button.config(state=tk.DISABLED)
        self.status_label.config(text="Estado: Esperando...", foreground="gray")
        self.time_remaining_label.config(text="")
    
    def _update_status(self):
        """Actualizar el estado y tiempo restante periódicamente"""
        if self.scheduler.is_action_scheduled():
            remaining = self.scheduler.get_remaining_time()
            if remaining:
                self.time_remaining_label.config(text=f"Tiempo restante: {remaining}")
        else:
            self.time_remaining_label.config(text="")
        
        # Actualizar cada segundo
        self.root.after(1000, self._update_status)
    
    def _on_closing(self):
        """Manejar el cierre de la ventana principal"""
        if self.scheduler.is_action_scheduled():
            if messagebox.askyesno(
                "Confirmar salida",
                "Hay una acción programada. ¿Deseas cancelarla y salir?"
            ):
                self.scheduler.cancel_scheduled_action()
                self.root.quit()
        else:
            self.root.quit()

# Made with Bob
