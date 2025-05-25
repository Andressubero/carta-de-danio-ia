from PIL import Image
from PIL.ExifTags import TAGS
from datetime import datetime

def get_image_capture_date(file_storage):
    try:
        image = Image.open(file_storage)
        exif_data = image._getexif()

        if not exif_data:
            raise ValueError("SIN_EXIF")

        for tag_id, value in exif_data.items():
            tag = TAGS.get(tag_id, tag_id)

        # Intentamos capturar las tres variantes comunes
        for tag_id, tag_name in [(36867, 'DateTimeOriginal'), (36868, 'DateTimeDigitized'), (306, 'DateTime')]:
            if tag_id in exif_data:
                value = exif_data[tag_id]
                try:
                    return datetime.strptime(value, '%Y:%m:%d %H:%M:%S')
                except ValueError:
                    raise ValueError(f"FORMATO_INVALIDO ({value})")

        raise ValueError("FECHA_NO_ENCONTRADA")

    except Exception as e:
        raise RuntimeError(f"ERROR_EXIF: {str(e)}")

