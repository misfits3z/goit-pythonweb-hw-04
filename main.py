import asyncio
from argparse import ArgumentParser
from pathlib import Path
from read_func import read_folder
from copy_func import copy_file
import logging 


logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Обробка аргументів командного рядка
parser = ArgumentParser(
    description="Copy files asynchronously into subfolders based on extension"
)
parser.add_argument("source", type=Path, help="Вихідна папка або файл")
parser.add_argument("dest", type=Path, help="Цільова папка")
parser.add_argument(
    "--chunk-size", type=int, default=65535, help="Розмір буфера копіювання"
)


async def main(args):
    try:
        tasks = []
        if args.source.is_dir():
            logging.info(f"Reading files from directory: {args.source}")
            files = await read_folder(args.source)  # Отримуємо список файлів
            for file in files:
                tasks.append(copy_file(file, args.dest, args.chunk_size))
        else:
            tasks.append(copy_file(args.source, args.dest, args.chunk_size))

        await asyncio.gather(*tasks)  # Виконуємо всі таски паралельно

    except Exception as e:
        logging.error(f"Error during execution: {e}", exc_info=True)


if __name__ == "__main__":
    asyncio.run(main(parser.parse_args()))


