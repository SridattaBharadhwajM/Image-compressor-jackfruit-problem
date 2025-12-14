import os
import io
from PIL import Image
OUTPUT_FORMATS = ["JPEG", "PNG", "WEBP", "TIFF", "BMP"]
def open_image_simple(filepath):
    """Open images using PIL and ensures RGB/L mode."""
    try:
        image = Image.open(filepath)
        if image.mode not in ('RGB', 'L', 'RGBA'):
            image = image.convert('RGB')
        return image
    except Exception:
        return None
def format_to_pil_ext(fmt_text):
    """Map user-visible format text to PIL format string."""
    if fmt_text.lower() in ["jpeg", "jpg"]:
        return "JPEG"
    return fmt_text.upper()
def save_image_processed(image, output_path, output_format_pil, final_quality):
    """Handles saving the image with quality and format checks."""
    # Handle transparency for formats like JPEG or BMP
    if output_format_pil in ["JPEG", "BMP"] and image.mode in ['RGBA', 'P']:
        background = Image.new("RGB", image.size, (255, 255, 255))
        mask = image.split()[-1] if image.mode == 'RGBA' else None
        background.paste(image, mask=mask)
        image = background
    save_args = {'format': output_format_pil}
    if output_format_pil in ["JPEG", "WEBP"]:
        save_args['quality'] = int(final_quality)
    try:
        image.save(output_path, **save_args)
        return True
    except Exception:
        return False