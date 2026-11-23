"""
PROGRAMACIÓN WEB - EVALUACIÓN N°3 (TA_6)
Felipe Álvarez Valle

Aplicación Flask con un menú principal y dos ejercicios:
  - Ejercicio 1: promedio de 3 notas (10 a 70) + asistencia (0 a 100) -> APROBADO / REPROBADO
  - Ejercicio 2: de 3 nombres distintos, el que tiene más caracteres (letras) y cuántos tiene
"""

from flask import Flask, render_template, request, redirect, url_for, abort

app = Flask(__name__)

# ---------------------------------------------------------------------------
# Reglas del ejercicio 1
# ---------------------------------------------------------------------------
NOTA_MINIMA = 10
NOTA_MAXIMA = 70
NOTA_APROBACION = 40
ASISTENCIA_MINIMA = 75

# ---------------------------------------------------------------------------
# Registros guardados en memoria (se pierden al detener el servidor)
# Cada envío correcto de un formulario se agrega a su lista.
# ---------------------------------------------------------------------------
historial_notas = []
historial_nombres = []


# ---------------------------------------------------------------------------
# Funciones de lógica (separadas de las rutas para poder reutilizarlas)
# ---------------------------------------------------------------------------
def calcular_promedio(nota1, nota2, nota3):
    """Devuelve el promedio de las tres notas, redondeado a un decimal."""
    return round((nota1 + nota2 + nota3) / 3, 1)


def obtener_estado(promedio, asistencia):
    """El alumno aprueba si el promedio es >= 40 y la asistencia es >= 75 %."""
    if promedio >= NOTA_APROBACION and asistencia >= ASISTENCIA_MINIMA:
        return "APROBADO"
    return "REPROBADO"


def validar_notas(notas, asistencia):
    """Revisa los rangos permitidos y devuelve una lista de errores (vacía si todo está bien)."""
    errores = []
    for posicion, nota in enumerate(notas, start=1):
        if not NOTA_MINIMA <= nota <= NOTA_MAXIMA:
            errores.append(f"La nota {posicion} debe estar entre {NOTA_MINIMA} y {NOTA_MAXIMA}.")
    if not 0 <= asistencia <= 100:
        errores.append("La asistencia debe estar entre 0 y 100.")
    return errores


def contar_letras(nombre):
    """Cuenta solo las letras del nombre (ignora espacios, guiones, etc.)."""
    return sum(1 for caracter in nombre if caracter.isalpha())


def nombre_mas_largo(nombres):
    """
    Devuelve una tupla (lista_de_ganadores, cantidad_de_caracteres).
    Si dos o más nombres empatan con la mayor cantidad, se devuelven todos.
    """
    cantidades = [contar_letras(nombre) for nombre in nombres]
    mayor = max(cantidades)
    ganadores = [nombre for nombre, cantidad in zip(nombres, cantidades) if cantidad == mayor]
    return ganadores, mayor


def validar_nombres(nombres):
    """Revisa que los 3 nombres tengan letras y que sean diferentes entre sí."""
    errores = []
    for posicion, nombre in enumerate(nombres, start=1):
        if contar_letras(nombre) == 0:
            errores.append(f"El nombre {posicion} debe contener al menos una letra.")
    nombres_normalizados = [nombre.lower() for nombre in nombres]
    if len(set(nombres_normalizados)) < len(nombres_normalizados):
        errores.append("Los 3 nombres deben ser diferentes.")
    return errores


def procesar_notas(nota1, nota2, nota3, asistencia):
    """Valida, calcula y guarda en memoria. Devuelve (resultado, errores)."""
    errores = validar_notas([nota1, nota2, nota3], asistencia)
    if errores:
        return None, errores
    promedio = calcular_promedio(nota1, nota2, nota3)
    estado = obtener_estado(promedio, asistencia)
    resultado = {
        "notas": [nota1, nota2, nota3],
        "asistencia": asistencia,
        "promedio": promedio,
        "estado": estado,
    }
    historial_notas.append(resultado)
    return resultado, []


def procesar_nombres(nombre1, nombre2, nombre3):
    """Valida, calcula y guarda en memoria. Devuelve (resultado, errores)."""
    nombres = [nombre1.strip(), nombre2.strip(), nombre3.strip()]
    errores = validar_nombres(nombres)
    if errores:
        return None, errores
    ganadores, cantidad = nombre_mas_largo(nombres)
    resultado = {
        "nombres": nombres,
        "ganadores": ganadores,
        "cantidad": cantidad,
    }
    historial_nombres.append(resultado)
    return resultado, []


# ---------------------------------------------------------------------------
# Rutas
# ---------------------------------------------------------------------------
@app.route("/")
def index():
    """Menú principal con los dos botones."""
    return render_template("index.html")


@app.route("/inicio")
@app.route("/menu")
def inicio():
    """Rutas alternativas que redirigen al menú principal."""
    return redirect(url_for("index"))


@app.route("/ejercicio1", methods=["GET", "POST"])
def ejercicio1():
    """GET muestra el formulario vacío; POST recibe los datos, calcula y muestra el resultado."""
    resultado = None
    errores = []
    datos = {}

    if request.method == "POST":
        datos = request.form
        try:
            nota1 = float(request.form["nota1"])
            nota2 = float(request.form["nota2"])
            nota3 = float(request.form["nota3"])
            asistencia = float(request.form["asistencia"])
        except (KeyError, ValueError):
            errores = ["Debes ingresar números válidos en todos los campos."]
        else:
            resultado, errores = procesar_notas(nota1, nota2, nota3, asistencia)

    return render_template(
        "ejercicio1.html",
        resultado=resultado,
        errores=errores,
        datos=datos,
        historial=historial_notas,
    )


@app.route("/ejercicio1/<nota1>/<nota2>/<nota3>/<asistencia>")
def ejercicio1_url(nota1, nota2, nota3, asistencia):
    """
    Misma lógica del ejercicio 1, pero recibiendo los datos como parámetros en la URL.
    Ejemplo: /ejercicio1/55/65/45/86
    Si algún valor no es número o está fuera de rango, se aborta la solicitud con error 400.
    """
    try:
        nota1, nota2, nota3, asistencia = float(nota1), float(nota2), float(nota3), float(asistencia)
    except ValueError:
        abort(400)
    if validar_notas([nota1, nota2, nota3], asistencia):
        abort(400)
    resultado, errores = procesar_notas(nota1, nota2, nota3, asistencia)
    datos = {"nota1": nota1, "nota2": nota2, "nota3": nota3, "asistencia": asistencia}
    return render_template(
        "ejercicio1.html",
        resultado=resultado,
        errores=errores,
        datos=datos,
        historial=historial_notas,
    )


@app.route("/ejercicio2", methods=["GET", "POST"])
def ejercicio2():
    """GET muestra el formulario vacío; POST recibe los nombres y muestra el más largo."""
    resultado = None
    errores = []
    datos = {}

    if request.method == "POST":
        datos = request.form
        nombre1 = request.form.get("nombre1", "")
        nombre2 = request.form.get("nombre2", "")
        nombre3 = request.form.get("nombre3", "")
        resultado, errores = procesar_nombres(nombre1, nombre2, nombre3)

    return render_template(
        "ejercicio2.html",
        resultado=resultado,
        errores=errores,
        datos=datos,
        historial=historial_nombres,
    )


@app.route("/ejercicio2/<nombre1>/<nombre2>/<nombre3>")
def ejercicio2_url(nombre1, nombre2, nombre3):
    """
    Misma lógica del ejercicio 2 con parámetros en la URL.
    Ejemplo: /ejercicio2/Felipe/Juan/Gustavo
    Si los nombres no son válidos se aborta la solicitud con error 400.
    """
    if validar_nombres([nombre1.strip(), nombre2.strip(), nombre3.strip()]):
        abort(400)
    resultado, errores = procesar_nombres(nombre1, nombre2, nombre3)
    datos = {"nombre1": nombre1, "nombre2": nombre2, "nombre3": nombre3}
    return render_template(
        "ejercicio2.html",
        resultado=resultado,
        errores=errores,
        datos=datos,
        historial=historial_nombres,
    )


@app.route("/historial/borrar/<ejercicio>", methods=["POST"])
def borrar_historial(ejercicio):
    """Vacía el historial en memoria del ejercicio indicado y vuelve a su formulario."""
    if ejercicio == "1":
        historial_notas.clear()
        return redirect(url_for("ejercicio1"))
    if ejercicio == "2":
        historial_nombres.clear()
        return redirect(url_for("ejercicio2"))
    abort(404)


# ---------------------------------------------------------------------------
# Páginas de error
# ---------------------------------------------------------------------------
@app.errorhandler(400)
def solicitud_invalida(error):
    mensaje = "Los datos enviados en la URL no son válidos. Revisa los rangos permitidos."
    return render_template("error.html", codigo=400, mensaje=mensaje), 400


@app.errorhandler(404)
def pagina_no_encontrada(error):
    mensaje = "La página que buscas no existe."
    return render_template("error.html", codigo=404, mensaje=mensaje), 404


if __name__ == "__main__":
    app.run(debug=True)
