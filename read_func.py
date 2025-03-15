from pathlib import Path
import asyncio

async def read_folder(source: Path):
    """Рекурсивно читаємо всі файли з папки"""
    task = []
    for entry in source.iterdir():
        if entry.is_dir():
            task.append(read_folder(entry))  # Рекурсивно обробляємо папку
        elif entry.is_file():
            task.append(entry)  # Додаємо файл у список для копіювання

    return await asyncio.gather(*task) if task else []
