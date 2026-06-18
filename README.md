# PowerOff-Timer ⏰

Aplicación de escritorio simple para programar el apagado, hibernación o suspensión de tu PC con Windows.

## 📋 Características

- ✅ Programar apagado del sistema a una hora específica
- ✅ Opciones de acción: Apagar, Hibernar o Suspender
- ✅ Advertencia 60 segundos antes de ejecutar la acción
- ✅ Botón de cancelación para detener la acción programada
- ✅ Interfaz gráfica simple e intuitiva con Tkinter
- ✅ Contador de tiempo restante en tiempo real

## 🖥️ Requisitos del Sistema

- **Sistema Operativo:** Windows 10 o superior
- **Python:** 3.7 o superior
- **Librerías:** Tkinter (incluida con Python)

## 📦 Instalación

### Opción 1: Ejecutar directamente con Python

1. Clona o descarga este repositorio:
```bash
git clone https://github.com/tu-usuario/PowerOff-Timer.git
cd PowerOff-Timer
```

2. Ejecuta la aplicación:
```bash
python main.py
```

### Opción 2: Crear ejecutable (opcional)

Si deseas crear un archivo `.exe` para ejecutar sin Python instalado:

1. Instala PyInstaller:
```bash
pip install pyinstaller
```

2. Crea el ejecutable:
```bash
pyinstaller --onefile --windowed --name PowerOff-Timer main.py
```

3. El ejecutable estará en la carpeta `dist/`

## 🚀 Uso

### Interfaz Principal

1. **Ingresa la hora** en formato 24 horas (HH:MM)
   - Ejemplo: `23:30` para las 11:30 PM
   - Ejemplo: `14:00` para las 2:00 PM

2. **Selecciona la acción** que deseas ejecutar:
   - **Apagar:** Apaga completamente el sistema
   - **Hibernar:** Guarda el estado actual y apaga (requiere hibernación habilitada)
   - **Suspender:** Pone el sistema en modo de bajo consumo

3. **Haz clic en "Programar"** para iniciar el temporizador

4. La aplicación mostrará:
   - Estado de la programación
   - Tiempo restante hasta la ejecución
   - Opción para cancelar en cualquier momento

### Advertencia Antes de Ejecutar

60 segundos antes de la hora programada:
- Se mostrará una ventana de advertencia
- Verás una cuenta regresiva
- Podrás cancelar la acción si cambias de opinión

### Cancelar una Acción Programada

- Haz clic en el botón **"Cancelar"** en cualquier momento
- Confirma la cancelación en el diálogo
- La aplicación volverá al estado inicial

## 📁 Estructura del Proyecto

```
PowerOff-Timer/
│
├── main.py          # Punto de entrada de la aplicación
├── app.py           # Interfaz gráfica con Tkinter
├── scheduler.py     # Lógica de programación y ejecución
├── README.md        # Este archivo
└── PLAN.md          # Documentación técnica del diseño
```

## 🔧 Detalles Técnicos

### Comandos del Sistema

La aplicación utiliza los siguientes comandos de Windows:

- **Apagar:** `shutdown /s /t 0`
- **Hibernar:** `shutdown /h`
- **Suspender:** `rundll32.exe powrprof.dll,SetSuspendState 0,1,0`

### Arquitectura

- **main.py:** Inicializa la aplicación y maneja errores globales
- **app.py:** Gestiona la interfaz gráfica y la interacción del usuario
- **scheduler.py:** Implementa la lógica de temporización usando threading

## ⚠️ Notas Importantes

1. **Permisos:** La aplicación necesita permisos para ejecutar comandos del sistema
2. **Hibernación:** Para usar la opción de hibernar, la hibernación debe estar habilitada en Windows
3. **Suspensión:** Algunos sistemas pueden no soportar suspensión por software
4. **Guardar trabajo:** Asegúrate de guardar tu trabajo antes de programar el apagado

## 🐛 Solución de Problemas

### La hibernación no funciona
- Verifica que la hibernación esté habilitada en Windows:
  ```cmd
  powercfg /hibernate on
  ```

### La suspensión no funciona
- Algunos sistemas no soportan suspensión por software
- Verifica la configuración de energía en el Panel de Control

### Error al ejecutar comandos
- Ejecuta la aplicación como administrador si es necesario
- Verifica que no haya políticas de grupo que bloqueen estos comandos

## 📝 Ejemplos de Uso

### Ejemplo 1: Apagar a medianoche
1. Ingresa: `00:00`
2. Selecciona: `Apagar`
3. Haz clic en: `Programar`

### Ejemplo 2: Hibernar después del trabajo
1. Ingresa: `18:30`
2. Selecciona: `Hibernar`
3. Haz clic en: `Programar`

### Ejemplo 3: Suspender para ahorrar energía
1. Ingresa: `22:00`
2. Selecciona: `Suspender`
3. Haz clic en: `Programar`

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Si encuentras un bug o tienes una sugerencia:

1. Abre un issue describiendo el problema o mejora
2. Si deseas contribuir código, haz un fork y envía un pull request

## 📄 Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.

## 👨‍💻 Autor

Desarrollado por Abraham Tartalos usando Python y Tkinter 

## 🔄 Versión

**v1.0.0** - Versión inicial
- Programación de apagado/hibernación/suspensión
- Interfaz gráfica con Tkinter
- Sistema de advertencia antes de ejecutar
- Cancelación de acciones programadas

---

**¿Preguntas o problemas?** Abre un issue en el repositorio.