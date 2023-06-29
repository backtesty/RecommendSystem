# Sistema de recomendación

<!-- ABOUT THE PROJECT -->
## Acerca del proyecto

En el presente proyecto muestro la construcción de una sistema de recomendación de productos que se obtiene a través de un servicio de API gratuito, el sistema permite recomendar productos a través del lenguaje natural y más.

## Tutorial
YouTube Completo (<a href="https://youtu.be/vYR7sit3NLI">https://youtu.be/vYR7sit3NLI</a>)

## Procesos 

* Configuración de Redis - Vector Similarity
* Creación del módulo de generación de embeddings OpenAI
* Módulo de recomendación con Lenguaje Natural


<!-- GETTING STARTED -->
## Tecnologías

* Python
* Redis
* Docker
* OpenAI


### Prerequisitos

Debe tener instalado Python y Docker
* Installar Docker (<a href="https://docs.docker.com/engine/install/">https://docs.docker.com/engine/install/</a>).
* Instalar Python (<a href="https://www.python.org/downloads/">https://www.python.org/downloads/</a>).
* Obtener el API KEY de OpenAI (<a href="https://openai.com/">https://openai.com/</a>).
* Agregar el API KEY en el archivo core/Recommedation.py openai.api_key='TU_APIKEY'

* Clonar el repositorio
  ```sh
  git clone https://github.com/backtesty/RecommendSystem.git
  ```

* Crear el entorno virtual
  ```sh
  python -m venv env
  ```
* Activar entorno virtual (windows):
  ```sh
  env\Scripts\activate
  ```
* Instalar las dependencias del proyecto:
  ```sh
  pip install -r requirements.txt
  ```
* Ejecutar en docker la imagen de redis:
  ```sh
  docker run -d --name redis-stack -p 6379:6379 -p 8001:8001 redis/redis-stack:latest
  ```
* Ejecutar el sistema de recomendación:
  ```sh
  python main.py
  ```
## Finalmente

Agradezco tu visita y espero que puedas revisar más acerca del tema en mi canal de <a href="https://www.youtube.com/channel/UCxGqlLmQXjFjkrnSRLa7B7g">YouTube</a>.
