from celery import Celery

from app.core.config import settings

# Для меня селери достаточно новая технология, обычно юзал background_task у фастапи

# тут мы по сути инициализиурем объект селери и передаём параметры:
# 1. название приложения
# 2. наш брокер сообщений (куда телега сможет вешать задания и убегать обратно, чтобы ловить другие задания)
# 3. и бд для резульатов (сюда будем сгружать все ответы для спокойствия)
# Но мне очень интересно, как тут решается проблема идемпотентности и тот вопрос, что если будет два пользователя, то они получат только свои ответы ИИ?

celery_app = Celery(
    "bot_service",
    broker=settings.RABBITMQ_URL,
    backend=settings.REDIS_URL,  
)

# Конфигурация
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="Europe/Kaliningrad", # Я из Калининграда :))
    enable_utc=True,
    include=["app.tasks.llm_tasks"] # мы тут говорим селери, где нужно искать задачи, без этого воркер не поймёт, чё ему делать
)