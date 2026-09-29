"""La misma idea que markov.py, con la biblioteca markovify.

Uso:
    python3 con_markovify.py                               # Martín Fierro, una estrofa de 6 versos
    python3 con_markovify.py textos/martin-fierro.txt 3    # contexto de 3 palabras
    python3 con_markovify.py textos/hechos.txt 2           # un texto en prosa: genera oraciones
    python3 con_markovify.py textos/martin-fierro.txt 2 copias

markovify trata cada línea del Martín Fierro como una "oración" (un verso) y cada oración
de un texto en prosa como una unidad. Por defecto descarta lo generado cuando se parece
demasiado al texto original. Con "copias" se cuenta cuánto de lo generado sería copia si
no hiciera ese control.
"""
import sys

import markovify

from markov import leer


def modelo(ruta, n):
    texto = leer(ruta)
    if "martin-fierro" in ruta:
        return markovify.NewlineText(texto, state_size=n), True
    return markovify.Text(texto, state_size=n), False


def generar(m, versos):
    cantidad = 6 if versos else 3
    for _ in range(cantidad):
        linea = m.make_sentence(tries=100)
        print(linea or "(no encontró nada que no fuera copia del texto original)")


def contar_copias(m, ruta, intentos=300):
    originales = {l.strip() for l in leer(ruta).splitlines() if l.strip()}
    sin_control = [m.make_sentence(test_output=False) for _ in range(intentos)]
    sin_control = [s for s in sin_control if s]
    copias = sum(s in originales for s in sin_control)
    print(f"Sin el control: de {len(sin_control)} versos generados, {copias} son copia textual de un verso del poema.")
    con_control = [m.make_sentence(tries=10) for _ in range(intentos)]
    con_control = [s for s in con_control if s]
    copias = sum(s in originales for s in con_control)
    print(f"Con el control (lo que hace markovify por defecto): {len(con_control)} generados, {copias} copias.")


if __name__ == "__main__":
    ruta = sys.argv[1] if len(sys.argv) > 1 else "textos/martin-fierro.txt"
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 2
    m, versos = modelo(ruta, n)
    if len(sys.argv) > 3 and sys.argv[3] == "copias":
        contar_copias(m, ruta)
    else:
        generar(m, versos)
