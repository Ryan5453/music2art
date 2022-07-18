import asyncio
import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from bot.core.config import debug_mode
from bot.video import do_it

logging_format = "[%(asctime)s] [%(levelname)s] %(name)s - %(message)s"
if debug_mode:
    level = logging.INFO
else:
    level = logging.INFO

logging.basicConfig(
    level=level, format="[%(asctime)s] [%(levelname)s] %(name)s - %(message)s"
)

logging.getLogger("charset_normalizer").setLevel(
    logging.FATAL
)  # It's SO noisy and completely unneeded logs

if debug_mode:
    try:
        asyncio.run(
            do_it()
        )  # When we are debugging, we don't want to run the scheduler
    except (KeyboardInterrupt, SystemExit):
        pass
    exit()

scheduler = AsyncIOScheduler()
scheduler.add_job(run_art_task, "interval", hours=1)
scheduler.start()


try:
    asyncio.get_event_loop().run_forever()
except (KeyboardInterrupt, SystemExit):
    pass
