import asyncio

from fastapi import FastAPI

from app.bot.dispatcher import get_bot, get_dispatcher

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}

async def main():
    bot = get_bot()
    dp = get_dispatcher()
    
    print("Бот запущен...")
    # Наверное лучше было бы работать с вебхуками, но мне показалось, что это итак overhead
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())