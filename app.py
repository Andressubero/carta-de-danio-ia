from flask import Flask, request, render_template, jsonify
import openai
import base64

app = Flask(__name__)

# Configura tu API Key (asegurate de mantenerla segura en producción)
openai.api_key = "TU_API_KEY_AQUI"

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        prompt = request.form.get("prompt")
        image_file = request.files.get("image")

        if not image_file or not prompt:
            return render_template("index.html", error="Falta imagen o prompt")

        # Convertir imagen a base64
        image_bytes = image_file.read()
        image_b64 = base64.b64encode(image_bytes).decode("utf-8")

        # Crear payload para GPT-4 Vision
        response = openai.ChatCompletion.create(
            model="gpt-4-vision-preview",
            messages=[
                {"role": "user", "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{image_b64}"
                        }
                    }
                ]}
            ],
            max_tokens=1000
        )

        result = response.choices[0].message.content
        return render_template("index.html", result=result)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
