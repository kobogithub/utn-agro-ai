#!/usr/bin/env python3
"""
Comprensión espacial 2D con Gemini 2.0
Script autónomo para ejecutar en contenedor Docker
Traducido al español por Matias Barreto
"""

import os
import io
import json
import random
import base64
import requests
import dataclasses
import logging
import sys
from io import BytesIO
from typing import List, Tuple
from pathlib import Path
from datetime import datetime

# Importaciones de librerías externas
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageColor
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Cargar variables de entorno
load_dotenv()

# Configurar logging
def configurar_logging(nivel_log: str = "INFO") -> logging.Logger:
    """Configura el sistema de logging con formato personalizado"""
    
    # Crear logger
    logger = logging.getLogger("gemini_spatial")
    logger.setLevel(getattr(logging, nivel_log.upper()))
    
    # Evitar duplicar handlers si ya existen
    if logger.handlers:
        return logger
    
    # Crear formatter personalizado
    formatter = logging.Formatter(
        '%(asctime)s | %(levelname)-8s | %(message)s',
        datefmt='%H:%M:%S'
    )
    
    # Handler para consola con colores
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # Handler para archivo de logs (opcional)
    log_file = Path("logs") / f"gemini_spatial_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    log_file.parent.mkdir(exist_ok=True)
    
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    return logger

# Inicializar logger
logger = configurar_logging(os.getenv('LOG_LEVEL', 'INFO'))

# Configuración
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
if not GOOGLE_API_KEY:
    logger.error("GOOGLE_API_KEY no está configurada en las variables de entorno")
    raise ValueError("GOOGLE_API_KEY no está configurada en las variables de entorno")

# Inicializar cliente
cliente = genai.Client(api_key=GOOGLE_API_KEY)

# Configuración del modelo
NOMBRE_MODELO = "gemini-2.5-flash"

# Instrucciones del sistema
INSTRUCCIONES_SISTEMA_BBOX = """
    Devolvé los bounding boxes como un array JSON con etiquetas. Nunca devuelvas máscaras ni código. Limitá a 25 objetos.
    Si un objeto aparece varias veces, nombralos según alguna característica única (color, tamaño, posición, etc.).
"""

# Configuración de seguridad
CONFIG_SEGURIDAD = [
    types.SafetySetting(
        category="HARM_CATEGORY_DANGEROUS_CONTENT",
        threshold="BLOCK_ONLY_HIGH",
    ),
]

# URLs de imágenes de ejemplo
URLS_IMAGENES = {
    "Socks.jpg": "https://storage.googleapis.com/generativeai-downloads/images/socks.jpg",
    "Vegetables.jpg": "https://storage.googleapis.com/generativeai-downloads/images/vegetables.jpg",
    "Japanese_bento.png": "https://storage.googleapis.com/generativeai-downloads/images/Japanese_Bento.png",
    "Cupcakes.jpg": "https://storage.googleapis.com/generativeai-downloads/images/Cupcakes.jpg",
    "Origamis.jpg": "https://storage.googleapis.com/generativeai-downloads/images/origamis.jpg",
    "Fruits.jpg": "https://storage.googleapis.com/generativeai-downloads/images/fruits.jpg",
    "Cat.jpg": "https://storage.googleapis.com/generativeai-downloads/images/cat.jpg",
    "Pumpkins.jpg": "https://storage.googleapis.com/generativeai-downloads/images/pumpkins.jpg",
    "Breakfast.jpg": "https://storage.googleapis.com/generativeai-downloads/images/breakfast.jpg",
    "Bookshelf.jpg": "https://storage.googleapis.com/generativeai-downloads/images/bookshelf.jpg",
    "Spill.jpg": "https://storage.googleapis.com/generativeai-downloads/images/spill.jpg"
}

def descargar_imagenes(directorio_imagenes: str = "images"):
    """Descarga las imágenes de ejemplo si no existen"""
    Path(directorio_imagenes).mkdir(exist_ok=True)
    logger.info(f"Verificando imágenes en directorio: {directorio_imagenes}")
    
    imagenes_descargadas = 0
    imagenes_existentes = 0
    
    for nombre_archivo, url in URLS_IMAGENES.items():
        ruta_archivo = Path(directorio_imagenes) / nombre_archivo
        
        if not ruta_archivo.exists():
            logger.info(f"Descargando {nombre_archivo}...")
            try:
                response = requests.get(url, timeout=30)
                response.raise_for_status()
                
                with open(ruta_archivo, 'wb') as f:
                    f.write(response.content)
                
                # Verificar tamaño del archivo
                tamaño_kb = ruta_archivo.stat().st_size / 1024
                logger.info(f"✓ {nombre_archivo} descargada ({tamaño_kb:.1f} KB)")
                imagenes_descargadas += 1
                
            except Exception as e:
                logger.error(f"✗ Error descargando {nombre_archivo}: {e}")
        else:
            logger.debug(f"✓ {nombre_archivo} ya existe")
            imagenes_existentes += 1
    
    logger.info(f"Resumen: {imagenes_existentes} existentes, {imagenes_descargadas} descargadas")

def parsear_json(salida_json: str) -> str:
    """Parsea la salida JSON del modelo"""
    logger.debug("Parseando respuesta JSON del modelo...")
    lineas = salida_json.splitlines()
    for i, linea in enumerate(lineas):
        if linea == "```json":
            salida_json = "\n".join(lineas[i+1:])
            salida_json = salida_json.split("```")[0]
            logger.debug(f"JSON extraído: {len(salida_json)} caracteres")
            break
    return salida_json

def obtener_colores():
    """Obtiene una lista de colores para dibujar"""
    colores_base = [
        'red', 'green', 'blue', 'yellow', 'orange', 'pink', 'purple', 'brown',
        'gray', 'beige', 'turquoise', 'cyan', 'magenta', 'lime', 'navy', 'maroon',
        'teal', 'olive', 'coral', 'lavender', 'violet', 'gold', 'silver'
    ]
    colores_adicionales = [nombre for (nombre, _) in ImageColor.colormap.items()]
    return colores_base + colores_adicionales

def obtener_fuente():
    """Obtiene la fuente para dibujar texto"""
    try:
        return ImageFont.truetype("/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc", size=14)
    except:
        try:
            return ImageFont.truetype("arial.ttf", size=14)
        except:
            return ImageFont.load_default()

def dibujar_bounding_boxes(imagen: Image.Image, bounding_boxes: str, archivo_salida: str = None) -> Image.Image:
    """Dibuja los bounding boxes sobre una imagen"""
    img = imagen.copy()
    
    # Convertir a RGB si tiene transparencia (evita error RGBA -> JPEG)
    if img.mode in ('RGBA', 'P'):
        # Crear fondo blanco para transparencias
        rgb_img = Image.new('RGB', img.size, (255, 255, 255))
        if img.mode == 'P':
            img = img.convert('RGBA')
        rgb_img.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
        img = rgb_img
    
    ancho, alto = img.size
    draw = ImageDraw.Draw(img)
    colores = obtener_colores()
    
    bounding_boxes_parsed = parsear_json(bounding_boxes)
    font = obtener_fuente()
    
    try:
        boxes_data = json.loads(bounding_boxes_parsed)
        
        for i, bbox in enumerate(boxes_data):
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
    
    except Exception as e:
        print(f"Error dibujando bounding boxes: {e}")
    
    if archivo_salida:
        # Crear directorio de salida si no existe
        output_path = Path(archivo_salida)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Guardar imagen en formato RGB
        img.save(output_path, 'JPEG', quality=95)
        print(f"Imagen guardada en: {output_path.absolute()}")
    
    return img

@dataclasses.dataclass(frozen=True)
class MascaraSegmentacion:
    y0: int
    x0: int
    y1: int
    x1: int
    mascara: np.array
    etiqueta: str

def parsear_segmentaciones(salida_predicha: str, img_alto: int, img_ancho: int) -> List[MascaraSegmentacion]:
    """Parsea las máscaras de segmentación"""
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

def detectar_objetos(imagen_path: str, prompt: str, directorio_salida: str = "output") -> str:
    """Detecta objetos en una imagen usando Gemini"""
    logger.info(f"🔍 Analizando imagen: {Path(imagen_path).name}")
    logger.debug(f"Prompt: {prompt}")
    
    try:
        # Cargar imagen
        logger.debug("Cargando y redimensionando imagen...")
        im = Image.open(imagen_path)
        tamaño_original = im.size
        im.thumbnail([1024, 1024], Image.Resampling.LANCZOS)
        tamaño_procesado = im.size
        
        logger.debug(f"Tamaño original: {tamaño_original}, procesado: {tamaño_procesado}")
        
        # Generar contenido
        logger.info("🤖 Enviando solicitud a Gemini...")
        respuesta = cliente.models.generate_content(
            model=NOMBRE_MODELO,
            contents=[prompt, im],
            config=types.GenerateContentConfig(
                system_instruction=INSTRUCCIONES_SISTEMA_BBOX,
                temperature=0.5,
                safety_settings=CONFIG_SEGURIDAD,
            )
        )
        
        logger.info("✅ Respuesta recibida del modelo")
        logger.debug(f"Respuesta completa: {respuesta.text}")
        
        # Parsear respuesta para contar objetos detectados
        try:
            json_response = parsear_json(respuesta.text)
            objetos = json.loads(json_response)
            logger.info(f"🎯 Detectados {len(objetos)} objetos en la imagen")
        except:
            logger.warning("No se pudo contar los objetos detectados")
        
        # Crear directorio de salida
        Path(directorio_salida).mkdir(parents=True, exist_ok=True)
        
        # Dibujar bounding boxes y guardar
        nombre_archivo = f"output_{Path(imagen_path).stem}_bbox.jpg"
        archivo_salida = Path(directorio_salida) / nombre_archivo
        
        logger.info("🎨 Dibujando bounding boxes...")
        imagen_con_boxes = dibujar_bounding_boxes(im, respuesta.text, str(archivo_salida))
        
        return respuesta.text
        
    except Exception as e:
        logger.error(f"❌ Error procesando {imagen_path}: {e}")
        raise

def ejecutar_ejemplos():
    """Ejecuta varios ejemplos de detección de objetos"""
    
    logger.info("📥 Preparando imágenes de ejemplo...")
    descargar_imagenes()
    
    ejemplos = [
        {
            "imagen": "images/Vegetables.jpg",
            "prompt": "Detectá los bounding boxes 2D de las verduras (usá 'label' como descripción del topping)",
            "descripcion": "Detección de verduras múltiples"
        },
        {
            "imagen": "images/Socks.jpg", 
            "prompt": "Mostrame las posiciones de las medias con carita",
            "descripcion": "Búsqueda de objetos específicos"
        },
        {
            "imagen": "images/Japanese_bento.png",
            "prompt": "Detectá la comida y etiquetala con caracteres japoneses y traducción al inglés.",
            "descripcion": "Etiquetado multilingüe (japonés/inglés)"
        },
        {
            "imagen": "images/Origamis.jpg",
            "prompt": "Dibujá un cuadrado alrededor de la sombra del zorro",
            "descripcion": "Razonamiento espacial avanzado"
        }
    ]
    
    # Crear directorio de salida
    directorio_salida = "output"
    Path(directorio_salida).mkdir(parents=True, exist_ok=True)
    logger.info(f"📁 Directorio de salida configurado: {directorio_salida}")
    
    logger.info(f"🚀 Ejecutando {len(ejemplos)} ejemplos de análisis...")
    
    ejemplos_exitosos = 0
    ejemplos_fallidos = 0
    
    for i, ejemplo in enumerate(ejemplos, 1):
        logger.info(f"\n--- Ejemplo {i}/{len(ejemplos)}: {ejemplo['descripcion']} ---")
        
        if not Path(ejemplo["imagen"]).exists():
            logger.error(f"❌ Imagen no encontrada: {ejemplo['imagen']}")
            ejemplos_fallidos += 1
            continue
        
        try:
            detectar_objetos(ejemplo["imagen"], ejemplo["prompt"], directorio_salida)
            logger.info(f"✅ Ejemplo {i} completado exitosamente")
            ejemplos_exitosos += 1
            
        except Exception as e:
            logger.error(f"❌ Error en ejemplo {i}: {e}")
            ejemplos_fallidos += 1
    
    # Verificar archivos generados
    archivos_generados = list(Path(directorio_salida).glob("*.jpg"))
    
    logger.info("\n" + "="*50)
    logger.info("📊 RESUMEN DE EJECUCIÓN")
    logger.info("="*50)
    logger.info(f"✅ Ejemplos exitosos: {ejemplos_exitosos}")
    logger.info(f"❌ Ejemplos fallidos: {ejemplos_fallidos}")
    logger.info(f"📁 Archivos generados: {len(archivos_generados)}")
    
    if archivos_generados:
        logger.info(f"\n📁 Archivos en '{directorio_salida}/':")
        for archivo in archivos_generados:
            tamaño_kb = archivo.stat().st_size / 1024
            logger.info(f"  ✓ {archivo.name} ({tamaño_kb:.1f} KB)")
    else:
        logger.warning("⚠️  No se generaron archivos de salida")
    
    return ejemplos_exitosos, ejemplos_fallidos

def verificar_entorno():
    """Verifica que el entorno esté correctamente configurado"""
    logger.info("🔍 Verificando configuración del entorno...")
    
    # Verificar API key
    if not GOOGLE_API_KEY or GOOGLE_API_KEY == "your_api_key_here":
        logger.error("GOOGLE_API_KEY no está configurada correctamente")
        raise ValueError("GOOGLE_API_KEY no está configurada correctamente")
    
    logger.info("✓ API key de Google configurada")
    
    # Verificar directorio actual
    directorio_trabajo = Path.cwd().absolute()
    logger.info(f"✓ Directorio de trabajo: {directorio_trabajo}")
    
    # Crear y verificar directorio de salida
    output_dir = Path("output")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Probar escritura
    test_file = output_dir / "test.txt"
    try:
        test_file.write_text("test")
        test_file.unlink()  # Eliminar archivo de prueba
        logger.info(f"✓ Directorio de salida escribible: {output_dir.absolute()}")
    except Exception as e:
        logger.warning(f"⚠️  Problema con directorio de salida: {e}")
        raise
    
    # Verificar conexión a la API (opcional)
    try:
        logger.debug("Verificando conexión con la API de Gemini...")
        # Test básico de conexión (sin gastar tokens)
        cliente_test = genai.Client(api_key=GOOGLE_API_KEY)
        logger.debug("✓ Cliente de Gemini inicializado correctamente")
    except Exception as e:
        logger.warning(f"⚠️  Problema con la API de Gemini: {e}")
    
    logger.info("✅ Entorno verificado correctamente")

def main():
    """Función principal"""
    inicio = datetime.now()
    
    logger.info("🚀 Iniciando análisis espacial 2D con Gemini")
    logger.info(f"🤖 Modelo: {NOMBRE_MODELO}")
    logger.info(f"🕒 Hora de inicio: {inicio.strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        verificar_entorno()
        exitosos, fallidos = ejecutar_ejemplos()
        
        # Calcular tiempo transcurrido
        duracion = datetime.now() - inicio
        logger.info(f"\n⏱️  Tiempo total de ejecución: {duracion.total_seconds():.1f} segundos")
        
        # Resumen final
        if fallidos == 0:
            logger.info("🎉 Análisis completado exitosamente - Todos los ejemplos funcionaron")
            return 0
        else:
            logger.warning(f"⚠️  Análisis completado con {fallidos} errores de {exitosos + fallidos} ejemplos")
            return 1
            
    except KeyboardInterrupt:
        logger.warning("❌ Ejecución interrumpida por el usuario")
        return 130
    except Exception as e:
        logger.error(f"❌ Error crítico durante la ejecución: {e}")
        logger.debug("Detalles del error:", exc_info=True)
        return 1

if __name__ == "__main__":
    # Mostrar información de logging al usuario
    log_dir = Path("logs")
    if log_dir.exists():
        log_files = list(log_dir.glob("*.log"))
        if log_files:
            latest_log = max(log_files, key=lambda x: x.stat().st_mtime)
            print(f"📋 Logs detallados en: {latest_log}")
    
    exit(main())