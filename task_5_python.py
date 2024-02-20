import asyncio
from enum import Enum
from typing import Optional
from dataclasses import dataclass
from datetime import datetime, timedelta
import random

# Определение таймаута для операции
timeout_seconds = timedelta(seconds=15).total_seconds()

class Response(Enum):
    Success = 1
    RetryAfter = 2
    Failure = 3

class ApplicationStatusResponse(Enum):
    Success = 1
    Failure = 2

@dataclass
class ApplicationResponse:
    application_id: str
    status: ApplicationStatusResponse
    description: str
    last_request_time: datetime
    retriesCount: Optional[int] = None

async def get_application_status1(identifier: str) -> Response:
    # Имитация ответа сервиса
    await asyncio.sleep(random.uniform(0.5, 2.0))  # Имитация задержки сети
    return random.choice(list(Response))

async def get_application_status2(identifier: str) -> Response:
    # Имитация ответа сервиса
    await asyncio.sleep(random.uniform(0.5, 2.0))  # Имитация задержки сети
    return random.choice(list(Response))

async def perform_operation(identifier: str) -> ApplicationResponse:
    start_time = datetime.now()
    retries = 0
    while True:
        if (datetime.now() - start_time).total_seconds() > timeout_seconds:
            # Превышение времени ожидания
            return ApplicationResponse(
                application_id=identifier,
                status=ApplicationStatusResponse.Failure,
                description="Operation timed out",
                last_request_time=datetime.now(),
                retriesCount=retries
            )

        # Параллельный запуск запросов к обоим сервисам
        status1, status2 = await asyncio.gather(
            get_application_status1(identifier),
            get_application_status2(identifier)
        )

        # Обработка ответов
        if status1 == Response.Success and status2 == Response.Success:
            return ApplicationResponse(
                application_id=identifier,
                status=ApplicationStatusResponse.Success,
                description="Application processed successfully",
                last_request_time=datetime.now(),
                retriesCount=retries
            )
        elif status1 == Response.RetryAfter or status2 == Response.RetryAfter:
            retries += 1
            await asyncio.sleep(2)  # Ожидание перед повторной попыткой
        else:
            # Если один из запросов завершился неудачей
            return ApplicationResponse(
                application_id=identifier,
                status=ApplicationStatusResponse.Failure,
                description="Application processing failed",
                last_request_time=datetime.now(),
                retriesCount=retries
            )

# Использование
async def main():
    result = await perform_operation("12345")
    print(result)

# Запуск
asyncio.run(main())
