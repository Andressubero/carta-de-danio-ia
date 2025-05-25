import uuid
from app import db
from .models import Image

# Lista de imágenes iniciales
initial_images = [
    {"url": "https://example.com/image1.jpg"},
    {"url": "https://example.com/image2.jpg"},
    {"url": "https://example.com/image3.jpg"}
]

def seed_images():
    for item in initial_images:
        existing = db.session.query(Image).filter_by(url=item["url"]).first()
        if not existing:
            image = Image(
                id=uuid.uuid4(),
                url=item["url"]
            )
            db.session.add(image)

    db.session.commit()
    print("✅ Seeding de imágenes completado.")

if __name__ == "__main__":
    seed_images()