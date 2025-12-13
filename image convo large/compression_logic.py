import io

def compress_to_target_size(image, target_size_kb, output_format_pil):
    """
    Iteratively lowers quality (1-100) to reach a target file size (KB).
    """
    target_size_bytes = target_size_kb * 1024
    current_quality = 90

    if output_format_pil not in ["JPEG", "WEBP"]:
        return current_quality

    while current_quality > 5:
        img_byte_arr = io.BytesIO()
        current_quality -= 5
        try:
            # Use image.copy() to ensure the image object is fresh for the save operation
            image.save(img_byte_arr, format=output_format_pil, quality=current_quality)
            if img_byte_arr.tell() <= target_size_bytes:
                return current_quality
        except Exception:
            break
    return 5