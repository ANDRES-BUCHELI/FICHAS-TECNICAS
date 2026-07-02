import os
import re
from functools import wraps

from flask import (
    Flask, render_template, request, redirect, url_for,
    session, send_from_directory, abort, flash
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PDF_DIR = os.path.join(BASE_DIR, "static", "pdfs")
DOCX_DIR = os.path.join(BASE_DIR, "static", "docx")

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-cambiar-en-produccion")
FICHAS_PASSWORD = os.environ.get("FICHAS_PASSWORD", "intela2026")

TIPOS = ["tubular", "abierto"]
TIPO_LABEL = {"tubular": "Tubular", "abierto": "Abierto"}
FAMILIAS = ["Jersey", "Fleece", "Pique", "Ribb", "Topper"]


def nombre_legible(stem):
    # "Ficha_Tecnica_JerseyMwt105_INTELA" -> "Jersey Mwt 105"
    s = stem
    s = re.sub(r"^Ficha_Tecnica_", "", s)
    s = re.sub(r"_INTELA$", "", s)
    s = re.sub(r"(?<=[a-zA-Zé])(?=[0-9])", " ", s)  # letra->numero
    s = re.sub(r"(?<=[0-9])(?=[A-ZÉ])", " ", s)      # numero->MAYUS
    s = re.sub(r"(?<=[a-zé])(?=[A-ZÉ])", " ", s)     # minuscula->MAYUS (camelCase)
    return s.strip()


def familia_de(nombre):
    for fam in FAMILIAS:
        if nombre.lower().startswith(fam.lower()):
            return fam
    return "Otras"


def listar_fichas():
    """Devuelve todas las fichas, con su tipo (tubular/abierto), agrupables por familia."""
    fichas = []
    for tipo in TIPOS:
        pdf_dir_tipo = os.path.join(PDF_DIR, tipo)
        docx_dir_tipo = os.path.join(DOCX_DIR, tipo)
        if not os.path.isdir(pdf_dir_tipo):
            continue
        for f in sorted(os.listdir(pdf_dir_tipo)):
            if not f.lower().endswith(".pdf"):
                continue
            stem = os.path.splitext(f)[0]
            nombre = nombre_legible(stem)
            docx_name = stem + ".docx"
            tiene_docx = os.path.exists(os.path.join(docx_dir_tipo, docx_name))
            fichas.append({
                "pdf": f,
                "docx": docx_name if tiene_docx else None,
                "nombre": nombre,
                "familia": familia_de(nombre),
                "tipo": tipo,
                "tipo_label": TIPO_LABEL[tipo],
            })
    fichas.sort(key=lambda x: (x["tipo"], x["familia"], x["nombre"]))
    return fichas


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not session.get("auth"):
            return redirect(url_for("login", next=request.path))
        return view(*args, **kwargs)
    return wrapped


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        clave = request.form.get("password", "")
        if clave == FICHAS_PASSWORD:
            session["auth"] = True
            destino = request.args.get("next") or url_for("index")
            return redirect(destino)
        flash("Clave incorrecta.", "danger")
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/")
@login_required
def index():
    fichas = listar_fichas()
    familias = sorted(set(f["familia"] for f in fichas))
    conteo_tipo = {t: sum(1 for f in fichas if f["tipo"] == t) for t in TIPOS}
    return render_template("index.html", fichas=fichas, familias=familias,
                            tipos=TIPOS, tipo_label=TIPO_LABEL, conteo_tipo=conteo_tipo)


def _tipo_valido(tipo):
    if tipo not in TIPOS:
        abort(404)


@app.route("/ver/<tipo>/<path:archivo>")
@login_required
def ver(tipo, archivo):
    _tipo_valido(tipo)
    if not archivo.lower().endswith(".pdf") or "/" in archivo or "\\" in archivo:
        abort(404)
    carpeta = os.path.join(PDF_DIR, tipo)
    if not os.path.exists(os.path.join(carpeta, archivo)):
        abort(404)
    return send_from_directory(carpeta, archivo, as_attachment=False,
                                mimetype="application/pdf")


@app.route("/descargar/<tipo>/<path:archivo>")
@login_required
def descargar(tipo, archivo):
    _tipo_valido(tipo)
    if not archivo.lower().endswith(".docx") or "/" in archivo or "\\" in archivo:
        abort(404)
    carpeta = os.path.join(DOCX_DIR, tipo)
    if not os.path.exists(os.path.join(carpeta, archivo)):
        abort(404)
    return send_from_directory(carpeta, archivo, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True, port=5050)
