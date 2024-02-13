import aiofiles
import json

# Асинхронне читання файлів json з локалізаціями
async def reader_file(file_path):
    # Отримуємо файл від параметру функції, і передаємо на читання
    async with aiofiles.open(file_path, mode='r', encoding='utf-8') as translate:
        content = await translate.read()
        return json.loads(content)

async def translate(locale: str, translation_folder: str = "localisation"):
    file_path = f"{translation_folder}/{locale}.json"
    try:
        translations = await reader_file(file_path)
        # Повертаємо вміст, а вже у шаблонах прочитуємо значення ключів json
        return translations
    except FileNotFoundError:
        return {"error": f"Translation file for {locale} not found."}
