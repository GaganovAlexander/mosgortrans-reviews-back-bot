from asyncio import run

from tg_bot.main import main
from db import create_tables


if __name__ == '__main__':
    create_tables()
    run(main())
