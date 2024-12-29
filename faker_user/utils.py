from random import choice
import aiofiles as aiof
import string


# Код для генерації паролю був взятий у старому об'єкту по генерації паролів
alphabet = list(string.ascii_letters)
number = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]
number_alphabet = [x for x in alphabet] + [x for x in number]
special_characters = list(string.punctuation)
Hard_dificult = number_alphabet + special_characters


def generate(selected_complexity: int, len_password: int):
    password = []
    
    if selected_complexity == 1 and len_password > 0:
        for char_pass in range(0, len_password):
            pass_char = choice(number)
            password.append(str(pass_char))
    elif selected_complexity == 2 and len_password > 0:
        for char_pass in range(0, len_password):
            pass_char = choice(number_alphabet)
            password.append(str(pass_char))
    elif selected_complexity == 3 and len_password > 0:
        for char_pass in range(0, len_password):
            pass_char = choice(Hard_dificult)
            password.append(str(pass_char))
    password_user = ''.join(password)
    return password_user


# Генерація адрес зі зміною домену і піддомену
async def rename(adress, SLD, TLD): # Приймає адресу, домен і піддомен
    current_name = adress.split('@')[0] # Отримуємо адресу
    # присвоюємо нові значення домеу і піддомену
    new_SLD = f'@{SLD}' 
    new_TLD = f'.{TLD}'
    # Об'єднуємо їх в пустий рядок
    return ''.join([current_name, new_SLD, new_TLD])


async def download_file(data: dict):
    async with aiof.open('data.txt', 'w', encoding='utf-8') as file:
        for key, value in data.items():
            await file.write(f'{key}: {value}\n')
        await file.flush()
    return file.name
