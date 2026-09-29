"""Una página web mínima sobre markov.py.

Uso:
    pip install flask
    python3 app.py            # abre en http://localhost:5000

La página no tiene lógica propia: importa entrenar() y generar() de markov.py. Si se cambia
markov.py y se guarda, el servidor se reinicia solo y al recargar la página se ve el cambio.
"""
from pathlib import Path

from flask import Flask, render_template_string, request

from markov import entrenar, generar, leer, palabras

TEXTOS = {p.stem: p for p in sorted(Path(__file__).parent.glob("textos/*.txt"))}

PAGINA = """<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Generador de Markov</title>
<style>
  body { font: 16px/1.5 system-ui, sans-serif; max-width: 760px; margin: 0 auto; padding: 24px 16px; color: #1f2328; background: #f7f6f2; }
  form { display: flex; flex-wrap: wrap; gap: 10px; align-items: center; }
  select, button { font: inherit; padding: 5px 10px; }
  .salida { background: #fff; border: 1px solid #d9d6cc; border-radius: 6px; padding: 14px; font-size: 1.15rem; margin: 16px 0; }
  table { border-collapse: collapse; width: 100%; font-size: .9rem; }
  td { border-top: 1px solid #d9d6cc; padding: 4px 6px; vertical-align: top; }
  code { background: #e3edf8; padding: 0 4px; border-radius: 3px; }
  .nota { color: #5d646d; font-size: .9rem; }
</style>
</head>
<body>
<h1>Generador de Markov</h1>
<p class="nota">Esta página solo llama a <code>entrenar()</code> y <code>generar()</code> de <code>markov.py</code>.</p>
<form>
  <select name="texto">
    {% for t in textos %}<option value="{{ t }}" {% if t == texto %}selected{% endif %}>{{ t }}</option>{% endfor %}
  </select>
  <label>Contexto:
    <select name="n">
      {% for i in (1, 2, 3) %}<option {% if i == n %}selected{% endif %}>{{ i }}</option>{% endfor %}
    </select> palabras
  </label>
  <button>Generar</button>
</form>
<div class="salida">{{ salida }}</div>
<p class="nota">La tabla tiene {{ filas|length }} filas. Estas son las que tienen más de una continuación posible:</p>
<table>
  {% for contexto, siguientes in filas if siguientes|length > 1 %}
  <tr><td><code>{{ contexto }}</code></td><td>{{ siguientes|join(" · ") }}</td></tr>
  {% endfor %}
</table>
</body>
</html>"""

app = Flask(__name__)


@app.route("/")
def inicio():
    texto = request.args.get("texto", "hechos")
    if texto not in TEXTOS:
        texto = "hechos"
    n = int(request.args.get("n", 2)) if request.args.get("n") in ("1", "2", "3") else 2

    tabla = entrenar(palabras(leer(TEXTOS[texto])), n)
    filas = []
    for contexto, siguientes in sorted(tabla.items(), key=lambda x: -len(set(x[1]))):
        conteo = [f"{p} ({siguientes.count(p)})" for p in dict.fromkeys(siguientes)]
        filas.append((" ".join(contexto), conteo))

    return render_template_string(
        PAGINA, textos=TEXTOS, texto=texto, n=n, salida=generar(tabla, n), filas=filas
    )


if __name__ == "__main__":
    # Sin modo debug (su consola permite ejecutar código desde el navegador), pero con
    # recarga automática: al guardar markov.py, el servidor se reinicia solo.
    app.run(host="0.0.0.0", port=5000, debug=False, use_reloader=True)
