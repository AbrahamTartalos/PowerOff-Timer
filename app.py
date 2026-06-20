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
    
    # Paleta de colores - Tema oscuro elegante
    COLORS = {
        'bg_dark': '#1a1a2e',           # Fondo principal oscuro
        'bg_medium': '#16213e',         # Fondo medio
        'bg_light': '#0f3460',          # Fondo claro
        'accent_cyan': '#00d9ff',       # Acento cyan brillante
        'accent_green': '#00ff88',      # Acento verde brillante
        'text_primary': '#e8e8e8',      # Texto principal
        'text_secondary': '#a0a0a0',    # Texto secundario
        'success': '#00ff88',           # Verde éxito
        'warning': '#ffa500',           # Naranja advertencia
        'error': '#ff4757',             # Rojo error
        'button_hover': '#1a5490',      # Hover de botones
    }
    
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
        
        # Configurar estilos personalizados
        self._setup_styles()
        
        # Configurar la ventana principal
        self._setup_window()
        
        # Crear la interfaz
        self._create_widgets()
        
        # Iniciar actualización del estado
        self._update_status()
    
    def _setup_styles(self):
        """Configurar estilos personalizados para ttk"""
        style = ttk.Style()
        
        # Configurar tema base
        style.theme_use('clam')
        
        # Estilo para Frame
        style.configure(
            'Dark.TFrame',
            background=self.COLORS['bg_dark']
        )
        
        # Estilo para Label
        style.configure(
            'Dark.TLabel',
            background=self.COLORS['bg_dark'],
            foreground=self.COLORS['text_primary'],
            font=('Segoe UI', 10)
        )
        
        style.configure(
            'Title.TLabel',
            background=self.COLORS['bg_dark'],
            foreground=self.COLORS['accent_cyan'],
            font=('Segoe UI', 16, 'bold')
        )
        
        style.configure(
            'Status.TLabel',
            background=self.COLORS['bg_dark'],
            foreground=self.COLORS['text_secondary'],
            font=('Segoe UI', 9)
        )
        
        style.configure(
            'Time.TLabel',
            background=self.COLORS['bg_dark'],
            foreground=self.COLORS['accent_green'],
            font=('Segoe UI', 11, 'bold')
        )
        
        # Estilo para Entry
        style.configure(
            'Dark.TEntry',
            fieldbackground=self.COLORS['bg_light'],
            foreground=self.COLORS['text_primary'],
            bordercolor=self.COLORS['accent_cyan'],
            lightcolor=self.COLORS['accent_cyan'],
            darkcolor=self.COLORS['bg_medium'],
            insertcolor=self.COLORS['accent_cyan']
        )
        
        # Estilo para Combobox
        style.configure(
            'Dark.TCombobox',
            fieldbackground=self.COLORS['bg_light'],
            background=self.COLORS['bg_light'],
            foreground=self.COLORS['text_primary'],
            arrowcolor=self.COLORS['accent_cyan'],
            bordercolor=self.COLORS['accent_cyan'],
            lightcolor=self.COLORS['accent_cyan'],
            darkcolor=self.COLORS['bg_medium']
        )
        
        style.map('Dark.TCombobox',
            fieldbackground=[('readonly', self.COLORS['bg_light'])],
            selectbackground=[('readonly', self.COLORS['bg_light'])],
            selectforeground=[('readonly', self.COLORS['text_primary'])]
        )
        
        # Estilo para botón Programar
        style.configure(
            'Schedule.TButton',
            background=self.COLORS['accent_green'],
            foreground='#000000',
            borderwidth=0,
            focuscolor='none',
            font=('Segoe UI', 10, 'bold'),
            padding=(20, 10)
        )
        
        style.map('Schedule.TButton',
            background=[
                ('active', '#00cc70'),
                ('disabled', self.COLORS['bg_medium'])
            ],
            foreground=[
                ('disabled', self.COLORS['text_secondary'])
            ]
        )
        
        # Estilo para botón Cancelar
        style.configure(
            'Cancel.TButton',
            background=self.COLORS['error'],
            foreground='#ffffff',
            borderwidth=0,
            focuscolor='none',
            font=('Segoe UI', 10, 'bold'),
            padding=(20, 10)
        )
        
        style.map('Cancel.TButton',
            background=[
                ('active', '#ff3344'),
                ('disabled', self.COLORS['bg_medium'])
            ],
            foreground=[
                ('disabled', self.COLORS['text_secondary'])
            ]
        )
    
    def _setup_window(self):
        """Configurar la ventana principal"""
        self.root.title("⚡ PowerOff-Timer")
        self.root.geometry("450x380")
        self.root.resizable(False, False)
        self.root.configure(bg=self.COLORS['bg_dark'])
        
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
        # Frame principal con padding y estilo oscuro
        main_frame = ttk.Frame(self.root, padding="30", style='Dark.TFrame')
        main_frame.grid(row=0, column=0, sticky=tk.W+tk.E+tk.N+tk.S)
        
        # Título con icono
        title_label = ttk.Label(
            main_frame,
            text="⚡ Programar Apagado del Sistema",
            style='Title.TLabel'
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 30))
        
        # Separador decorativo
        separator1 = tk.Frame(main_frame, height=2, bg=self.COLORS['accent_cyan'])
        separator1.grid(row=1, column=0, columnspan=2, sticky=tk.W+tk.E, pady=(0, 20))
        
        # Label y entrada para la hora
        time_label = ttk.Label(
            main_frame,
            text="🕐 Hora (HH:MM):",
            style='Dark.TLabel'
        )
        time_label.grid(row=2, column=0, sticky=tk.W, pady=10)
        
        # Frame para la entrada de hora con fondo
        time_frame = tk.Frame(main_frame, bg=self.COLORS['bg_dark'])
        time_frame.grid(row=2, column=1, sticky=tk.W+tk.E, pady=10)
        
        # Entrada de hora con validación y estilo
        self.hour_var = tk.StringVar()
        self.minute_var = tk.StringVar()
        
        hour_entry = tk.Entry(
            time_frame,
            textvariable=self.hour_var,
            width=5,
            justify="center",
            bg=self.COLORS['bg_light'],
            fg=self.COLORS['text_primary'],
            insertbackground=self.COLORS['accent_cyan'],
            font=('Segoe UI', 12, 'bold'),
            relief=tk.FLAT,
            borderwidth=2,
            highlightthickness=2,
            highlightbackground=self.COLORS['bg_medium'],
            highlightcolor=self.COLORS['accent_cyan']
        )
        hour_entry.grid(row=0, column=0, padx=(0, 5))
        
        separator_label = tk.Label(
            time_frame,
            text=":",
            bg=self.COLORS['bg_dark'],
            fg=self.COLORS['accent_cyan'],
            font=('Segoe UI', 14, 'bold')
        )
        separator_label.grid(row=0, column=1)
        
        minute_entry = tk.Entry(
            time_frame,
            textvariable=self.minute_var,
            width=5,
            justify="center",
            bg=self.COLORS['bg_light'],
            fg=self.COLORS['text_primary'],
            insertbackground=self.COLORS['accent_cyan'],
            font=('Segoe UI', 12, 'bold'),
            relief=tk.FLAT,
            borderwidth=2,
            highlightthickness=2,
            highlightbackground=self.COLORS['bg_medium'],
            highlightcolor=self.COLORS['accent_cyan']
        )
        minute_entry.grid(row=0, column=2, padx=(5, 0))
        
        # Placeholder text
        self.hour_var.set("00")
        self.minute_var.set("00")
        
        # Label y selector de acción
        action_label = ttk.Label(
            main_frame,
            text="⚙️ Acción:",
            style='Dark.TLabel'
        )
        action_label.grid(row=3, column=0, sticky=tk.W, pady=10)
        
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
            width=20,
            style='Dark.TCombobox',
            font=('Segoe UI', 10)
        )
        action_combo.grid(row=3, column=1, sticky=tk.W+tk.E, pady=10)
        action_combo.current(0)  # Seleccionar "Apagar" por defecto
        
        # Separador decorativo
        separator2 = tk.Frame(main_frame, height=2, bg=self.COLORS['accent_cyan'])
        separator2.grid(row=4, column=0, columnspan=2, sticky=tk.W+tk.E, pady=(20, 20))
        
        # Frame para los botones
        button_frame = tk.Frame(main_frame, bg=self.COLORS['bg_dark'])
        button_frame.grid(row=5, column=0, columnspan=2, pady=10)
        
        # Botón Programar
        self.schedule_button = ttk.Button(
            button_frame,
            text="▶ Programar",
            command=self._on_schedule_click,
            style='Schedule.TButton',
            width=15
        )
        self.schedule_button.grid(row=0, column=0, padx=8)
        
        # Botón Cancelar
        self.cancel_button = ttk.Button(
            button_frame,
            text="✕ Cancelar",
            command=self._on_cancel_click,
            state=tk.DISABLED,
            style='Cancel.TButton',
            width=15
        )
        self.cancel_button.grid(row=0, column=1, padx=8)
        
        # Label de estado
        self.status_label = ttk.Label(
            main_frame,
            text="Estado: Esperando...",
            style='Status.TLabel'
        )
        self.status_label.grid(row=6, column=0, columnspan=2, pady=(15, 5))
        
        # Label de tiempo restante
        self.time_remaining_label = ttk.Label(
            main_frame,
            text="",
            style='Time.TLabel'
        )
        self.time_remaining_label.grid(row=7, column=0, columnspan=2, pady=5)
        
        # Configurar el grid para que se expanda
        main_frame.columnconfigure(1, weight=1)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
    
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
                messagebox.showinfo("✓ Cancelado", message)
            else:
                messagebox.showerror("✕ Error", message)
    
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
        self.warning_window.title("⚠️ Advertencia del Sistema")
        self.warning_window.geometry("500x400")
        self.warning_window.resizable(False, False)
        self.warning_window.configure(bg=self.COLORS['bg_dark'])
        
        # Hacer que la ventana esté siempre al frente ANTES de centrarla
        self.warning_window.attributes('-topmost', True)
        
        # Forzar el foco en la ventana
        self.warning_window.focus_force()
        
        # Centrar la ventana
        self.warning_window.update_idletasks()
        width = self.warning_window.winfo_width()
        height = self.warning_window.winfo_height()
        x = (self.warning_window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.warning_window.winfo_screenheight() // 2) - (height // 2)
        self.warning_window.geometry(f'{width}x{height}+{x}+{y}')
        
        # Traer la ventana al frente después de posicionarla
        self.warning_window.lift()
        self.warning_window.focus_force()
        
        # Frame principal con fondo oscuro
        warning_frame = tk.Frame(
            self.warning_window,
            bg=self.COLORS['bg_dark'],
            padx=30,
            pady=30
        )
        warning_frame.pack(fill=tk.BOTH, expand=True)
        
        # Borde decorativo superior
        top_border = tk.Frame(warning_frame, height=3, bg=self.COLORS['warning'])
        top_border.pack(fill=tk.X, pady=(0, 20))
        
        # Icono y mensaje
        icon_label = tk.Label(
            warning_frame,
            text="⚠️",
            font=("Segoe UI", 50),
            bg=self.COLORS['bg_dark'],
            fg=self.COLORS['warning']
        )
        icon_label.pack(pady=(0, 15))
        
        action_text = self.action_var.get().lower()
        message_label = tk.Label(
            warning_frame,
            text=f"El sistema se va a {action_text} en:",
            font=("Arial", 13),
            bg=self.COLORS['bg_dark'],
            fg=self.COLORS['text_primary']
        )
        message_label.pack(pady=(0, 15))
        
        # Contador con tamaño apropiado
        self.countdown_label = tk.Label(
            warning_frame,
            text=str(seconds_remaining),
            font=("Arial", 56, "bold"),
            bg=self.COLORS['bg_dark'],
            fg="#00FF00",
            width=3
        )
        self.countdown_label.pack(pady=15)
        
        seconds_text = tk.Label(
            warning_frame,
            text="segundos",
            font=("Arial", 12),
            bg=self.COLORS['bg_dark'],
            fg=self.COLORS['text_primary']
        )
        seconds_text.pack(pady=(0, 15))
        
        # Botón de cancelar estilizado
        cancel_warning_button = tk.Button(
            warning_frame,
            text="✕ CANCELAR ACCIÓN",
            command=self._on_cancel_click,
            bg=self.COLORS['error'],
            fg='#ffffff',
            font=('Segoe UI', 11, 'bold'),
            relief=tk.FLAT,
            padx=30,
            pady=12,
            cursor='hand2',
            activebackground='#ff3344',
            activeforeground='#ffffff'
        )
        cancel_warning_button.pack(pady=(10, 0))
        
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
        
        try:
            if seconds > 0:
                # Actualizar el texto del label con colores fijos y visibles
                self.countdown_label.config(text=str(seconds))
                
                # Cambiar color según el tiempo restante
                if seconds <= 5:
                    self.countdown_label.config(fg="#FF0000")  # Rojo brillante
                elif seconds <= 10:
                    self.countdown_label.config(fg="#FFA500")  # Naranja
                else:
                    self.countdown_label.config(fg="#00FF00")  # Verde brillante
                
                # Forzar actualización visual inmediata
                self.countdown_label.update()
                
                # Programar siguiente actualización
                self.warning_window.after(1000, lambda: self._update_countdown(seconds - 1))
            else:
                self.countdown_label.config(
                    text="⚡",
                    fg="#00FFFF"
                )
                self.countdown_label.update()
        except tk.TclError:
            # La ventana fue cerrada
            self.countdown_active = False
    
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
        self.status_label.config(
            text="Estado: Esperando...",
            foreground=self.COLORS['text_secondary']
        )
        self.time_remaining_label.config(text="")
    
    def _update_status(self):
        """Actualizar el estado y tiempo restante periódicamente"""
        if self.scheduler.is_action_scheduled():
            remaining = self.scheduler.get_remaining_time()
            if remaining:
                self.time_remaining_label.config(
                    text=f"⏱️ Tiempo restante: {remaining}"
                )
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
