import json
from collections import defaultdict

from openai import OpenAI

import src.bot.settings as bot_settings
from src.products import products


class ContentMaker:
    def __init__(self, products: list[dict], settings: dict):
        self.products = products
        self.settings = settings


class OpenAIWorker:
    products: list[dict] = products

    def __init__(self, model: str, history_file: str, api_key: str, organization: str, project: str):
        self.model = model
        self.history_file = history_file
        self.api_key = api_key
        self.organization = organization
        self.project = project

    def get_client(self):
        return OpenAI(
            api_key=self.api_key,
            organization=self.organization,
            project=self.project
        )

    def load_histories(self):
        try:
            with open(self.history_file, 'r', encoding='UTF-8') as file:
                content = file.read()
                return json.loads(content)
        except FileNotFoundError:
            return defaultdict(list)

    def save_histories(self, histories):
        with open(self.history_file, 'w', encoding='UTF-8') as file:
            file.write(json.dumps(histories, ensure_ascii=False, indent=4))

    def get_product_info(self, query: str, user: str):
        client = self.get_client()
        user_histories: dict = self.load_histories()

        # Получение истории сообщений пользователя
        messages = user_histories.get(user, [])

        # Если история пуста, добавляем системное сообщение
        if len(messages) == 0:
            messages.append(
                bot_settings.openai_contnet['start']
            )

        # Добавляем информацию о товарах в сообщения, если это первое сообщение
            # for product in self.products:
            #     product_info = (
            #         f"Name: {product['name']}\n"
            #         f"Price: {product['price']}\n"
            #         f"Category: {product['category']}\n"
            #         f"Description: {product['description']}\n"
            #         f"Weight: {product['weight']}\n"
            #         f"Composition: {product['composition']}\n"
            #     )
            #     messages.append({"role": "system", "content": product_info})

        messages.append({"role": "user", "content": query})

        # Делаем запрос к OpenAI API
        response = client.chat.completions.create(
            model=self.model,
            user=str(user),
            messages=messages
        )

        msg = response.choices[0].message.content

        # Добавляем ответ ассистента в историю сообщений
        messages.append({"role": "assistant", "content": msg})

        # Обновляем историю сообщений пользователя
        user_histories[str(user)] = messages

        # Сохранение истории сообщений в файл
        self.save_histories(user_histories)

        return msg
