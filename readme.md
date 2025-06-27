# 📄 Carta de Daño IA – Backend

API desarrollada en Python que permite gestionar usuarios, vehículos y cartas de daño, con integración a IA para análisis inteligente de imágenes. Los usuarios deben estar autenticados para registrar vehículos o cargar cartas de daño.

---

## ⚙️ Tecnologías utilizadas

- Python 3.9
- Flask
- SQLAlchemy
- MySQL
- OpenAI API (opcional)

---

## 🚀 Ejecución local

### 🔁 Requisitos previos

- Python **3.9.0**
- MySQL instalado y corriendo
- Base de datos previamente creada en MySQL
- Un usuario con permisos de lectura y escritura sobre dicha base

### 🧪 Pasos para levantar el proyecto

1. **Clonar el repositorio: En tu terminal ejecuta lo siguiente**

git clone https://github.com/Andressubero/carta-de-danio-ia.git
cd carta-de-danio-ia

2. **Instalar dependencias:**

pip install -r requirements.txt


3. **Configurar las variables de entorno:**

Para ello, guíate por el archivo .env.example, recuerda que 
necesitaras la api key de gemini o gpt a usar, o ambas si quieres probar con ambas.

También necesitaras añadir los prompts que se enviarán a la IA, para ello,
crea una carpeta llamada prompts a nivel root (al mismo nivel que las otras carpetas).
En esta carpeta crea los siguientes archivos:

3.1 **paths.json**

{
    "alta_validacion": "alta.txt",
    "comparacion_validacion": "comparacion.txt"
}

3.2 **alta.txt**

Actúa como un inspector de vehículos. Analiza la imagen actual proporcionada. Responde exclusivamente con un único JSON bien formado.

Verifica si la imagen contiene un vehículo real, no un juguete, auto de videojuego, imagen renderizada, inválida, editada, photoshopeada o generada por IA.

Te llegará un objeto con la siguiente estructura (los datos son solo de ejemplo):

{
  "brand": "marca",
  "model": "modelo",
  "states": [
    {
      "image": "url de la imagen lateral derecha",
      "image_type": "LATERAL_LEFT",
      "parts": [
        {
          "part": "puerta delantera derecha",
          "damages": [
            {
              "type": "abolladura",
              "description": "abolladura descripcion"
            }
          ]
        }
      ]
    }
  ]
}

Los datos anteriores son solo un ejemplo. Debes realizar el análisis real de la imagen proporcionada y completar el JSON de respuesta con los resultados reales de tu análisis.

Debes constatar si los daños declarados están o no presentes en la imagen actual.

Condiciones clave:

- Si el vehículo de la imagen no es válido, indícalo en "additional_comments".
- Completa todos los campos en inglés, excepto "additional_comments", que debe estar en español.
- La estimación del porcentaje de daño debe ser por el vehículo completo, en el campo "total_vehicle_damage_percentage".
- "confidence_percentage" indica la certeza de detección del daño.
- Los únicos valores válidos para damages[].type son: "ABOLLADURA", "RALLON", "OTRO", "SIN_DANO", "ROTURA". No uses otros valores.
- SOLO debes incluir en states[].parts las partes que estaban en el JSON de entrada.
    - Si detectas daños en partes que NO estaban en el JSON, menciónalos en "additional_comments", pero NO los agregues en "parts".
    - Si detectas daños adicionales en una parte que sí está en el JSON, pero el daño no estaba declarado, NO lo agregues en "damages[]". Menciónalo en "additional_comments".

- El campo damages[].present_in_reference debe completarse siempre con `false`, ya que en este caso no hay imagen de referencia.

- Si existen daños presentes en la imagen que NO están reflejados en el JSON recibido, coméntalos en "additional_comments" y en "validation_reasons" con el texto:
  "Existen daños presentes en la imagen que no están declarados".

- Si "estimated_brand" no coincide con "brand", o "estimated_model" no coincide con "model", coméntalo en "additional_comments" y en "validation_reasons" con el texto:
  "La marca/modelo estimado no coincide con el declarado".

- El campo "comparison_with_reference" debe completarse siempre con el texto: "No aplica".
- El campo "is_same_unit_as_reference" debe ser siempre `true`.
- El campo "same_unit_confidence" debe ser siempre `100`.

- En los campos como "severity" que tienen como ejemplo "BAJA || MEDIA || ALTA", debes responder con uno de esos tres valores reales, según tu análisis.

Nuevo campo requerido:

- validation_reasons: debes incluir un array de strings con las razones de validación encontradas. Ejemplos de valores posibles:
    - "Existen daños presentes en la imagen que no están declarados"
    - "La imagen es de poca calidad"
    - "La marca/modelo estimado no coincide con el declarado"
    - Cualquier otra inconsistencia o detalle relevante.
    - Si no hay inconsistencias, el array puede estar vacío.

Utiliza "additional_comments" para incluir cualquier comentario adicional relevante sobre la imagen o el vehículo.

Formato de respuesta (los datos son solo de ejemplo — debes completarlos con los resultados reales de tu análisis):

{
  "is_vehicle_valid": true,
  "image_type": "vehiculo_real",
  "vehicle_type": "sedan",
  "estimated_brand": "La marca que creas que corresponde al vehiculo de la imagen",
  "estimated_model": "El modelo que creas que corresponda al vehiculo de la imagen",
  "image_quality": "BAJA || MEDIA || ALTA",
  "is_same_unit_as_reference": true,
  "same_unit_confidence": 100,
  "total_vehicle_damage_percentage": "40%",
  "additional_comments": "Daños importantes en la parte frontal del vehículo.",
  "comparison_with_reference": "No aplica",
  "validation_reasons": [
    "Existen daños presentes en la imagen que no están declarados",
    "La marca/modelo estimado no coincide con el declarado"
  ],
  "states": [
    {
      "image": "url de la imagen lateral derecha",
      "image_type": "ImageTypeEnum.LATERAL_RIGHT",
      "parts": [
        {
          "name": "puerta delantera derecha",
          "severity": "MEDIA",
          "damages": [
            {
              "type": "ABOLLADURA",
              "description": "abolladura descripción",
              "confidence_percentage": 100,
              "present_in_reference": false
            }
          ]
        }
      ]
    }
  ]
}

Importante: los datos de este JSON son solo de ejemplo. Tu respuesta debe contener los datos reales obtenidos de tu análisis.
Importante: en el json de respuesta en states.parts solamente agrega las pares que tengan algun  daño detectado por ti,
no la agregues partes sin daño aunque vengan en el json del prompt.
Responde únicamente con el JSON estructurado según el formato indicado.


3.2 **comparacion.txt**

Actúa como un inspector de vehículos. Analiza la imagen actual proporcionada y, si corresponde, compárala con una imagen de referencia.  
Responde exclusivamente con un único JSON bien formado, siguiendo el formato provisto.

Validación de la imagen:

1. Verifica si la imagen contiene un vehículo real. No debe ser un juguete, auto de videojuego, imagen renderizada, inválida, editada, photoshopeada o generada por IA.
2. Si la imagen no es válida, indícalo en "validation_reasons".

Comparación entre imagen actual y de referencia:

- La imagen de referencia representa el vehículo antes del incidente (sin daños).
- La imagen actual muestra el estado del vehículo luego del incidente.
- Compará ambas imágenes enfocándote en la misma región del vehículo para cada parte.
- Evaluá si los daños declarados como nuevos realmente no estaban en la referencia.
- Si un daño ya estaba presente (aunque sutilmente), establecé: "present_in_reference": true.

Reglas para análisis visual:

- Utilizá análisis visual y de patrones para determinar:
  - Coincidencia de daños.
  - Nuevos daños visibles.
  - Señales de edición o reutilización de imágenes.
- Si ambas imágenes son visualmente idénticas (posición, iluminación, daños), consideralas la misma imagen. Indicá esto en "validation_reasons" y "comparison_with_reference".

Validación de inconsistencias:

Incluí en "validation_reasons" un array de strings con observaciones en el caso de que tu análisis detecte lo siguiente:

- "Existen daños presentes en la imagen que no están declarados en el json"
- "Existen daños declarados en el json como nuevos que ya estaban en la imagen de referencia"
- "La imagen es de poca calidad"
- "La probabilidad de que el vehículo en la imagen de referencia y en la actual sean la misma es baja"
Esto solo debes añadirlo en en validation_reasons si tu análisis lo detecta, sino no. Si encuentras alguna otra incongruencia, puedes añadirlo también
Importante:  
Si detectás que un daño declarado como nuevo ya estaba en la referencia, debes incluir este mensaje textual en validation_reasons:

"Existen daños declarados como nuevos que ya estaban en la imagen de referencia"

Reglas específicas:

- "present_in_reference" es por daño específico: si el daño (type + description) aparece también en la referencia, debe ser true.
- "confidence_percentage" indica certeza en la detección del daño.
- "severity" debe ser uno de los siguientes: "LOW", "MID", "HIGH".
- "total_vehicle_damage_percentage" representa el daño en TODO el vehículo, como un porcentaje.
- "comparison_with_reference" describe en español las diferencias visuales detectadas.
- "additional_comments" debe incluir observaciones adicionales sobre la imagen o el análisis.

Restricciones:

- Los únicos valores válidos para damages[].type son:
  - "ABOLLADURA", "RALLON", "OTRO", "SIN_DANO", "ROTURA"
- Solo debes incluir en states[].parts las partes presentes en el JSON de entrada.
  - Si hay daños en partes no listadas → mencionarlos en "validation_reasons", pero NO agregarlos a "parts".
  - Si una parte declarada tiene daños adicionales no especificados → mencionarlo en "validation_reasons", NO agregar esos daños al array.

Formato de entrada:

{
"brand": "marca",
"model": "modelo",
"states":[
  {
    "image": "url de la imagen lateral derecha",
    "reference_image": "url de la imagen lateral derecha de referencia",
    "image_type": "LATERAL_LEFT",
    "brand": "marca",
    "model": "modelo",
    "parts": [
      {
        "part": "puerta delantera derecha",
        "damages": [
          {
            "type": "abolladura",
            "description": "abolladura descripcion"
          }
        ]
      }
    ]
  }
]
}

Formato de respuesta (completar con datos reales):

{
  "is_vehicle_valid": true,
  "image_type": "vehiculo_real",
  "vehicle_type": "sedan",
  "estimated_brand": "Dodge",
  "estimated_model": "Charger",
  "image_quality": "buena",
  "is_same_unit_as_reference": true,
  "same_unit_confidence": 100,
  "total_vehicle_damage_percentage": "40%",
  "additional_comments": "Daños importantes en la parte frontal del vehículo.",
  "comparison_with_reference": "Daños severos en el parachoques delantero, faros y capó. Abolladuras y rayones significativos.",
  "validation_reasons": [
    "Existen daños presentes en la imagen que no están declarados",
    "La imagen es de poca calidad"
  ],
  "states": [
    {
      "image": "url de la imagen lateral derecha",
      "reference_image": "url de la imagen lateral derecha de referencia",
      "image_type": "ImageTypeEnum.LATERAL_RIGHT",
      "parts": [
        {
          "name": "puerta delantera derecha",
          "severity": "MID",
          "damages": [
            {
              "type": "ABOLLADURA",
              "description": "abolladura descripción",
              "confidence_percentage": 100,
              "present_in_reference": false
            }
          ]
        }
      ]
    }
  ]
}
Importante: los datos de este JSON son solo de ejemplo. Tu respuesta debe contener los datos reales obtenidos de tu análisis.
Importante: en el json de respuesta en states.parts solamente agrega las pares que tengan algun  daño detectado por ti,
no la agregues partes sin daño aunque vengan en el json del prompt.
Importante final:  
No modifiques la estructura de entrada ni de salida. Todos los nombres de campos y el formato deben mantenerse exactamente como están.



4. **Correr la aplicación:**

python app.py

4. **Ingreso:**

Puedes ingresar creando un usuario nuevo (rol usuario) o como admin
usando el usuario creado en el seed (Ver el archivo models/user_seed.py)



## 🚀 Notas para desarrolladores:

1. **Añadir de un nuevo tipo de vehículo:**

Para añadir un nuevo tipo de vehículo es necesario modificar los siguientes archivos:

1.1 vehicle_type_seed: Se debe agregar el nombre del nuevo tipo de vehículo en
el array initial_vehicles_type.

1.2 parts_seed: este archivo solamente debe modificarse si se quiere añadir partes nuevas
que no se encuentran ya en el array initial_parts de dicho archivo. 
En el caso de añadir una nueva parte, se debe agregar en las condiciones de la función infer_image_type 
para asignarle un tipo de imagen requerida a la hora de crear una carta de daño.
Este último paso se puede obviar si el nombre de la nueva parte
contiene 'derech' o 'izquierd' ya que la función contempla esos casos actualmente.

1.3 Se debe crear un archivo nuevo dentro de la carpeta models llamado *tiponuevo*_type_part_seed,
donde tipo nuevo es el nombre del nuevo tipo de vehículo. Luego se copia el código de vehicle_type_part_seed, 
se pega en este nuevo archivo, reemplaza 'Sedán' en la linea 46 por el nombre del nuevo tipo de vehículo y
en el array initial_vehicle_type_part_names deben estar las partes correspondientes a este nuevo tipo de vehiculo.
Por último se cambia el nombre de la función que realiza el seed por seed_*nuevotipo*_type_parts.
Este archivo se encarga de crear las relaciones entre el tipo de vehículo y las partes que tiene.

1.4 Finalmente se importa y se ejecuta esa función que recien le cambiamos el nombre en el archivo app.py 
al final y dentro del bloque de código que comienza en la linea 55 (va a ser parte de ese bloque), 
Al abrir ese archivo e ir a la linea 55 se observan las importaciones y ejecuciones de los seeds.


2. **Consultar cartas de daño historicamente:**

Las cartas de daño se registran en la tabla vehicle_state con su respectiva fecha de creación.
Los registros de esta tabla tienen una relación de uno a muchos con la tabla vehicle_part_state,
la cual contiene los estados las partes que fueron subidos en dicha carta de daño.
Estas dos tablas contienen lo referente a lo que sube el usuario, mientras que la tabla ai_report
contiene el de la carta de daño.




