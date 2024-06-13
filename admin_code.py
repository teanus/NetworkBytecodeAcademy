import hashlib
import os


def generate_random_code() -> str:
    """
    Генерирует случайный код длиной 16 символов.

    Функция использует криптографически стойкий генератор случайных чисел для
    генерации 16 байтов случайных данных. Затем эти данные хэшируются с
    использованием SHA-256, и первые 16 символов хэш-строки возвращаются как случайный код.

    Returns:
        str: Случайный код длиной 16 символов.
    """
    random_number = os.urandom(16)
    random_hash = hashlib.sha256(random_number).hexdigest()
    return random_hash[:16]


ADMIN_CODE = "a9c4de71215ae469"
