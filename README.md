---
title: Proyecto Agro
emoji: 🏃
colorFrom: blue
colorTo: yellow
sdk: gradio
sdk_version: 5.49.1
app_file: app.py
pinned: false
short_description: probar hacer proyecto
---

Check out the configuration reference at https://huggingface.co/docs/hub/spaces-config-reference


# Clasificador de Variedades de Manzanas (MVP Agro)

## Descripción
Este Proyecto Mínimo Viable (MVP) aborda el desafío de **clasificar variedades de manzanas a partir de una imagen**. Utilizando técnicas de visión por computadora con IA Generativa, la aplicación permite a los usuarios obtener una identificación estimada de la variedad de manzana en una foto, junto con un indicador de la confianza de la predicción.

El público objetivo incluye a **productores**, **consumidores** y **técnicos** del sector agropecuario. Para aquellos sin experiencia previa en la identificación de variedades, la aplicación sirve como una herramienta de ayuda y aprendizaje. Para usuarios con conocimientos, ofrece una segunda opinión para validar o comparar sus propias estimaciones.

El flujo de uso es sencillo: el usuario carga una foto de una manzana en la interfaz web, la aplicación procesa la imagen, detecta la fruta principal, la clasifica, y muestra la variedad estimada y su nivel de confianza.

## Demo
Puedes acceder a la aplicación desplegada públicamente en Hugging Face Spaces a través del siguiente enlace:
[https://huggingface.co/spaces/martn37/proyecto_agro](https://huggingface.co/spaces/martn37/proyecto_agro)

[Opcional:  un video demo corto,  enlace]

## Funcionalidades
- Carga de imágenes de frutas a través de una interfaz web intuitiva.
- Determinación en forma automática de la fruta principal en la imagen utilizando un modelo de IA.
- Resaltado visual de la fruta detectada con un recuadro en la imagen original.
- Clasificación de la variedad de la fruta utilizando un modelo de visión por computadora.
- Mostrar los resultados de la clasificación (variedad estimada y su nivel de confianza).

## Stack Tecnológico
- Framework de Interfaz: **Gradio**
- Modelos de IA:
    - Detección de Objetos: **facebook/detr-resnet-50** (Modelo pre-entrenado de Hugging Face)
    - Clasificación de Imágenes: **apple/mobilevit-small** (Modelo pre-entrenado de Hugging Face)
- Librerías principales:
    - `gradio`: Para la interfaz de usuario.
    - `Pillow` (PIL): Procesamiento básico de imágenes.
    - `numpy`: Operaciones numéricas.
    - `transformers`: Carga y uso de modelos de Hugging Face.
    - `torch`: Backend de deep learning (requerido por los modelos).
    - `timm`: Librería de modelos de visión (requerida por DETRConvEncoder).

## Instalación y Uso Local

### Prerrequisitos
- Python **3.12** (versión utilizada en el entorno de desarrollo)
- Git

##  Instrucciones instalación
##   Clonar el repositorio desde GitHub:


 Clonar el repositorio: git clone https://github.com/martinm5267/proyecto_agro_intartif.git

    Navegar al directorio donde se va a guardar el proyecto, por ejemplo: 
    
    cd proyecto_agro_intartif 
    
##  Crear y activar entorno virtual:

python -m venv venv, source venv/bin/activate (Linux/macOS)
 venv\Scripts\activate (Windows) 

Estos son los comandos estándar para crear y activar un entorno virtual con venv en Python, cubriendo los diferentes sistemas operativos.
    
##  Instalar dependencias: 
pip install -r requirements.txt 
Este es el comando estándar para instalar todas las librerías listadas en requirements.txt.

## Ejecutar la aplicación: python app.py
 Este es el comando estándar para ejecutar un script Python llamado app.py.







