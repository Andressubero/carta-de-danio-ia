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

