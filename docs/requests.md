´´


# Análisis de Daños en Vehículos mediante IA

Este sistema permite detectar y analizar automáticamente daños visibles en vehículos a partir de imágenes, utilizando inteligencia artificial. A través de un `prompt de entrada`, se envía una imagen junto con las partes del vehículo a evaluar. El modelo devuelve un `prompt de salida` estructurado con los resultados del análisis, incluyendo severidad del daño, nivel de confianza y comparación con una referencia.

---

## 📥 Prompt de Entrada

```json
[
  {
    "image": "url de la imagen lateral derecha",
    "image_type": "ImageTypeEnum.LATERAL_RIGHT", // hace referencia al enum
    "parts": [
      {
        "part": "puerta delantera derecha",
        "damages": [
          {
            "type": "abolladura",
            "description": "abolladora descripción"
          }
        ]
      }
    ]
  }
]
```

---

## 📤 Prompt de Salida

```json
{
  "vehiculo_valido": true,
  "tipo_imagen": "vehiculo_real",
  "tipo_vehiculo": "sedán",
  "modelo_estimado": "Dodge Charger",
  "calidad_imagen": "buena",
  "es_misma_unidad_que_referencia": true,
  "confianza_misma_unidad": 100,
  "porcentaje_danio_vehiculo_total": "40%",
  "comentarios_adicionales": "Daños importantes en la parte frontal del vehículo.",
  "comparacion_con_referencia": "Daños severos en el parachoques delantero, faros y capó. Abolladuras y rayones significativos.",
  "data": [
    {
      "image": "url de la imagen lateral derecha",
      "image_type": "ImageTypeEnum.LATERAL_RIGHT", // hace referencia al enum
      "parts": [
        {
          "name": "puerta delantera derecha",
          "severidad": "MEDIA",
          "damages": [
            {
              "type": "abolladura",
              "description": "abolladora descripción",
              "porcentaje_de_seguridad": 100,
              "presente_en_referencia": false
            }
          ]
        }
      ]
    }
  ]
}
```

---

## 📝 Notas

- Asegurate de que los nombres de las partes sean **idénticos** entre entrada y referencia.
- Las claves duplicadas fueron eliminadas para cumplir con la sintaxis JSON.
- Podés modificar las URLs de imagen para evaluar distintos ángulos del vehículo.