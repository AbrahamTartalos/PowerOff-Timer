# PowerOff-Timer ⏰

Aplicación de escritorio completa para gestionar el apagado del sistema y el control de pantalla en Windows.

## 📋 Características

### 🔌 Programación de Apagado
- ✅ Programar apagado del sistema a una hora específica
- ✅ Opciones de acción: Apagar, Hibernar o Suspender
- ✅ Advertencia 60 segundos antes de ejecutar la acción
- ✅ Botón de cancelación para detener la acción programada
- ✅ Contador de tiempo restante en tiempo real

### 🖥️ Control de Pantalla
- ✅ Configurar tiempo de apagado automático de pantalla
- ✅ Opciones predefinidas: 1, 5, 10, 15, 30, 40 minutos, 1 hora o Nunca
- ✅ Aplicación simultánea para modo conectado (AC) y batería (DC)
- ✅ Visualización de configuración actual del sistema
- ✅ Interfaz intuitiva con sistema de pestañas

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

La aplicación cuenta con un sistema de pestañas que organiza las funcionalidades:

### 🔌 Pestaña: Programar Apagado

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

#### Advertencia Antes de Ejecutar

60 segundos antes de la hora programada:
- Se mostrará una ventana de advertencia
- Verás una cuenta regresiva
- Podrás cancelar la acción si cambias de opinión

#### Cancelar una Acción Programada

- Haz clic en el botón **"Cancelar"** en cualquier momento
- Confirma la cancelación en el diálogo
- La aplicación volverá al estado inicial

### 🖥️ Pestaña: Control de Pantalla

Esta funcionalidad te permite configurar el tiempo de inactividad antes de que la pantalla se apague automáticamente.

1. **Visualiza la configuración actual:**
   - Al abrir la pestaña, verás la configuración actual para modo conectado (AC) y batería (DC)
   - Usa el botón "🔄 Actualizar" para recargar la configuración

2. **Selecciona el tiempo de apagado:**
   - **1 minuto:** Para apagado rápido
   - **5 minutos:** Ideal para pausas cortas
   - **10 minutos:** Configuración equilibrada (predeterminada)
   - **15 minutos:** Para trabajo continuo
   - **30 minutos:** Para sesiones largas
   - **40 minutos:** Para presentaciones
   - **1 hora:** Para trabajo extendido
   - **Nunca:** La pantalla nunca se apagará automáticamente

3. **Aplica la configuración:**
   - Haz clic en "✓ Aplicar Configuración"
   - Confirma la acción en el diálogo
   - La configuración se aplicará tanto para modo conectado como batería

4. **Verifica el resultado:**
   - La aplicación mostrará un mensaje de éxito
   - La configuración actual se actualizará automáticamente

> **⚠️ Nota:** Esta funcionalidad puede requerir permisos de administrador en algunos sistemas. Si encuentras errores de acceso, ejecuta la aplicación como administrador.

## 📁 Estructura del Proyecto

```
PowerOff-Timer/
│
├── main.py              # Punto de entrada de la aplicación
├── app.py               # Interfaz gráfica con Tkinter (sistema de pestañas)
├── scheduler.py         # Lógica de programación y ejecución de apagado
├── screen_controller.py # Control de tiempo de apagado de pantalla
├── icon.ico             # Icono de la aplicación
├── build_exe.bat        # Script para crear ejecutable
├── README.md            # Este archivo
└── PLAN.md              # Documentación técnica del diseño
```

## 🔧 Detalles Técnicos

### Comandos del Sistema

#### Programación de Apagado
La aplicación utiliza los siguientes comandos de Windows:

- **Apagar:** `shutdown /s /t 0`
- **Hibernar:** `shutdown /h`
- **Suspender:** `rundll32.exe powrprof.dll,SetSuspendState 0,1,0`

#### Control de Pantalla
Utiliza el comando `powercfg` de Windows:

- **Consultar configuración:** `powercfg /query SCHEME_CURRENT SUB_VIDEO VIDEOIDLE`
- **Configurar AC (conectado):** `powercfg /change monitor-timeout-ac [minutos]`
- **Configurar DC (batería):** `powercfg /change monitor-timeout-dc [minutos]`

### Arquitectura

- **main.py:** Inicializa la aplicación y maneja errores globales
- **app.py:** Gestiona la interfaz gráfica con sistema de pestañas y la interacción del usuario
- **scheduler.py:** Implementa la lógica de temporización usando threading
- **screen_controller.py:** Gestiona la configuración de tiempo de apagado de pantalla mediante powercfg

## ⚠️ Notas Importantes

### Programación de Apagado
1. **Permisos:** La aplicación necesita permisos para ejecutar comandos del sistema
2. **Hibernación:** Para usar la opción de hibernar, la hibernación debe estar habilitada en Windows
3. **Suspensión:** Algunos sistemas pueden no soportar suspensión por software
4. **Guardar trabajo:** Asegúrate de guardar tu trabajo antes de programar el apagado

### Control de Pantalla
1. **Permisos de Administrador:** En algunos sistemas, modificar la configuración de energía puede requerir permisos de administrador
2. **Aplicación Global:** Los cambios afectan tanto al modo conectado (AC) como al modo batería (DC)
3. **Persistencia:** La configuración se mantiene incluso después de cerrar la aplicación
4. **Compatibilidad:** Funciona en Windows 10 y superior

## 🐛 Solución de Problemas

### Programación de Apagado

#### La hibernación no funciona
- Verifica que la hibernación esté habilitada en Windows:
  ```cmd
  powercfg /hibernate on
  ```

#### La suspensión no funciona
- Algunos sistemas no soportan suspensión por software
- Verifica la configuración de energía en el Panel de Control

#### Error al ejecutar comandos
- Ejecuta la aplicación como administrador si es necesario
- Verifica que no haya políticas de grupo que bloqueen estos comandos

### Control de Pantalla

#### Error de acceso denegado
- **Solución:** Ejecuta la aplicación como administrador
  - Clic derecho en el ejecutable o script
  - Selecciona "Ejecutar como administrador"

#### No se puede leer la configuración actual
- Verifica que el comando `powercfg` esté disponible en tu sistema
- Ejecuta en CMD: `powercfg /?` para verificar

#### Los cambios no se aplican
- Asegúrate de tener permisos de administrador
- Verifica que no haya políticas de grupo que restrinjan cambios de energía
- Revisa el Plan de energía activo en Configuración de Windows

#### La pantalla se sigue apagando aunque configuré "Nunca"
- Algunos protectores de pantalla pueden tener su propia configuración
- Verifica la configuración del protector de pantalla en Windows
- Algunas aplicaciones de terceros pueden sobrescribir esta configuración

## 📝 Ejemplos de Uso

### Programación de Apagado

#### Ejemplo 1: Apagar a medianoche
1. Ve a la pestaña "🔌 Programar Apagado"
2. Ingresa: `00:00`
3. Selecciona: `Apagar`
4. Haz clic en: `Programar`

#### Ejemplo 2: Hibernar después del trabajo
1. Ve a la pestaña "🔌 Programar Apagado"
2. Ingresa: `18:30`
3. Selecciona: `Hibernar`
4. Haz clic en: `Programar`

#### Ejemplo 3: Suspender para ahorrar energía
1. Ve a la pestaña "🔌 Programar Apagado"
2. Ingresa: `22:00`
3. Selecciona: `Suspender`
4. Haz clic en: `Programar`

### Control de Pantalla

#### Ejemplo 1: Configurar apagado rápido para ahorrar energía
1. Ve a la pestaña "🖥️ Control de Pantalla"
2. Selecciona: `5 minutos`
3. Haz clic en: `✓ Aplicar Configuración`
4. Confirma la acción

#### Ejemplo 2: Desactivar apagado automático para presentaciones
1. Ve a la pestaña "🖥️ Control de Pantalla"
2. Selecciona: `Nunca`
3. Haz clic en: `✓ Aplicar Configuración`
4. Confirma la acción

#### Ejemplo 3: Configuración equilibrada para trabajo
1. Ve a la pestaña "🖥️ Control de Pantalla"
2. Selecciona: `15 minutos`
3. Haz clic en: `✓ Aplicar Configuración`
4. Confirma la acción

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Si encuentras un bug o tienes una sugerencia:

1. Abre un issue describiendo el problema o mejora
2. Si deseas contribuir código, haz un fork y envía un pull request

## 📄 Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.

## 👨‍💻 Autor

Desarrollado por Abraham Tartalos usando Python y Tkinter 

## 🔄 Versión

**v2.0.0** - Actualización Mayor
- ✨ **NUEVO:** Control de tiempo de apagado de pantalla
- ✨ **NUEVO:** Sistema de pestañas para organizar funcionalidades
- ✨ **NUEVO:** Visualización de configuración actual de pantalla
- ✨ **NUEVO:** Opciones predefinidas de tiempo (1, 5, 10, 15, 30, 40 min, 1 hora, Nunca)
- ✨ **NUEVO:** Aplicación simultánea para modo AC y DC
- 🎨 Interfaz mejorada con tema oscuro elegante
- 🔧 Arquitectura modular con `screen_controller.py`
- 📝 Documentación ampliada

**v1.0.0** - Versión inicial
- Programación de apagado/hibernación/suspensión
- Interfaz gráfica con Tkinter
- Sistema de advertencia antes de ejecutar
- Cancelación de acciones programadas

---

**¿Preguntas o problemas?** Abre un issue en el repositorio.