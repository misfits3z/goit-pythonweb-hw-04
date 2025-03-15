import asyncio
from argparse import ArgumentParser
from pathlib import Path
from aiofile import async_open

# обробка аргументів командного рядка
parser = ArgumentParser(
    description="Copy files asynchronously into subfolders based on extension"
)
parser.add_argument("source", type=Path) #вихідна папка
parser.add_argument("dest", type=Path)  #цільова папка
parser.add_argument("--chunk-size", type=int, default=65535)


async def copy_file(source: Path, dest_folder: Path, chunk_size: int):
    ext = source.suffix.lstrip(".") or "unknown"
    target_folder = dest_folder / ext
    target_folder.mkdir(parents=True, exist_ok=True)
    destination = target_folder / source.name #шлях до нового файлу

    async with async_open(source, "rb") as src, async_open(destination, "wb") as dest:
        async for chunk in src.iter_chunked(chunk_size): #читаємо шматками і записуємо в новий файл
            await dest.write(chunk)


async def main(args):
    tasks = []
    if args.source.is_dir():
        for file in args.source.iterdir():
            if file.is_file():
                tasks.append(copy_file(file, args.dest, args.chunk_size))
    else:
        tasks.append(copy_file(args.source, args.dest, args.chunk_size))

    await asyncio.gather(*tasks) #всі асинхроні таски запускаємо одночасно


if __name__ == "__main__": 
    asyncio.run(main(parser.parse_args()))
