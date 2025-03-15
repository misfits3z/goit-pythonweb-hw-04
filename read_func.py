import logging
from pathlib import Path


async def read_folder(source: Path):
    """Recursively reads all files in the source folder and its subfolders"""
    try:
        tasks = []

        # Рекурсивно обходимо всі файли і папки
        async def read_dir(directory):
            for entry in directory.iterdir():
                if entry.is_dir():
                    await read_dir(entry)  # Рекурсивно викликаємо для підкаталогів
                elif entry.is_file():
                    tasks.append(entry)  # Додаємо файли до списку

        await read_dir(source)  # Початковий виклик для кореневої папки
        logging.info(f"Found {len(tasks)} files in {source}.")
        return tasks

    except Exception as e:
        logging.error(f"Error reading folder {source}: {e}", exc_info=True)
        return []


