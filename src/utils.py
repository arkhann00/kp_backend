

from pathlib import Path
import uuid

from fastapi import UploadFile, HTTPException


UPLOAD_DIR = Path("uploads/products")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "webp", "gif"}

MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB

async def save_product_image(file: UploadFile):
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=400, 
            detail="Файл должен быть изображением"
        )
    
    # Проверка расширения
    if not file.filename:
        raise HTTPException(status_code=400, detail="Имя файла отсутствует")
    
    file_extension = file.filename.split(".")[-1].lower()
    if file_extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Разрешенные форматы: {', '.join(ALLOWED_EXTENSIONS)}"
        )
    
    # Читаем содержимое
    content = await file.read()
    
    # Проверка размера
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail=f"Файл слишком большой. Максимум: {MAX_FILE_SIZE / 1024 / 1024}MB"
        )
    
    # Генерируем уникальное имя
    unique_filename = f"{uuid.uuid4()}.{file_extension}"
    file_path = UPLOAD_DIR / unique_filename
    
    # Сохраняем файл
    with open(file_path, "wb") as f:
        f.write(content)
    
    # Возвращаем относительный путь
    return f"/uploads/products/{unique_filename}"


def delete_product_image(image_url: str):
    try:
        # Убираем ведущий слэш и создаем Path
        file_path = Path(image_url.lstrip("/"))
        
        if file_path.exists():
            file_path.unlink()
            return True
        return False
    except Exception:
        return False