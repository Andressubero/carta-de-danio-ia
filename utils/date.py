from PIL import Image
from PIL.ExifTags import TAGS
from datetime import datetime

def get_image_capture_date(file_storage):
    try:
        image = Image.open(file_storage)
        exif_data = image.getexif()
        if not exif_data:
            raise ValueError("SIN_EXIF")

        for tag, value in exif_data.items():
            if TAGS.get(tag) == 'DateTimeOriginal':
                try:
                    return datetime.strptime(value, '%Y:%m:%d %H:%M:%S')
                except ValueError:
                    raise ValueError("FORMATO_INVALIDO")

        raise ValueError("FECHA_NO_ENCONTRADA")

    except Exception as e:
        raise RuntimeError(f"ERROR_EXIF: {str(e)}")
