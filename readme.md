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