# %% [markdown]
# # Comprensión espacial 2D con Gemini 2.0
# 
# Cuaderno traducido al español por Matias Barreto para enseñar comprensión espacial 2D con Gemini 2.0.

# %% [markdown]
# ## 1. Instalar el SDK
# 
# Instalá el paquete `google-genai` usando pip para acceder a la API de Gemini.


# %% [markdown]
# ## 2. Configurar la clave de API
# 
# Configurá tu clave de API de Google almacenada en un secreto de Colab o como variable de entorno. Si no tenés una clave, consultá la documentación oficial para obtenerla.

# %%
from google.colab import userdata
import os
from dotenv import dotenv_values

config = dotenv_values(".env")

GOOGLE_API_KEY = config["GOOGLE_API_KEY"]

# %% [markdown]
# ## 3. Inicializar el cliente del SDK
# 
# Inicializá el cliente de Gemini con tu clave de API para poder hacer solicitudes al modelo.

# %%
from google import genai
from google.genai import types

cliente = genai.Client(api_key=GOOGLE_API_KEY)

# %% [markdown]
# ## 4. Seleccionar y configurar el modelo
# 
# Elegí el modelo de Gemini que quieras usar y configurá el nombre según tus necesidades. Los modelos 2.5 suelen dar mejores resultados para segmentación y razonamiento avanzado.

# %%
nombre_modelo = "gemini-2.5-flash-preview-04-17" # @param ["gemini-1.5-flash-latest","gemini-2.0-flash-lite","gemini-2.0-flash","gemini-2.5-flash-preview-04-17","gemini-2.5-pro-exp-03-25"] {"allow-input":true}

# %% [markdown]
# ## 5. Definir instrucciones del sistema y configuración de seguridad
# 
# Definí las instrucciones del sistema para el modelo y configurá los parámetros de seguridad para el contenido generado.

# %%
instrucciones_sistema_bbox = """
    Devolvé los bounding boxes como un array JSON con etiquetas. Nunca devuelvas máscaras ni código. Limitá a 25 objetos.
    Si un objeto aparece varias veces, nombralos según alguna característica única (color, tamaño, posición, etc.).
"""
config_seguridad = [
    types.SafetySetting(
        category="HARM_CATEGORY_DANGEROUS_CONTENT",
        threshold="BLOCK_ONLY_HIGH",
    ),
]

# %% [markdown]
# ## 6. Importar módulos necesarios
# 
# Importá todas las librerías y módulos requeridos, como PIL, requests, io, json, numpy, etc.

# %%
import google.generativeai as genai
from PIL import Image

import io
import os
import requests
from io import BytesIO
import json
import random
import numpy as np
import base64
import dataclasses
from PIL import ImageDraw, ImageFont, ImageColor

# %% [markdown]
# ## 7. Funciones utilitarias para procesamiento y visualización
# 
# Definí funciones para parsear la salida JSON, dibujar bounding boxes y segmentaciones sobre las imágenes.

# %%
# Parsear la salida JSON del modelo
def parsear_json(salida_json: str):
    lineas = salida_json.splitlines()
    for i, linea in enumerate(lineas):
        if linea == "```json":
            salida_json = "\n".join(lineas[i+1:])
            salida_json = salida_json.split("```")[0]
            break
    return salida_json

colores_adicionales = [nombre for (nombre, _) in ImageColor.colormap.items()]

def dibujar_bounding_boxes(imagen, bounding_boxes):
    """
    Dibuja los bounding boxes sobre una imagen usando PIL y diferentes colores.
    """
    img = imagen
    ancho, alto = img.size
    draw = ImageDraw.Draw(img)
    colores = [
        'red', 'green', 'blue', 'yellow', 'orange', 'pink', 'purple', 'brown',
        'gray', 'beige', 'turquoise', 'cyan', 'magenta', 'lime', 'navy', 'maroon',
        'teal', 'olive', 'coral', 'lavender', 'violet', 'gold', 'silver'
    ] + colores_adicionales

    bounding_boxes = parsear_json(bounding_boxes)
    font = ImageFont.truetype("NotoSansCJK-Regular.ttc", size=14)

    for i, bbox in enumerate(json.loads(bounding_boxes)):
        color = colores[i % len(colores)]
        y1 = int(bbox["box_2d"][0]/1000 * alto)
        x1 = int(bbox["box_2d"][1]/1000 * ancho)
        y2 = int(bbox["box_2d"][2]/1000 * alto)
        x2 = int(bbox["box_2d"][3]/1000 * ancho)
        if x1 > x2:
            x1, x2 = x2, x1
        if y1 > y2:
            y1, y2 = y2, y1
        draw.rectangle(((x1, y1), (x2, y2)), outline=color, width=4)
        if "label" in bbox:
            draw.text((x1 + 8, y1 + 6), bbox["label"], fill=color, font=font)
    img.show()

@dataclasses.dataclass(frozen=True)
class MascaraSegmentacion:
    y0: int
    x0: int
    y1: int
    x1: int
    mascara: np.array
    etiqueta: str

def parsear_segmentaciones(salida_predicha: str, img_alto: int, img_ancho: int):
    items = json.loads(parsear_json(salida_predicha))
    mascaras = []
    for item in items:
        abs_y0 = int(item["box_2d"][0] / 1000 * img_alto)
        abs_x0 = int(item["box_2d"][1] / 1000 * img_ancho)
        abs_y1 = int(item["box_2d"][2] / 1000 * img_alto)
        abs_x1 = int(item["box_2d"][3] / 1000 * img_ancho)
        if abs_y0 >= abs_y1 or abs_x0 >= abs_x1:
            print("Bounding box inválido", item["box_2d"])
            continue
        etiqueta = item["label"]
        png_str = item["mask"]
        if not png_str.startswith("data:image/png;base64,"):
            print("Máscara inválida")
            continue
        png_str = png_str.removeprefix("data:image/png;base64,")
        png_str = base64.b64decode(png_str)
        mascara = Image.open(io.BytesIO(png_str))
        alto_bbox = abs_y1 - abs_y0
        ancho_bbox = abs_x1 - abs_x0
        if alto_bbox < 1 or ancho_bbox < 1:
            print("Bounding box inválido")
            continue
        mascara = mascara.resize((ancho_bbox, alto_bbox), resample=Image.Resampling.BILINEAR)
        np_mascara = np.zeros((img_alto, img_ancho), dtype=np.uint8)
        np_mascara[abs_y0:abs_y1, abs_x0:abs_x1] = mascara
        mascaras.append(MascaraSegmentacion(abs_y0, abs_x0, abs_y1, abs_x1, np_mascara, etiqueta))
    return mascaras

def superponer_mascara(img: Image, mascara: np.ndarray, color: str, alpha: float = 0.7) -> Image.Image:
    if not (0.0 <= alpha <= 1.0):
        raise ValueError("Alpha debe estar entre 0.0 y 1.0")
    color_rgb = ImageColor.getrgb(color)
    img_rgba = img.convert("RGBA")
    ancho, alto = img_rgba.size
    alpha_int = int(alpha * 255)
    color_rgba = color_rgb + (alpha_int,)
    capa_mascara = np.zeros((alto, ancho, 4), dtype=np.uint8)
    mascara_logica = mascara > 127
    capa_mascara[mascara_logica] = color_rgba
    capa_pil = Image.fromarray(capa_mascara, 'RGBA')
    resultado = Image.alpha_composite(img_rgba, capa_pil)
    return resultado

def dibujar_segmentaciones(img: Image, mascaras: list):
    colores = [
        'red', 'green', 'blue', 'yellow', 'orange', 'pink', 'purple', 'brown',
        'gray', 'beige', 'turquoise', 'cyan', 'magenta', 'lime', 'navy', 'maroon',
        'teal', 'olive', 'coral', 'lavender', 'violet', 'gold', 'silver'
    ] + colores_adicionales
    font = ImageFont.truetype("NotoSansCJK-Regular.ttc", size=14)
    for i, mascara in enumerate(mascaras):
        color = colores[i % len(colores)]
        img = superponer_mascara(img, mascara.mascara, color)
    draw = ImageDraw.Draw(img)
    for i, mascara in enumerate(mascaras):
        color = colores[i % len(colores)]
        draw.rectangle(((mascara.x0, mascara.y0), (mascara.x1, mascara.y1)), outline=color, width=4)
    for i, mascara in enumerate(mascaras):
        color = colores[i % len(colores)]
        if mascara.etiqueta != "":
            draw.text((mascara.x0 + 8, mascara.y0 - 20), mascara.etiqueta, fill=color, font=font)
    img.show()

# %% [markdown]
# ## 8. Descargar imágenes de ejemplo
# 
# Descargá imágenes de ejemplo desde URLs públicas para usarlas en los ejercicios del cuaderno.

# %% [markdown]
# ## 9. Cargar y mostrar una imagen
# 
# Cargá una imagen de ejemplo, redimensionala y mostrála para comenzar a trabajar sobre ella.

# %%
imagen = "Vegetables.jpg" # @param ["Socks.jpg","Vegetables.jpg","Japanese_bento.png","Cupcakes.jpg","Origamis.jpg","Fruits.jpg","Cat.jpg","Pumpkins.jpg","Breakfast.jpg","Bookshelf.jpg", "Spill.jpg"] {"allow-input":true}

im = Image.open(imagen)
im.thumbnail([620, 620], Image.Resampling.LANCZOS)
im

# %% [markdown]
# ## 10. Detectar objetos y dibujar bounding boxes
# 
# Enviá la imagen y un prompt al modelo para detectar objetos y visualizar los bounding boxes sobre la imagen.

# %%
prompt = "Detectá los bounding boxes 2D de las verduras (usá 'label' como descripción del topping)"  # @param {type:"string"}

im = Image.open(BytesIO(open(imagen, "rb").read()))
im.thumbnail([1024, 1024], Image.Resampling.LANCZOS)

respuesta = cliente.models.generate_content(
    model=nombre_modelo,
    contents=[prompt, im],
    config=types.GenerateContentConfig(
        system_instruction=instrucciones_sistema_bbox,
        temperature=0.5,
        safety_settings=config_seguridad,
    )
)

print(respuesta.text)

# %%
dibujar_bounding_boxes(im, respuesta.text)
im

# %% [markdown]
# ## 11. Buscar objetos específicos en una imagen
# 
# Ejecutá prompts personalizados para buscar y resaltar objetos específicos dentro de una imagen.

# %%
imagen = "Socks.jpg" # @param ["Socks.jpg","Vegetables.jpg","Japanese_bento.png","Cupcakes.jpg","Origamis.jpg","Fruits.jpg","Cat.jpg","Pumpkins.jpg","Breakfast.jpg","Bookshelf.jpg", "Spill.jpg"] {"allow-input":true}
prompt = "Mostrame las posiciones de las medias con carita"  # @param ["Detectá todas las medias arcoíris", "Encontrá todas las medias y etiquetalas con emojis", "Mostrame las posiciones de las medias con carita", "Encontrá la media que hace juego con la de arriba"] {"allow-input":true}

im = Image.open(imagen)
im.thumbnail([640, 640], Image.Resampling.LANCZOS)

respuesta = cliente.models.generate_content(
    model=nombre_modelo,
    contents=[prompt, im],
    config=types.GenerateContentConfig(
        system_instruction=instrucciones_sistema_bbox,
        temperature=0.5,
        safety_settings=config_seguridad,
    )
)

print(respuesta.text)
dibujar_bounding_boxes(im, respuesta.text)
im

# %% [markdown]
# ## 12. Ejemplo de razonamiento multilingüe
# 
# Pedile al modelo que etiquete objetos en la imagen usando japonés y traducción al inglés, demostrando capacidades multilingües.

# %%
imagen = "Japanese_bento.png" # @param ["Socks.jpg","Vegetables.jpg","Japanese_bento.png","Cupcakes.jpg","Origamis.jpg","Fruits.jpg","Cat.jpg","Pumpkins.jpg","Breakfast.jpg","Bookshelf.jpg", "Spill.jpg"] {"allow-input":true}
prompt = "Detectá la comida y etiquetala con caracteres japoneses y traducción al inglés."  # @param ["Detectá la comida y etiquetala con caracteres japoneses y traducción al inglés.", "Mostrame los platos veganos", "Explicá qué son esos platos en 5 palabras", "Encontrá los platos con alérgenos y etiquetalos"] {"allow-input":true}

im = Image.open(imagen)
im.thumbnail([640, 640], Image.Resampling.LANCZOS)

respuesta = cliente.models.generate_content(
    model=nombre_modelo,
    contents=[prompt, im],
    config=types.GenerateContentConfig(
        system_instruction=instrucciones_sistema_bbox,
        temperature=0.5,
        safety_settings=config_seguridad,
    )
)

dibujar_bounding_boxes(im, respuesta.text)
im

# %% [markdown]
# ## 13. Ejemplo de razonamiento espacial avanzado
# 
# Usá prompts que requieran razonamiento espacial, como encontrar sombras o dar consejos basados en la imagen.

# %%
imagen = "Origamis.jpg" # @param ["Socks.jpg","Vegetables.jpg","Japanese_bento.png","Cupcakes.jpg","Origamis.jpg","Fruits.jpg","Cat.jpg","Pumpkins.jpg","Breakfast.jpg","Bookshelf.jpg", "Spill.jpg"] {"allow-input":true}
prompt = "Dibujá un cuadrado alrededor de la sombra del zorro"  # @param ["Encontrá los dos animales de origami.", "¿Dónde están las sombras de los origamis?", "Dibujá un cuadrado alrededor de la sombra del zorro"] {"allow-input":true}

im = Image.open(imagen)
im.thumbnail([640, 640], Image.Resampling.LANCZOS)

respuesta = cliente.models.generate_content(
    model=nombre_modelo,
    contents=[prompt, im],
    config=types.GenerateContentConfig(
        system_instruction=instrucciones_sistema_bbox,
        temperature=0.5,
        safety_settings=config_seguridad,
    )
)

dibujar_bounding_boxes(im, respuesta.text)
im

# %%
imagen = "Spill.jpg" # @param ["Socks.jpg","Vegetables.jpg","Japanese_bento.png","Cupcakes.jpg","Origamis.jpg","Fruits.jpg","Cat.jpg","Pumpkins.jpg","Breakfast.jpg","Bookshelf.jpg", "Spill.jpg"] {"allow-input":true}
prompt = "Decime cómo limpiar mi mesa con una explicación como etiqueta. No solo etiquetes los objetos."  # @param ["Mostrame dónde se derramó mi café.", "Decime cómo limpiar mi mesa con una explicación como etiqueta. No solo etiquetes los objetos.", "Dibujá un cuadrado alrededor de la sombra del zorro"] {"allow-input":true}

im = Image.open(imagen)
im.thumbnail([640, 640], Image.Resampling.LANCZOS)

respuesta = cliente.models.generate_content(
    model=nombre_modelo,
    contents=[prompt, im],
    config=types.GenerateContentConfig(
        system_instruction=instrucciones_sistema_bbox,
        temperature=0.5,
        safety_settings=config_seguridad,
    )
)

dibujar_bounding_boxes(im, respuesta.text)
im

# %% [markdown]
# ## 14. Segmentación de imágenes y visualización de máscaras
# 
# Pedile al modelo máscaras de segmentación, decodificalas y superponelas sobre la imagen para una visualización avanzada.

# %%
imagen = "Cupcakes.jpg" # @param ["Socks.jpg","Vegetables.jpg","Japanese_bento.png","Cupcakes.jpg","Origamis.jpg","Fruits.jpg","Cat.jpg","Pumpkins.jpg","Breakfast.jpg","Bookshelf.jpg", "Spill.jpg"] {"allow-input":true}
prompt = "Dame las máscaras de segmentación para los objetos pequeños de metal, madera y vidrio (ignorá la mesa). Devolvé una lista JSON donde cada entrada tenga el bounding box en 'box_2d', la máscara en 'mask' y la etiqueta en 'label'. Usá etiquetas descriptivas."  # @param {type:"string"}

im = Image.open(BytesIO(open(imagen, "rb").read()))
im.thumbnail([1024, 1024], Image.Resampling.LANCZOS)

respuesta = cliente.models.generate_content(
    model=nombre_modelo,
    contents=[prompt, im],
    config=types.GenerateContentConfig(
        temperature=0.5,
        safety_settings=config_seguridad,
    )
)

print(respuesta.text)
mascaras = parsear_segmentaciones(respuesta.text, img_alto=im.size[1], img_ancho=im.size[0])
dibujar_segmentaciones(im, mascaras)

# %% [markdown]
# ## 15. Capacidades preliminares: punteo y cajas 3D
# 
# Las capacidades de punteo (pointing) y cajas 3D son experimentales en los modelos Gemini. Si te interesa explorar estas funciones avanzadas, podés consultar el siguiente cuaderno de ejemplo:
# 
# [Ejemplo de comprensión espacial 3D](../examples/Spatial_understanding_3d.ipynb)
# 
# <a href="../examples/Spatial_understanding_3d.ipynb"><img src="https://storage.googleapis.com/generativeai-downloads/images/box_3d.png" height="400"/></a>
# 

# %% [markdown]
# ## 16. ¿Qué sigue?
# 
# Para ver un ejemplo más completo y de punta a punta, podés revisar el código del [ejemplo de AI Studio](https://aistudio.google.com/starter-apps/spatial) disponible en [Github](https://github.com/google-gemini/starter-applets/tree/main/spatial).
# 
# También vas a encontrar muchos otros ejemplos de las capacidades de Gemini 2.0 en el [cookbook oficial](https://github.com/google-gemini/cookbook/tree/main/gemini-2/), incluyendo:
# 
# - [API en vivo](./Get_started_LiveAPI.ipynb)
# - [Comprensión de video](./Video_understanding.ipynb)
# - [Ejemplo de marketing de mochila a propulsión](../examples/Market_a_Jet_Backpack.ipynb)
# - [Adiviná la forma](../examples/Guess_the_shape.ipynb)
# 
# Y, por supuesto, el ejemplo de [punteo y cajas 3D](../examples/Spatial_understanding_3d.ipynb) mencionado antes.


