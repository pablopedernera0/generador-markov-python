"""Generador de texto con una cadena de Markov, sin bibliotecas.

Uso:
    python3 markov.py textos/hechos.txt            # contexto de 2 palabras
    python3 markov.py textos/hechos.txt 3          # contexto de 3 palabras
    python3 markov.py textos/hechos.txt 2 tabla    # muestra la tabla en vez de generar

Es la misma idea que la página https://pablopedernera0.github.io/generador-markov/
"""
import random
import re
import sys
from collections import defaultdict


def leer(ruta):
    """Lee un texto. Si tiene encabezado (nombre:, pista:, línea ---), lo saltea."""
    texto = open(ruta, encoding="utf-8").read()
    if "\n---\n" in texto:
        texto = texto.split("\n---\n", 1)[1]
    return texto


def palabras(texto):
    """Separa el texto en palabras y signos de puntuación."""
    return re.findall(r"[^\W_]+|[.,;:¿?¡!()«»—]", texto)


def entrenar(tokens, n):
    """Entrenar es contar: para cada secuencia de n palabras, qué palabra vino después."""
    tabla = defaultdict(list)
    for i in range(len(tokens) - n):
        contexto = tuple(tokens[i:i + n])
        tabla[contexto].append(tokens[i + n])
    return tabla


def generar(tabla, n, largo=40):
    """Usar el modelo es sortear: mirar las últimas n palabras y elegir una de las que vinieron después."""
    # Arranca después de un punto, para empezar una oración. El punto no se muestra.
    comienzos = [c for c in tabla if c[0] == "."] or list(tabla)
    salida = list(random.choice(comienzos))
    for _ in range(largo):
        contexto = tuple(salida[-n:])
        if contexto not in tabla:        # el modelo nunca vio este contexto: se traba
            break
        # La lista guarda cada aparición, con repetidos: lo que vino más veces sale más seguido.
        salida.append(random.choice(tabla[contexto]))
    return unir(salida[1:] if salida[0] == "." else salida)


def unir(tokens):
    texto = " ".join(tokens)
    texto = re.sub(r" ([.,;:?!)»])", r"\1", texto)
    return re.sub(r"([¿¡(«]) ", r"\1", texto)


if __name__ == "__main__":
    ruta = sys.argv[1] if len(sys.argv) > 1 else "textos/hechos.txt"
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 2
    tabla = entrenar(palabras(leer(ruta)), n)

    if len(sys.argv) > 3 and sys.argv[3] == "tabla":
        for contexto, siguientes in sorted(tabla.items(), key=lambda x: -len(set(x[1]))):
            conteo = {p: siguientes.count(p) for p in dict.fromkeys(siguientes)}
            print(" ".join(contexto), "->", conteo)
    else:
        print(generar(tabla, n))
