# UTN Agro AI - Curso de LLMs

Repositorio de contenido de módulos en el programa "Desarrollo Avanzado de Soluciones de IA"

**Autores:** Kevin Barroso, Matías Barreto

## 📋 Contenido del Curso

### Módulo 1: Introducción a LLMs
- **00 - Índice**: Introducción general al curso
- **01 - Clase 01**: Actualización de información y búsqueda web
- **02 - Clase 01**: Solución de ejercicios de búsqueda web
- **03 - Clase 02**: ChatGPT API - Ejemplo mínimo y conceptos básicos
- **04 - Clase 03**: OpenAI API - Scraping y extracción de datos
- **05 - Clase 04**: Claude API - Ejemplos y visión por computadora
- **06 - Clase 05**: Gemini API - Ejemplos y tareas de PLN
- **07 - Clase 06**: APIs de datos climáticos y visualización
- **08 - Clase 07**: A/B Testing con OpenAI - Experimentos y evaluación
- **09 - Clase 08**: A/B Testing con Gemini - Experimentos
- **10 - Clase 09**: Ollama - Modelos locales
- **11 - Clase 09**: LM Studio - Interfaz para modelos locales

## 🔧 Configuración del Entorno

### 1. Clonar el Repositorio
```bash
git clone https://github.com/kobogithub/utn-agro-ai.git
cd utn-agro-ai
```

### 2. Configurar Variables de Entorno

#### Para uso local:
1. Copia el archivo de ejemplo:
   ```bash
   cp .env.example .env
   ```

2. Edita el archivo `.env` y completa tus API keys:
   ```env
   # OpenAI API Key
   OPENAI_API_KEY=tu_openai_api_key_aqui
   
   # Anthropic API Key (Claude)
   ANTHROPIC_API_KEY=tu_anthropic_api_key_aqui
   
   # Google API Key (Gemini)
   GOOGLE_API_KEY=tu_google_api_key_aqui
   ```

#### Para uso en Google Colab:
Los notebooks detectan automáticamente si se ejecutan en Colab y utilizarán los secretos de Colab. Configura tus API keys en:
- Colab → Secretos → Agregar nuevo secreto
- Nombres de secretos: `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `GOOGLE_API_KEY`

### 3. Obtener API Keys

#### OpenAI API Key
1. Visita [https://platform.openai.com/account/api-keys](https://platform.openai.com/account/api-keys)
2. Crea una nueva API key
3. Copia la clave y pégala en tu archivo `.env`

#### Anthropic API Key (Claude)
1. Visita [https://console.anthropic.com/](https://console.anthropic.com/)
2. Crea una cuenta y genera una API key
3. Copia la clave y pégala en tu archivo `.env`

#### Google API Key (Gemini)
1. Visita [https://makersuite.google.com/app/apikey](https://makersuite.google.com/app/apikey)
2. Crea una nueva API key
3. Copia la clave y pégala en tu archivo `.env`

## 🚀 Uso de los Notebooks

### Instalación de Dependencias
Cada notebook instala automáticamente las dependencias necesarias. Las principales librerías utilizadas son:
- `openai` - Para interactuar con la API de OpenAI
- `anthropic` - Para interactuar con la API de Claude
- `google-genai` - Para interactuar con la API de Gemini
- `python-dotenv` - Para cargar variables de entorno
- `requests` - Para realizar peticiones HTTP
- `beautifulsoup4` - Para web scraping

### Estructura de los Notebooks
Todos los notebooks han sido refactorizados para seguir las mejores prácticas:

1. **Detección automática de entorno**: Los notebooks detectan si se ejecutan en Colab o localmente
2. **Carga segura de API keys**: Utiliza `python-dotenv` para entornos locales y secretos de Colab
3. **Manejo de errores**: Mensajes claros si faltan las API keys
4. **Compatibilidad**: Funciona tanto en Jupyter local como en Google Colab

### Ejemplo de Uso
```python
# El código de configuración está incluido en cada notebook
# Solo necesitas ejecutar las celdas en orden

# 1. Instalar dependencias y cargar API keys
!pip install openai python-dotenv --quiet
from openai import OpenAI
import os
from dotenv import load_dotenv

# 2. Configuración automática
load_dotenv()
# ... código de detección de entorno ...

# 3. Usar la API
client = OpenAI(api_key=OPENAI_API_KEY)
response = client.chat.completions.create(...)
```

## 🔒 Seguridad

- **Nunca** commits tus API keys al repositorio
- El archivo `.env` está incluido en `.gitignore` para prevenir commits accidentales
- Usa el archivo `.env.example` como plantilla
- En Colab, utiliza la función de secretos integrada

## 🛠️ Herramientas de Desarrollo

### GitHub Cuenta

[GitHub](https://github.com/) es la plataforma de desarrollo colaborativo más popular del mundo, basada en Git. Permite a los desarrolladores:

- **Control de versiones distribuido**: Rastrea cambios en el código fuente durante el desarrollo de software
- **Colaboración en equipo**: Múltiples desarrolladores pueden trabajar en el mismo proyecto simultáneamente
- **Repositorios públicos y privados**: Almacena y organiza proyectos de código
- **Issues y Pull Requests**: Sistema de seguimiento de errores y revisión de código
- **GitHub Actions**: Automatización de flujos de trabajo CI/CD
- **GitHub Pages**: Hosting gratuito para sitios web estáticos

**Características principales:**
- Interfaz web intuitiva para gestión de repositorios
- Integración con herramientas de desarrollo
- Comunidad activa de desarrolladores
- Documentación y wikis integradas

### Instalación de Git

Control de Versiones [Git](https://git-scm.com/)

### Instalación de Python

Lenguaje de programación [Python](https://www.python.org/)

Entorno Virtual de [Python Virtualenv](https://realpython.com/python-virtual-environments-a-primer/)

### Extensiones VSCode

Para una mejor experiencia de desarrollo, se recomienda instalar las siguientes extensiones en Visual Studio Code:

- **Python**: Soporte completo para Python
- **Jupyter**: Para trabajar con notebooks
- **Python Docstring Generator**: Generación automática de docstrings
- **GitLens**: Mejoras para Git
- **Pylance**: Language server para Python

## 🤝 Contribuciones

Este es un proyecto educativo. Si encuentras errores o tienes sugerencias:
1. Abre un issue describiendo el problema
2. Propón mejoras mediante pull requests
3. Asegúrate de no incluir API keys en tus contribuciones

## 📚 Recursos Adicionales

### Documentación de APIs
- [OpenAI API Documentation](https://platform.openai.com/docs)
- [Anthropic Claude API Documentation](https://docs.anthropic.com/)
- [Google Gemini API Documentation](https://ai.google.dev/docs)

### Tutoriales Relacionados
- [DeepLearning.AI ChatGPT Prompt Engineering](https://learn.deeplearning.ai/chatgpt-prompt-eng/)
- [Anthropic Claude Documentation](https://docs.anthropic.com/)

## 📄 Licencia

Este proyecto es de uso educativo para la UTN. Consulta con los instructores sobre el uso y distribución del material.

## 🆘 Soporte

Si tienes problemas con la configuración:
1. Verifica que tus API keys sean válidas
2. Asegúrate de que el archivo `.env` esté en la raíz del proyecto
3. Revisa que las dependencias estén instaladas correctamente
4. Consulta los logs de error para más detalles

---

**Desarrollado para UTN - Universidad Tecnológica Nacional**  
**Curso: Introducción a Large Language Models aplicados a la Agroindustria**
