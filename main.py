from aiogram import executor
import os
from misc import dp, bot
import ll
#run
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)