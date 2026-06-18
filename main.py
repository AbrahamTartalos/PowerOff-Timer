"""
PowerOff-Timer - Aplicación de escritorio para programar apagado del sistema
Punto de entrada principal de la aplicación
"""

import sys
import tkinter as tk
from tkinter import messagebox
from app import PowerOffTimerApp


def main():
    """
    Función principal que inicializa y ejecuta la aplicación
    """
    try:
        # Crear la ventana principal de Tkinter
        root = tk.Tk()
        
        # Crear la aplicación
        app = PowerOffTimerApp(root)
        
        # Iniciar el loop principal de la aplicación
        root.mainloop()
        
    except Exception as e:
        # Manejar cualquier error crítico
        error_msg = f"Error crítico al iniciar la aplicación:\n{str(e)}"
        print(error_msg, file=sys.stderr)
        
        # Intentar mostrar un mensaje de error gráfico
        try:
            root = tk.Tk()
            root.withdraw()  # Ocultar la ventana principal
            messagebox.showerror("Error", error_msg)
        except:
            pass
        
        sys.exit(1)


if __name__ == "__main__":
    main()

# Made with Bob
