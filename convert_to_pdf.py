"""
Convierte todas las fichas técnicas (.docx) a PDF usando Word (via docx2pdf),
y copia tanto los PDF como los .docx originales dentro de fichas_web/static/,
para que la app Flask los sirva como archivos estáticos empaquetados con el
proyecto (el servidor en la nube no tiene acceso a la carpeta de OneDrive).

La carpeta fuente tiene dos subcarpetas - TUBULAR y ABIERTO - según el tipo de
tela. Esa misma división se replica en static/pdfs/<tipo>/ y static/docx/<tipo>/
para que la web pueda mostrarlas agrupadas y sea fácil buscarlas por tipo.

Requiere: Microsoft Word instalado, cerrado antes de correr este script.
Re-ejecutar cada vez que se agreguen o modifiquen fichas en la carpeta fuente.
"""
import os
import shutil
import sys

FUENTE = r"C:\Users\intel\OneDrive\Escritorio\FICHAS TECNICAS\FICHAS NUEVO FORMATO"
TIPOS = ["TUBULAR", "ABIERTO"]
BASE = os.path.dirname(os.path.abspath(__file__))
DEST_PDF = os.path.join(BASE, "static", "pdfs")
DEST_DOCX = os.path.join(BASE, "static", "docx")


def main():
    try:
        from docx2pdf import convert
    except ImportError:
        print("Falta docx2pdf. Instalar con: pip install docx2pdf pywin32")
        sys.exit(1)

    total = 0
    for tipo in TIPOS:
        fuente_tipo = os.path.join(FUENTE, tipo)
        if not os.path.isdir(fuente_tipo):
            print(f"AVISO: no existe {fuente_tipo}, se omite.")
            continue

        dest_pdf_tipo = os.path.join(DEST_PDF, tipo.lower())
        dest_docx_tipo = os.path.join(DEST_DOCX, tipo.lower())
        os.makedirs(dest_pdf_tipo, exist_ok=True)
        os.makedirs(dest_docx_tipo, exist_ok=True)

        archivos = sorted(f for f in os.listdir(fuente_tipo) if f.lower().endswith(".docx"))
        if not archivos:
            print(f"No se encontraron .docx en {fuente_tipo}")
            continue

        print(f"[{tipo}] {len(archivos)} archivos .docx encontrados.")

        for f in archivos:
            shutil.copy(os.path.join(fuente_tipo, f), os.path.join(dest_docx_tipo, f))
        print(f"[{tipo}] Copiados {len(archivos)} .docx a {dest_docx_tipo}")

        print(f"[{tipo}] Convirtiendo a PDF con Word (asegúrate de que esté cerrado)...")
        convert(dest_docx_tipo, dest_pdf_tipo)

        generados = [f for f in os.listdir(dest_pdf_tipo) if f.lower().endswith(".pdf")]
        print(f"[{tipo}] Listo: {len(generados)} PDF generados en {dest_pdf_tipo}")
        total += len(generados)

        faltantes = set(os.path.splitext(f)[0] for f in archivos) - set(
            os.path.splitext(f)[0] for f in generados
        )
        if faltantes:
            print(f"[{tipo}] ADVERTENCIA - no se generó PDF para:")
            for f in sorted(faltantes):
                print("  -", f)

    print(f"\nTotal general: {total} PDF generados.")


if __name__ == "__main__":
    main()
