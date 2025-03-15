from pathlib import Path
from aiofile import async_open


async def copy_file(source: Path, dest_folder: Path, chunk_size: int):
    ext = source.suffix.lstrip(".") or "unknown"
    target_folder = dest_folder / ext
    target_folder.mkdir(parents=True, exist_ok=True)
    destination = target_folder / source.name #шлях до нового файлу

    async with async_open(source, "rb") as src, async_open(destination, "wb") as dest:
        async for chunk in src.iter_chunked(chunk_size): #читаємо шматками і записуємо в новий файл
            await dest.write(chunk)


