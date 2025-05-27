# Request para el servicio de IA

´´
[
    {
        img: "la imagen partida en bytes del lado lateral derecho del auto",
        "image_type": ImageTypeEnum.LATERAL_RIGHT,
        parts: [
            {
                name: "puerta derecha delantera",
                "daño": "abolladura"
            },
            {
                name: "puerta derecha trasera",
                "daño": "abolladura"
            },
            {
                name: "ventana derecha trasera",
                "daño": "roto"
            },

        ]
        
    },
    {
        img: "la imagen partida en bytes del lado lateral izquierdo del auto",
                "image_type": ImageTypeEnum.LATERAL_LEFT,
        parts: [
            {
                name: "puerta izquierda delantera",
                "damage": [{"damage_type": "ABOLLADURA", "description": "abolladora descripción"}] 
            },
            {
                name: "puerta izquierda trasera",
                "damage": [{"damage_type": "ABOLLADURA", "description": "abolladora descripción"}] 
            },
            {
                name: "ventana izquierda trasera",
                "damage": [{"damage_type": "ABOLLADURA", "description": "abolladora descripción"}] 
            },

        ]
        
    }
]
´´