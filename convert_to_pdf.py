"""
Convierte todas las fichas técnicas (.docx) a PDF usando Word (via docx2pdf),
y copia tanto los PDF como los .docx originales dentro de fichas_web/static/,
para que la app Flask los sirva como archivos estáticos empaquetados con el
proyecto (el servidor en la nube no tiene acceso a la carpeta de OneDrive).

Requiere: Microsoft Word instalado, cerrado antes de correr este script.
Re-ejecutar cada vez que se agreguen o modifiquen fichas en la carpeta fuente.
"""
import os
import shutil
import sys

FUENTE = r"C:\Users\intel\OneDrive\Escritorio\FICHAS TECNICAS\FICHAS NUEVO FORMATO"
BASE = os.path.dirname(os.path.abspath(__file__))
DEST_PDF = os.path.join(BASE, "static", "pdfs")
DEST_DOCX = os.path.join(BASE, "static", "docx")


def main():
    os.makedirs(DEST_PDF, exist_ok=True)
    os.makedirs(DEST_DOCX, exist_ok=True)

    archivos = sorted(f for f in os.listdir(FUENTE) if f.lower().endswith(".docx"))
    if not archivos:
        print(f"No se encontraron .docx en {FUENTE}")
        return

    print(f"Encontrados {len(archivos)} archivos .docx en la carpeta fuente.")

    # 1) copiar los .docx originales (para el botón "Descargar Word")
    for f in archivos:
        shutil.copy(os.path.join(FUENTE, f), os.path.join(DEST_DOCX, f))
    print(f"Copiados {len(archivos)} .docx a {DEST_DOCX}")

    # 2) convertir a PDF con Word (docx2pdf controla Word por COM)
    try:
        from docx2pdf import convert
    except ImportError:
        print("Falta docx2pdf. Instalar con: pip install docx2pdf pywin32")
        sys.exit(1)

    print("Convirtiendo a PDF con Word (asegúrate de que Word esté cerrado)...")
    convert(DEST_DOCX, DEST_PDF)

    generados = [f for f in os.listdir(DEST_PDF) if f.lower().endswith(".pdf")]
    print(f"Listo: {len(generados)} PDF generados en {DEST_PDF}")

    faltantes = set(os.path.splitext(f)[0] for f in archivos) - set(
        os.path.splitext(f)[0] for f in generados
    )
    if faltantes:
        print("ADVERTENCIA - no se generó PDF para:")
        for f in sorted(faltantes):
            print("  -", f)


if __name__ == "__main__":
    main()
