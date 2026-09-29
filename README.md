# Generador de texto con cadenas de Markov, en Python

Código de la sección optativa de la lectura sobre cadenas de Markov, material complementario
del generador web: https://pablopedernera0.github.io/generador-markov/

Un generador de Markov aprende contando qué palabra vino después de cada secuencia de
palabras en un texto, y genera sorteando la siguiente según esas cuentas. Acá está dos veces:

| Archivo | Qué hace |
|---|---|
| `markov.py` | El generador completo en Python puro, sin bibliotecas. Unas treinta líneas. |
| `con_markovify.py` | La misma idea con la biblioteca [markovify](https://github.com/jsvine/markovify). |
| `app.py` | Una página web mínima con Flask que llama a `markov.py`. Al guardar `markov.py`, se reinicia sola. |
| `textos/` | Los textos de partida: los de la página web y *El gaucho Martín Fierro*. |

Para probarlo sin instalar nada, en el navegador: escenario de Killercoda
[generador-markov](https://killercoda.com/pablop22/scenario/generador-markov), que clona este
repo y lo deja listo para usar.

## Uso

`markov.py` no necesita nada más que Python 3. Para `con_markovify.py` y `app.py` conviene un
entorno virtual: en Ubuntu y Debian recientes, `pip install` fuera de un entorno virtual está
bloqueado para proteger los paquetes del sistema, y forzarlo puede chocar con versiones que
trae el sistema (pasa con `blinker`, que usa Flask).

```bash
python3 -m venv .venv          # en Ubuntu, si falla: sudo apt install python3-venv
source .venv/bin/activate
pip install markovify flask
```

```bash
python3 markov.py textos/hechos.txt            # genera con 2 palabras de contexto
python3 markov.py textos/hechos.txt 3          # con 3
python3 markov.py textos/oficios.txt 2 tabla   # muestra la tabla: el modelo entero

python3 con_markovify.py                              # una estrofa del Martín Fierro
python3 con_markovify.py textos/martin-fierro.txt 3   # con 3 palabras de contexto
python3 con_markovify.py textos/martin-fierro.txt 2 copias
```

La última línea muestra algo que el generador web deja ver a ojo: con poco texto y mucho
contexto, lo generado es copia del original. `markovify` lo controla por defecto: descarta
una oración generada si repite textualmente un tramo del original de más del 70 % de su
largo (o de 15 palabras). El modo `copias` genera 300 versos con y sin ese control y cuenta
cuántos son un verso del poema tal cual.

Y una página web sobre el mismo código:

```bash
python3 app.py      # http://localhost:5000
```

`app.py` no tiene lógica propia: importa `entrenar()` y `generar()` de `markov.py`. Probá
cambiar algo en `markov.py` (por ejemplo, que `generar()` elija siempre la continuación más
frecuente en lugar de sortear), guardar y recargar la página. Es, en chiquito, la relación
entre un modelo y la aplicación que lo usa.

## Textos

Los textos de `textos/` tienen un encabezado (`nombre:`, `pista:`, línea `---`) que los
scripts saltean. *El gaucho Martín Fierro* (José Hernández, 1872) es de dominio público; el
texto sale de la edición digital de la Biblioteca Digital Argentina publicada en Proyecto
Gutenberg (ebook 14765), sin la carta del autor ni los números de estrofa.
