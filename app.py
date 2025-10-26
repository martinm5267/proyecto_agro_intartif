

# app.py - Versi�n integrada con detecci�n, clasificaci�n y visualizaci�n

# Importamos las librer�as necesarias
import gradio as gr
from PIL import Image, ImageDraw # Import ImageDraw for drawing on images
import numpy as np
from transformers import pipeline # Make sure transformers is installed (pip install transformers)


# --- Cargar Modelos ---

# Cargar el modelo de detecci�n de objetos
# Este modelo es general, necesitamos verificar si detecta la fruta deseada (ej. 'apple')
try:
    object_detector = pipeline("object-detection", model="facebook/detr-resnet-50")
    print("Object detection model loaded successfully.")
except Exception as e:
    print(f"Error loading object detection model: {e}")
    object_detector = None

# Cargar el modelo de clasificaci�n de im�genes (el elegido por el usuario)
# Este modelo deber�a estar entrenado para las clases relevantes (ej. madurez, variedad)
try:
    clasificador = pipeline("image-classification", model="apple/mobilevit-small")
    print("Image classification model (apple/mobilevit-small) loaded successfully.")
except Exception as e:
    print(f"Error loading image classification model: {e}")
    clasificador = None


# --- Funci�n de Procesamiento ---

def clasificar_madurez_with_box(imagen: Image.Image):
    """
    Procesa una imagen: detecta objetos, selecciona el m�s relevante (fruta),
    lo clasifica y dibuja un recuadro en la imagen original.

    Args:
        imagen: Objeto PIL Image de la imagen de entrada.

    Returns:
        Una tupla con la imagen modificada (con recuadro) y una cadena de texto con los resultados.
        Retorna None para la imagen si no hay entrada v�lida.
    """
    if imagen is None:
        # Return None for the image output when no image is uploaded
        return None, "Por favor, sube una imagen."

    # Create a copy of the image to draw on
    image_with_box = imagen.copy()
    draw = ImageDraw.Draw(image_with_box)

    text_output = "" # Initialize text output

    if object_detector is None:
        text_output = "Error: el modelo de detecci�n de objetos no pudo cargarse."
        # Return the original image and an error message if detector fails
        return imagen, text_output

    try:
        # Realizar detecci�n de objetos
        detections = object_detector(inputs=imagen)
        print("Object detection results:", detections)

        # TODO: Ajustar 'target_fruit_label' seg�n las etiquetas reales del modelo DETR
        # y el tipo de fruta espec�fico del proyecto (ej. 'apple', 'orange', etc.)
        target_fruit_label = 'apple'
        # Filtrar por detecciones con confianza > 0.5 y la etiqueta objetivo
        # Es CRUCIAL verificar qu� etiquetas produce 'facebook/detr-resnet-50'
        # para la fruta deseada. Podr�a ser necesario ajustar este filtro.
        relevant_fruits = [det for det in detections if det['label'] == target_fruit_label and det['score'] > 0.5]

        if not relevant_fruits:
            text_output = f"No se detectaron objetos de tipo '{target_fruit_label}' en la imagen con suficiente confianza."
            # Return the original image when no relevant fruits are found
            return imagen, text_output

        # Funci�n para calcular el �rea de la caja delimitadora
        def get_box_area(box):
            return (box['xmax'] - box['xmin']) * (box['ymax'] - box['ymin'])

        # Seleccionar el objeto m�s relevante (el de mayor �rea en este caso simple)
        most_relevant_fruit = max(relevant_fruits, key=lambda det: get_box_area(det['box']))

        box = most_relevant_fruit['box']
        xmin, ymin, xmax, ymax = box['xmin'], box['ymin'], box['xmax'], box['ymax']

        # Dibujar el recuadro en la copia de la imagen
        # Las coordenadas deben ser enteros para ImageDraw
        draw.rectangle([(int(xmin), int(ymin)), (int(xmax), int(ymax))], outline="blue", width=5) # Grosor del recuadro

        # Recortar la imagen a la caja delimitadora del objeto detectado
        cropped_fruit_img = imagen.crop((int(xmin), int(ymin), int(xmax), int(ymax)))

        # Pasar la imagen recortada al modelo de clasificaci�n
        if clasificador is None:
            text_output = "Error: el modelo de clasificaci�n no pudo cargarse."
            # Return the image with the box drawn, and the classification error
            return image_with_box, text_output

        try:
            clasificacion_resultados = clasificador(inputs=cropped_fruit_img)
            print("Classification results on cropped image:", clasificacion_resultados)

            if clasificacion_resultados:
                # El modelo apple/mobilevit-small tiene etiquetas espec�ficas.
                # Necesitamos ver cu�les son para interpretar el resultado correctamente.
                # Por ahora, tomamos el primer resultado.
                mejor_prediccion = clasificacion_resultados[0]
                label = mejor_prediccion['label'] # Etiqueta predicha por mobilevit-small
                confianza = mejor_prediccion['score'] # Puntuaci�n de confianza

                # Combinar detecci�n y clasificaci�n en la salida de texto
                text_output = (
                    f"Objeto detectado (tipo DETR: '{most_relevant_fruit['label']}', "
                    f"Confianza detecci�n: {most_relevant_fruit['score']:.2f}, "
                    f"�rea: {get_box_area(box):.0f}).\n\n"
                    f"Clasificado por mobilevit-small como: '{label}' "
                    f"(Confianza clasificaci�n: {confianza:.2f})."
                )

            else:
                text_output = f"Objeto detectado de tipo '{target_fruit_label}', pero el modelo de clasificaci�n no pudo clasificarlo."

        except Exception as e:
             text_output = f"Ocurri� un error durante la clasificaci�n del objeto detectado: {e}"
             # Return the image with the box drawn, and the classification error
             return image_with_box, text_output


    except Exception as e:
        text_output = f"Ocurri� un error durante la detecci�n de objetos: {e}"
        # Return the original image and the detection error
        return imagen, text_output

    # Retornar tanto la imagen modificada como la salida de texto
    return image_with_box, text_output


# --- Definici�n de la Interfaz de Gradio ---

interfaz = gr.Interface(
    fn=clasificar_madurez_with_box,  # Usamos la funci�n que devuelve imagen y texto
    inputs=gr.Image(type="pil", label="Sube una imagen de fruta"), # Componente de entrada de imagen
    # Las salidas son una lista de componentes de Gradio
    outputs=[
        gr.Image(type="pil", label="Imagen con fruta detectada"), # Salida para la imagen con recuadro
        "text" # Salida para el texto de resultados
    ],
    title="Detector y Clasificador de Frutas (MVP Agro)",  # T�tulo de la interfaz
    description="Sube una foto de una fruta (idealmente una manzana) y la IA intentar� detectarla y clasificarla usando mobilevit-small." # Descripci�n
)

# --- Lanzar la Interfaz ---

# Esta condici�n asegura que interfaz.launch() solo se llame cuando el script se ejecuta directamente
# (�til si esto fuera un archivo .py). En Colab, lanzar directamente funciona.
if __name__ == "__main__":
    interfaz.launch()








