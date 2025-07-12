from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential
from bot.config_reader import config

class DeepseekService:
    def __init__(self):
        self.endpoint = "https://models.github.ai/inference"
        self.model = config.DEEPSEEK_MODEL
        self.github_key = config.GITHUB_TOKEN
        self.client = ChatCompletionsClient(endpoint=self.endpoint, credential=AzureKeyCredential(self.github_key.get_secret_value()))
        self.system_prompt = """"
       # Role: Профессиональный HR-ассистент  
        ## Задача  
        Создать структурированное резюме в формате Markdown **ТОЛЬКО** на основе предоставленных пользователем данных.  

        ## Правила  
        ### Обязательные:  
        1. **Строгая структура разделов**:  
        - Имя и контакты  
        - Желаемая должность  
        - Местоположение и гражданство  
        - Готовность к переезду/командировкам  
        - Опыт работы  
        - Образование  
        - Навыки (Soft Skills, Профессиональные)  
        - Дополнительная информация (водительские права, сертификаты и т.д.)  
        2. **Источники данных**:  
        - Использовать **ТОЛЬКО** предоставленные пользователем данные.  
        - Запрещено добавлять/придумывать информацию, даже если раздел кажется неполным.  
        3. **Стиль изложения**:  
        - Профессиональный, лаконичный, без шаблонных фраз.  
        - Допустимо креативное перефразирование для улучшения читаемости, **без искажения смысла**.  

        ### Форматирование:  
        - **Только ASCII**:  
        - Кавычки: прямые (")  
        - Апострофы: простые (')  
        - Тире: дефис (-) вместо длинного тире  
        - Запрещены любые Unicode-символы (например, •, →, é).  
        - **Markdown**:  
        - Заголовки: `##`, `###`  
        - Списки: дефисы с пробелом (`- item`)  
        - Экранировать спецсимволы: `*`, `_`, `#` → `\*`, `\_`, `\#`  
        - **Не использовать**: таблицы, жирный/курсив (кроме заголовков).  
        """

    
    def generate_resume(self, data: dict):
        response = self.client.complete(
            messages=[
                SystemMessage(self.system_prompt),
                UserMessage(self.generate_user_pompt(data))
            ],
            temperature=0.6,
            model=self.model,
            max_tokens=1500
    )
        return response.choices[0].message.content

    def generate_user_pompt(self, data: dict):
        return (
            "Создай профессиональное резюме\n"
            f"Кандидат: {data.get('full_name')}\n"
            f"Возраст: {data.get('age')}\n"
            f"Контанкты: {data.get('contacts')}\n"
            f"Место жительства: {data.get('place_of_residence')}\n"
            f"Гражданство: {data.get('citizenship')}\n"
            f"Готовность к переезду или коммандировкам: {data.get('removal')}\n"
            f"Претендуемая должность: {data.get('desired_position')}\n"
            f"Опыт работы: {data.get('experience')}\n"
            f"Образование: {data.get('education')}\n"
            f"Навыки: {data.get('skills')}\n"
            f"Опыт вождения: {data.get('driving_exp')}\n"
            f"Дополнительная информация: {data.get('additional')}"
        )
        #return self.system_prompt
        
    
deepseek_service = DeepseekService()
    
    

