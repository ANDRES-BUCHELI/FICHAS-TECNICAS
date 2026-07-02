# Fichas Técnicas Intela - Portal Web

Sitio con clave de acceso compartida donde el equipo puede ver e imprimir las fichas técnicas de tela de Intela desde cualquier lugar con internet.

## Cómo funciona

- Las 64 fichas ya están convertidas a PDF y empaquetadas en `static/pdfs/` y `static/docx/` (no se leen en vivo desde OneDrive; el servidor en la nube no tiene acceso a esa carpeta).
- Una sola clave (`FICHAS_PASSWORD`) protege todo el sitio. No hay cuentas individuales.
- Cada ficha se puede "Ver / Imprimir" (se abre el PDF en el navegador, con el botón de imprimir nativo del visor) o "Descargar Word" (el .docx original, editable).

## Actualizar el catálogo (cuando se agreguen o cambien fichas)

1. Asegúrate de que **Microsoft Word esté cerrado**.
2. Desde esta carpeta (`fichas_web`), corre:
   ```
   python convert_to_pdf.py
   ```
   Esto vuelve a copiar todos los `.docx` de
   `C:\Users\intel\OneDrive\Escritorio\FICHAS TECNICAS\FICHAS NUEVO FORMATO`
   y regenera los PDF.
3. Vuelve a desplegar (ver abajo) para que los cambios se reflejen en el sitio en línea.

## Probar en esta PC antes de publicar

```
pip install -r requirements.txt
pip install docx2pdf pywin32 waitress   # solo hacen falta en esta PC, no en el hosting
python app.py
```
Abre `http://localhost:5050`. La clave por defecto en pruebas locales es `intela2026`
(cámbiala definiendo la variable de entorno `FICHAS_PASSWORD` antes de correr `python app.py`).

## Publicarlo en internet (Render.com, gratis)

Esta parte la tienes que hacer tú — crear la cuenta de un servicio externo no es algo
que se pueda automatizar. Son 10-15 minutos, una sola vez:

1. Crea una cuenta gratis en **https://render.com** (puedes entrar con tu cuenta de Google/GitHub).
2. Sube esta carpeta (`fichas_web`) a un repositorio de **GitHub** (puede ser privado):
   - Si no tienes Git instalado, la forma más simple es crear el repositorio directo desde
     la web de GitHub ("Add file" → "Upload files") y arrastrar toda la carpeta.
3. En Render: **New +** → **Web Service** → conecta tu cuenta de GitHub → elige el repositorio.
4. Render va a detectar el archivo `render.yaml` automáticamente y va a pedirte el valor de
   `FICHAS_PASSWORD` (la clave que van a usar todos para entrar) — escríbela ahí.
5. Click en **Create Web Service** y espera 2-3 minutos a que termine el primer deploy.
6. Render te da una URL pública (algo como `https://fichas-tecnicas-intela.onrender.com`) —
   esa es la que compartes con tu equipo, junto con la clave.

**Nota sobre el plan gratis de Render:** el sitio "se duerme" tras ~15 minutos sin uso y tarda
unos segundos en despertar la primera vez que alguien entra después de estar inactivo — normal
en el plan gratuito, no es un error.

### Para actualizar el sitio ya publicado
Cada vez que corras `convert_to_pdf.py` con fichas nuevas, tienes que volver a subir los
archivos cambiados al repositorio de GitHub (reemplazando los de `static/pdfs` y `static/docx`);
Render vuelve a desplegar automáticamente en cuanto detecta el cambio.

## Cambiar la clave de acceso

En el panel de Render: tu servicio → **Environment** → edita `FICHAS_PASSWORD` → **Save Changes**
(el sitio se reinicia solo con la clave nueva).
