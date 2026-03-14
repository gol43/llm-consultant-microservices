from aiogram import F, Router, types
from aiogram.filters import Command

from app.core.jwt import decode_and_validate
from app.infra.redis import get_redis
from app.tasks.llm_tasks import ask_llm_task

router = Router()


@router.message(Command("start"))
async def cmd_start(message: types.Message):
    welcome_text = (
        f"👋 Привет, {message.from_user.first_name}!\n\n"
        "Я — Bot Service для LLM-консультаций. Чтобы начать:\n"
        "1. Зарегистрируйтесь в Auth Service и получите JWT.\n"
        "2. Отправьте мне токен командой: <code>/token ваш_jwt</code>\n"
        "3. После этого вы сможете задавать вопросы нейросети."
    )
    await message.answer(welcome_text, parse_mode="HTML")


@router.message(Command("token"))
async def cmd_token(message: types.Message):
    args = message.text.split()
    if len(args) < 2:
        return await message.answer("Использование: <code>/token ваш_jwt</code>", parse_mode="HTML")

    token = args[1]
    try:
        decode_and_validate(token)
        redis_client = get_redis()
        await redis_client.set(f"token:{message.from_user.id}", token, ex=3600)
        await message.answer("Токен принят и сохранён! Можете задавать вопросы.")
        
    except ValueError as e:
        await message.answer(f"Невалидный токен: {e}")
    except Exception:
        await message.answer("Ошибка при работе с хранилищем.")


@router.message(F.text & ~F.text.startswith("/"))
async def handle_message(message: types.Message):
    redis_client = get_redis()
    token = await redis_client.get(f"token:{message.from_user.id}")
    if not token:
        return await message.answer(
            "Доступ запрещён. Сначала отправьте токен: <code>/token ваш_jwt</code>",
            parse_mode="HTML"
        )
    try:
        decode_and_validate(token)
        await message.answer("Запрос принят в очередь...")
        
        # Самое важное: Метод delay тут не запускает функцию ask_llm_task! 
        # Он упаковывает айди чата и вопрос в JSON и кидает её в RabbitMQ. На этом работа хендлера закончена. 
        # Бот свободен и ждет сообщений от других людей.
        # Публикуем задачу в RabbitMQ (через Celery)
        ask_llm_task.delay(chat_id=message.chat.id, prompt=message.text)
        
    except ValueError:
        await message.answer("Срок действия токена истёк. Получите новый в Auth Service.")