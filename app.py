"""
PowerOff-Timer - Interfaz gráfica de usuario
Maneja la interfaz Tkinter y la interacción con el usuario
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading
from scheduler import SystemScheduler
from screen_controller import ScreenController


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
        self.screen_controller = ScreenController()
        self.warning_window = None
        self.countdown_active = False
        
        # Configurar estilos personalizados
        self._setup_styles()
        
        # Configurar la ventana principal
        self._setup_window()
        
        # Crear la barra de menú
        self._create_menu_bar()
        
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
        
        # Estilo para Notebook (pestañas)
        style.configure(
            'Dark.TNotebook',
            background=self.COLORS['bg_dark'],
            borderwidth=0,
            tabmargins=[2, 5, 2, 0]
        )
        
        style.configure(
            'Dark.TNotebook.Tab',
            background=self.COLORS['bg_medium'],
            foreground=self.COLORS['text_primary'],
            padding=[20, 10],
            font=('Segoe UI', 10, 'bold'),
            borderwidth=1
        )
        
        style.map('Dark.TNotebook.Tab',
            background=[
                ('selected', self.COLORS['bg_light']),
                ('active', self.COLORS['button_hover'])
            ],
            foreground=[
                ('selected', self.COLORS['accent_cyan']),
                ('active', self.COLORS['text_primary'])
            ],
            padding=[
                ('selected', [20, 12]),  # Ligeramente más grande cuando está seleccionada
                ('!selected', [20, 10])
            ],
            font=[
                ('selected', ('Segoe UI', 10, 'bold')),
                ('!selected', ('Segoe UI', 10, 'bold'))
            ]
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
        self.root.geometry("500x510")
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
    
    def _create_menu_bar(self):
        """Crear la barra de menú de la aplicación"""
        menubar = tk.Menu(self.root, bg=self.COLORS['bg_medium'], fg=self.COLORS['text_primary'])
        self.root.config(menu=menubar)
        
        # Menú Ayuda
        help_menu = tk.Menu(
            menubar,
            tearoff=0,
            bg=self.COLORS['bg_medium'],
            fg=self.COLORS['text_primary'],
            activebackground=self.COLORS['accent_cyan'],
            activeforeground='#000000'
        )
        menubar.add_cascade(label="Ayuda", menu=help_menu)
        help_menu.add_command(label="Acerca de", command=self._show_about_dialog)
    
    def _show_about_dialog(self):
        """Mostrar ventana de diálogo 'Acerca de'"""
        # Crear ventana modal
        about_window = tk.Toplevel(self.root)
        about_window.title("Acerca de PowerOff-Timer")
        about_window.geometry("400x350")
        about_window.resizable(False, False)
        about_window.configure(bg=self.COLORS['bg_dark'])
        
        # Hacer la ventana modal
        about_window.transient(self.root)
        about_window.grab_set()
        
        # Centrar la ventana
        about_window.update_idletasks()
        width = about_window.winfo_width()
        height = about_window.winfo_height()
        x = (about_window.winfo_screenwidth() // 2) - (width // 2)
        y = (about_window.winfo_screenheight() // 2) - (height // 2)
        about_window.geometry(f'{width}x{height}+{x}+{y}')
        
        # Frame principal
        main_frame = tk.Frame(
            about_window,
            bg=self.COLORS['bg_dark'],
            padx=30,
            pady=20
        )
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Borde decorativo superior
        top_border = tk.Frame(main_frame, height=3, bg=self.COLORS['accent_cyan'])
        top_border.pack(fill=tk.X, pady=(0, 20))
        
        # Icono y nombre de la app
        app_name_label = tk.Label(
            main_frame,
            text="⚡ PowerOff-Timer",
            font=("Segoe UI", 20, "bold"),
            bg=self.COLORS['bg_dark'],
            fg=self.COLORS['accent_cyan']
        )
        app_name_label.pack(pady=(0, 5))
        
        # Versión
        version_label = tk.Label(
            main_frame,
            text="v2.0",
            font=("Segoe UI", 11),
            bg=self.COLORS['bg_dark'],
            fg=self.COLORS['text_secondary']
        )
        version_label.pack(pady=(0, 20))
        
        # Separador
        separator = tk.Frame(main_frame, height=1, bg=self.COLORS['bg_light'])
        separator.pack(fill=tk.X, pady=(0, 20))
        
        # Información del desarrollador
        dev_label = tk.Label(
            main_frame,
            text="Desarrollador",
            font=("Segoe UI", 10, "bold"),
            bg=self.COLORS['bg_dark'],
            fg=self.COLORS['text_primary']
        )
        dev_label.pack(pady=(0, 5))
        
        dev_name_label = tk.Label(
            main_frame,
            text="Abraham Tartalos",
            font=("Segoe UI", 11),
            bg=self.COLORS['bg_dark'],
            fg=self.COLORS['accent_green']
        )
        dev_name_label.pack(pady=(0, 15))
        
        # Copyright
        copyright_label = tk.Label(
            main_frame,
            text="© 2026",
            font=("Segoe UI", 9),
            bg=self.COLORS['bg_dark'],
            fg=self.COLORS['text_secondary']
        )
        copyright_label.pack(pady=(0, 15))
        
        # GitHub
        github_frame = tk.Frame(main_frame, bg=self.COLORS['bg_dark'])
        github_frame.pack(pady=(0, 5))
        
        github_icon = tk.Label(
            github_frame,
            text="🔗",
            font=("Segoe UI", 11),
            bg=self.COLORS['bg_dark'],
            fg=self.COLORS['text_primary']
        )
        github_icon.pack(side=tk.LEFT, padx=(0, 5))
        
        github_label = tk.Label(
            github_frame,
            text="https://github.com/AbrahamTartalos",
            font=("Segoe UI", 9, "underline"),
            bg=self.COLORS['bg_dark'],
            fg=self.COLORS['accent_cyan'],
            cursor="hand2"
        )
        github_label.pack(side=tk.LEFT)
        
        # Hacer el link clickeable
        github_label.bind("<Button-1>", lambda e: self._open_url("https://github.com/AbrahamTartalos"))
        
        # Email
        email_frame = tk.Frame(main_frame, bg=self.COLORS['bg_dark'])
        email_frame.pack(pady=(0, 20))
        
        email_icon = tk.Label(
            email_frame,
            text="📧",
            font=("Segoe UI", 11),
            bg=self.COLORS['bg_dark'],
            fg=self.COLORS['text_primary']
        )
        email_icon.pack(side=tk.LEFT, padx=(0, 5))
        
        # Entry de solo lectura para permitir selección y copia
        email_entry = tk.Entry(
            email_frame,
            font=("Segoe UI", 9),
            bg=self.COLORS['bg_dark'],
            fg=self.COLORS['text_primary'],
            relief=tk.FLAT,
            borderwidth=0,
            readonlybackground=self.COLORS['bg_dark'],
            highlightthickness=0,
            width=28,
            justify=tk.CENTER
        )
        email_entry.insert(0, "abrahamrtartalos@gmail.com")
        email_entry.config(state='readonly')
        email_entry.pack(side=tk.LEFT)
        
        # Botón Cerrar
        close_button = tk.Button(
            main_frame,
            text="Cerrar",
            command=about_window.destroy,
            bg=self.COLORS['accent_cyan'],
            fg='#000000',
            font=('Segoe UI', 10, 'bold'),
            relief=tk.FLAT,
            padx=30,
            pady=8,
            cursor='hand2',
            activebackground=self.COLORS['button_hover'],
            activeforeground='#ffffff'
        )
        close_button.pack(pady=(10, 0))
        
        # Foco en el botón cerrar
        close_button.focus_set()
        
        # Permitir cerrar con ESC
        about_window.bind('<Escape>', lambda e: about_window.destroy())
    
    def _open_url(self, url: str):
        """Abrir URL en el navegador predeterminado"""
        import webbrowser
        webbrowser.open(url)
    
    def _create_widgets(self):
        """Crear todos los widgets de la interfaz"""
        # Frame principal con padding y estilo oscuro
        main_frame = ttk.Frame(self.root, padding="20", style='Dark.TFrame')
        main_frame.grid(row=0, column=0, sticky=tk.W+tk.E+tk.N+tk.S)
        
        # Título principal
        title_label = ttk.Label(
            main_frame,
            text="⚡ PowerOff-Timer",
            style='Title.TLabel'
        )
        title_label.grid(row=0, column=0, pady=(0, 20))
        
        # Crear Notebook (sistema de pestañas)
        self.notebook = ttk.Notebook(main_frame, style='Dark.TNotebook')
        self.notebook.grid(row=1, column=0, sticky=tk.W+tk.E+tk.N+tk.S, pady=(0, 10))
        
        # Crear pestañas
        self._create_shutdown_tab()
        self._create_screen_control_tab()
        
        # Configurar el grid
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
    
    def _create_shutdown_tab(self):
        """Crear la pestaña de programación de apagado"""
        # Frame para la pestaña
        shutdown_frame = ttk.Frame(self.notebook, style='Dark.TFrame', padding="20")
        self.notebook.add(shutdown_frame, text="🔌 Programar Apagado")
        
        # Título de la sección
        section_title = ttk.Label(
            shutdown_frame,
            text="Programar Apagado del Sistema",
            style='Dark.TLabel',
            font=('Segoe UI', 12, 'bold'),
            foreground=self.COLORS['accent_cyan']
        )
        section_title.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Separador decorativo
        separator1 = tk.Frame(shutdown_frame, height=2, bg=self.COLORS['accent_cyan'])
        separator1.grid(row=1, column=0, columnspan=2, sticky=tk.W+tk.E, pady=(0, 20))
        
        # Label y entrada para la hora
        time_label = ttk.Label(
            shutdown_frame,
            text="🕐 Hora (HH:MM):",
            style='Dark.TLabel'
        )
        time_label.grid(row=2, column=0, sticky=tk.W, pady=10)
        
        # Frame para la entrada de hora con fondo
        time_frame = tk.Frame(shutdown_frame, bg=self.COLORS['bg_dark'])
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
            shutdown_frame,
            text="⚙️ Acción:",
            style='Dark.TLabel'
        )
        action_label.grid(row=3, column=0, sticky=tk.W, pady=10)
        
        self.action_var = tk.StringVar()
        action_combo = ttk.Combobox(
            shutdown_frame,
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
        separator2 = tk.Frame(shutdown_frame, height=2, bg=self.COLORS['accent_cyan'])
        separator2.grid(row=4, column=0, columnspan=2, sticky=tk.W+tk.E, pady=(20, 20))
        
        # Frame para los botones
        button_frame = tk.Frame(shutdown_frame, bg=self.COLORS['bg_dark'])
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
            shutdown_frame,
            text="Estado: Esperando...",
            style='Status.TLabel'
        )
        self.status_label.grid(row=6, column=0, columnspan=2, pady=(15, 5))
        
        # Label de tiempo restante
        self.time_remaining_label = ttk.Label(
            shutdown_frame,
            text="",
            style='Time.TLabel'
        )
        self.time_remaining_label.grid(row=7, column=0, columnspan=2, pady=5)
        
        # Configurar el grid para que se expanda
        shutdown_frame.columnconfigure(1, weight=1)
    
    def _create_screen_control_tab(self):
        """Crear la pestaña de control de pantalla"""
        # Frame para la pestaña
        screen_frame = ttk.Frame(self.notebook, style='Dark.TFrame', padding="20")
        self.notebook.add(screen_frame, text="🖥️ Control de Pantalla")
        
        # Título de la sección
        section_title = ttk.Label(
            screen_frame,
            text="Control de Tiempo de Apagado de Pantalla",
            style='Dark.TLabel',
            font=('Segoe UI', 12, 'bold'),
            foreground=self.COLORS['accent_cyan']
        )
        section_title.grid(row=0, column=0, columnspan=2, pady=(0, 15))
        
        # Descripción
        description = ttk.Label(
            screen_frame,
            text="Configura el tiempo de inactividad antes de que\nla pantalla se apague automáticamente.",
            style='Dark.TLabel',
            font=('Segoe UI', 9),
            foreground=self.COLORS['text_secondary'],
            justify=tk.CENTER
        )
        description.grid(row=1, column=0, columnspan=2, pady=(0, 20))
        
        # Separador decorativo
        separator = tk.Frame(screen_frame, height=2, bg=self.COLORS['accent_cyan'])
        separator.grid(row=2, column=0, columnspan=2, sticky=tk.W+tk.E, pady=(0, 20))
        
        # Configuración actual
        self.current_config_label = ttk.Label(
            screen_frame,
            text="Cargando configuración actual...",
            style='Dark.TLabel',
            font=('Segoe UI', 9),
            foreground=self.COLORS['accent_green']
        )
        self.current_config_label.grid(row=3, column=0, columnspan=2, pady=(0, 20))
        
        # Label para selección de tiempo
        time_select_label = ttk.Label(
            screen_frame,
            text="⏱️ Tiempo de apagado:",
            style='Dark.TLabel'
        )
        time_select_label.grid(row=4, column=0, sticky=tk.W, pady=10)
        
        # Combobox para seleccionar tiempo
        self.screen_timeout_var = tk.StringVar()
        timeout_combo = ttk.Combobox(
            screen_frame,
            textvariable=self.screen_timeout_var,
            values=list(ScreenController.TIME_OPTIONS.keys()),
            state="readonly",
            width=20,
            style='Dark.TCombobox',
            font=('Segoe UI', 10)
        )
        timeout_combo.grid(row=4, column=1, sticky=tk.W+tk.E, pady=10)
        timeout_combo.current(2)  # Seleccionar "10 minutos" por defecto
        
        # Separador decorativo
        separator2 = tk.Frame(screen_frame, height=2, bg=self.COLORS['accent_cyan'])
        separator2.grid(row=5, column=0, columnspan=2, sticky=tk.W+tk.E, pady=(20, 20))
        
        # Frame para botones
        button_frame = tk.Frame(screen_frame, bg=self.COLORS['bg_dark'])
        button_frame.grid(row=6, column=0, columnspan=2, pady=10)
        
        # Botón Aplicar
        apply_button = ttk.Button(
            button_frame,
            text="✓ Aplicar Configuración",
            command=self._on_apply_screen_timeout,
            style='Schedule.TButton',
            width=25
        )
        apply_button.grid(row=0, column=0, padx=5)
        
        # Botón Actualizar
        refresh_button = ttk.Button(
            button_frame,
            text="🔄 Actualizar",
            command=self._load_current_screen_config,
            style='Cancel.TButton',
            width=15
        )
        refresh_button.grid(row=0, column=1, padx=5)
        
        # Label de estado de la operación
        self.screen_status_label = ttk.Label(
            screen_frame,
            text="",
            style='Status.TLabel'
        )
        self.screen_status_label.grid(row=7, column=0, columnspan=2, pady=(15, 5))
        
        # Configurar el grid
        screen_frame.columnconfigure(1, weight=1)
        
        # Cargar configuración actual al iniciar
        self.root.after(100, self._load_current_screen_config)
    def _load_current_screen_config(self):
        """Cargar y mostrar la configuración actual de tiempo de apagado de pantalla"""
        success, ac_minutes, dc_minutes, message = self.screen_controller.get_current_timeout()
        
        if success:
            ac_desc = self.screen_controller.get_timeout_description(ac_minutes)
            dc_desc = self.screen_controller.get_timeout_description(dc_minutes)
            
            self.current_config_label.config(
                text=f"📊 Configuración actual:\nConectado (AC): {ac_desc} | Batería (DC): {dc_desc}",
                foreground=self.COLORS['accent_green']
            )
            self.screen_status_label.config(text="")
        else:
            self.current_config_label.config(
                text=f"⚠️ Error al cargar configuración: {message}",
                foreground=self.COLORS['error']
            )
    
    def _on_apply_screen_timeout(self):
        """Aplicar el nuevo tiempo de apagado de pantalla"""
        selected_option = self.screen_timeout_var.get()
        
        if not selected_option:
            messagebox.showerror("Error", "Por favor selecciona un tiempo")
            return
        
        # Obtener los minutos correspondientes
        minutes = ScreenController.TIME_OPTIONS.get(selected_option)
        
        if minutes is None:
            messagebox.showerror("Error", "Opción inválida")
            return
        
        # Confirmar la acción
        if minutes == 0:
            confirm_msg = "¿Deseas configurar la pantalla para que NUNCA se apague automáticamente?"
        elif minutes == 60:
            confirm_msg = "¿Deseas configurar la pantalla para que se apague después de 1 hora?"
        elif minutes > 60:
            hours = minutes // 60
            remaining = minutes % 60
            if remaining == 0:
                confirm_msg = f"¿Deseas configurar la pantalla para que se apague después de {hours} hora{'s' if hours > 1 else ''}?"
            else:
                confirm_msg = f"¿Deseas configurar la pantalla para que se apague después de {hours} hora{'s' if hours > 1 else ''} y {remaining} minuto{'s' if remaining > 1 else ''}?"
        else:
            confirm_msg = f"¿Deseas configurar la pantalla para que se apague después de {minutes} minuto{'s' if minutes > 1 else ''}?"
        
        if not messagebox.askyesno("Confirmar", confirm_msg):
            return
        
        # Aplicar la configuración
        success, message = self.screen_controller.set_screen_timeout(minutes)
        
        if success:
            self.screen_status_label.config(
                text=f"✓ {message}",
                foreground=self.COLORS['success']
            )
            messagebox.showinfo("✓ Éxito", message)
            
            # Actualizar la configuración mostrada
            self.root.after(500, self._load_current_screen_config)
        else:
            self.screen_status_label.config(
                text=f"✕ Error: {message}",
                foreground=self.COLORS['error']
            )
            
            # Verificar si es un problema de permisos
            if "acceso" in message.lower() or "denied" in message.lower():
                messagebox.showerror(
                    "Error de Permisos",
                    f"{message}\n\nPuede que necesites ejecutar la aplicación como Administrador."
                )
            else:
                messagebox.showerror("Error", message)
    
    
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
