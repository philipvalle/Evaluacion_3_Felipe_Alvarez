# Evaluación N°3 – Programación Web (TA_6)

**Alumno:** Felipe Álvarez Valle
**Asignatura:** Programación Web – IPLACEX

Aplicación web desarrollada con **Flask** (framework de Python para construir aplicaciones web). Tiene un menú principal con dos botones, y cada botón abre un formulario:

- **Ejercicio 1:** recibe 3 notas (10 a 70) y la asistencia (0 a 100). Muestra el promedio y el estado **APROBADO** si el promedio es mayor o igual a 40 y la asistencia es mayor o igual a 75 %. En cualquier otro caso muestra **REPROBADO**.
- **Ejercicio 2:** recibe 3 nombres diferentes. Muestra el nombre con mayor cantidad de caracteres (letras) y cuántos tiene. Si hay empate, muestra todos los nombres empatados.

## Estructura del proyecto

```
Evaluacion_3_FELIPE_ALVAREZ/
├── main.py               # Rutas y lógica en Python
├── requirements.txt      # Dependencias del proyecto (instaladas con pip)
├── templates/            # Páginas HTML (Jinja2)
│   ├── base.html         # Página base con bloques; carga el CSS
│   ├── index.html        # Menú principal
│   ├── ejercicio1.html   # Formulario de notas
│   ├── ejercicio2.html   # Formulario de nombres
│   └── error.html        # Páginas de error 400 / 404
└── static/
    └── css/
        └── estilos.css   # Estilos de todas las páginas
```

## Cómo ejecutarlo

1. Crear el entorno virtual:
   ```
   python -m venv venv
   ```
2. Activarlo:
   - Windows: `venv\Scripts\activate`
   - macOS / Linux: `source venv/bin/activate`
3. Instalar las dependencias con **pip** (gestor de paquetes de Python):
   ```
   pip install -r requirements.txt
   ```
4. Ejecutar la aplicación:
   ```
   python main.py
   ```
5. Abrir en el navegador: http://127.0.0.1:5000

## Rutas

| Ruta | Método | Descripción |
|------|--------|-------------|
| `/` | GET | Menú principal |
| `/inicio`, `/menu` | GET | Redirigen al menú principal |
| `/ejercicio1` | GET / POST | Formulario de notas (GET lo muestra; POST lo procesa) |
| `/ejercicio1/<nota1>/<nota2>/<nota3>/<asistencia>` | GET | Ejercicio 1 con parámetros por URL. Ej.: `/ejercicio1/55/65/45/86` |
| `/ejercicio2` | GET / POST | Formulario de nombres |
| `/ejercicio2/<nombre1>/<nombre2>/<nombre3>` | GET | Ejercicio 2 con parámetros por URL. Ej.: `/ejercicio2/Felipe/Juan/Gustavo` |
| `/historial/borrar/<ejercicio>` | POST | Borra los cálculos guardados en memoria |

Si en las rutas con parámetros los valores no son válidos, la solicitud se aborta con un error 400 (`abort(400)`), y se muestra una página de error.

Cada cálculo correcto se guarda en una lista en memoria y aparece en una tabla bajo el formulario. Los registros se pierden al detener el servidor.
