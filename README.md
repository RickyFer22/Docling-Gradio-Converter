# Docling - Conversor de Documentos (Gradio)

Esta aplicación Gradio permite convertir documentos a formato Markdown o JSON utilizando la librería `docling`.

## Funcionalidades

- Convertir documentos DOC, DOCX, PDF y TXT a Markdown o JSON.
- Mostrar la información del documento convertido en la interfaz.
- Descargar el documento convertido en un archivo.

## Cómo usar

1. Ejecuta el archivo `app.py`.
2. La aplicación se abrirá en tu navegador web.
3. Sube el archivo que deseas convertir utilizando el botón "Upload Your Document".
4. Selecciona el formato de salida (Markdown o JSON).
5. Haz clic en el botón "Convert Document" para iniciar la conversión.
6. Una vez completada la conversión, se mostrará el contenido convertido y la metadata del documento.
7. Puedes descargar el documento convertido utilizando el botón "Download Converted File".

## Dependencias

- gradio
- docling
- json
- tempfile
- os
