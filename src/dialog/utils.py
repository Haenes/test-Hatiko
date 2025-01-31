from redis.asyncio import Redis


async def get_token(redis: Redis, user_id: int):
    token_in_cache = await redis.get(user_id)

    if token_in_cache:
        return token_in_cache


def isValidIMEI(imei: int):
    # Если длина не равна 15 - IMEI некорректно.
    if len(str(imei)) != 15:
        return False

    current_number = 0
    sum = 0

    for i in range(15, 0, -1):
        # Получить последнее число.
        current_number = (int(imei % 10))

        if i % 2 == 0:
            # Удвоить каждое второе число.
            current_number *= 2

        # Найти сумму чисел.
        sum += sum_digets(current_number)

        # Разделить IMEI на 10, чтобы current_number получило следующее слева число.
        imei /= 10
    return (sum % 10 == 0)


def sum_digets(number: int):
    """ Возвращает сумму чисел IMEI. """
    sum = 0

    while number > 0:
        sum += number % 10
        # Если число > 10 - разделить его на 10 и добавить остаток в сумму.
        number = int(number / 10)

    return sum
