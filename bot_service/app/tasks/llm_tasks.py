import asyncio

from app.infra.celery_app import celery_app
from app.services.openrouter_client import OpenRouterClient

# Создаем экземпляр клиента для работы с нейросетью.
llm_client = OpenRouterClient()

async def _get_llm_answer_async(prompt: str, system_instruction: str = None) -> str:
    messages = []
    if system_instruction:
        messages.append({"role": "system", "content": system_instruction})
    messages.append({"role": "user", "content": prompt})
    return await llm_client.get_completion(messages)


# Как я понял, селери юзает под капотом kombu для общения с реббитом.
# там устанавливается полноценная tcp связь между ними по порту 5672
# потом там открывается канал и потом выполняется всё то, как работает реббит под капотом
# exchanges, publish и прочее.
# потом этот обменик смотрим routing key, котоырй как я понял = селери
# и кладёт нашего джейсона в очередь

# и потом уже наш воркер как постоянный слушатель ловит наше сообщение и смотрит его параметры
# там он находит значение функции, которую нужно запустить.
# на самом деле селери под капотом делает прикольную вещь

# он извлекает поле "task": "app.tasks.llm_tasks.ask_llm_task"
# и кладёт его в свой словарик - реестр задач, и там всё сохраняет
# потом запускается execution pool - это уже дочерние процессы или потоки, которые в свою очередь берут 
# и смотрят этот реестр задач и вызывают там функции.   

# и только тогда, когда ask_llm_task выполнится без ошибок, то только потом селери отправить ACK в реббит.
# и только потом реббит окончательно удалит сообщение из очереди

async def send_to_telegram(chat_id, answer):
    """Здесь используется локальный импорт get_bot для решения проблемы цикл импортов, где-то час убил на решение"""
    from app.bot.dispatcher import get_bot
    bot = get_bot()
    try:
        await bot.send_message(chat_id=chat_id, text=answer)
    except Exception as e:
        print(f"Ошибка при отправке в TG: {e}")

@celery_app.task()
def ask_llm_task(chat_id: int, prompt: str, system_instruction: str = None):
    try:
        # Запускаем асинхронный код внутри синхронного воркера Celery.
        answer = asyncio.run(_get_llm_answer_async(prompt, system_instruction))
        asyncio.run(send_to_telegram(chat_id, answer))
        return answer # Celery сохранит этот текст в Redis (Result Backend)

    except Exception as e:
        print(f"Критическая ошибка в задаче: {e}")
        raise e
    