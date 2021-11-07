# Spore REST API client
Spore REST API client


Simple example:
```py
import asyncio

from spore_api.client import SporeClient


async def main() -> None:
    async with SporeClient() as client:
        print(await client.get_creature(500267423060))


asyncio.run(main())
```

# TODO:
 * Общий абстрактный класс для клиентов + ассихронный клиент
 * Классы перевода из сырой информации в датаклассы, вместо `from_dict`, тк метод `from_dict` должен быть обратимый
