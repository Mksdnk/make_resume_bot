# Resume Generator Bot 

Телеграм-бот для создания профессиональных резюме. Пользователь отвечает на несколько вопросов, а бот генерирует готовый документ — сначала в виде Markdown для проверки, затем в PDF.

## Что умеет бот 

- Ведёт пользователя по шагам: ФИО → контакты → образование → опыт → навыки
- Генерирует текст резюме через DeepSeek V3
- Конвертирует результат в PDF с кастомными шрифтами SF Compact
- Даёт возможность просмотреть и отредактировать резюме перед финальной отправкой
- Сохраняет прогресс между сессиями — можно прервать и вернуться

## Стек 

- **Python 3.12** — основной язык
- **Aiogram** — Telegram-интеграция
- **DeepSeek-V3-0324** — генерация текста (через Azure Inference API)
- **Celery + Redis** — асинхронные задачи и кеш
- **FPDF2** — сборка PDF
- **Pydantic** — валидация конфигурации
- **Docker** — изоляция окружения

## Как это работает 

1. Пользователь запускает `/resume`
2. Бот последовательно спрашивает: ФИО, контакты, образование, опыт, навыки и дополнительную информацию
3. Ответы сохраняются в Redis
4. В фоне запускается задача Celery — DeepSeek собирает резюме
5. Пользователь видит результат в Markdown, может его отредактировать
6. После подтверждения бот отдаёт готовый PDF

## Детали реализации 

**Асинхронность.** Генерация не блокирует бота — Celery обрабатывает её в фоне. `task_id` сохраняется в Redis, чтобы потом подтянуть результат.

**FSM.** Состояние диалога хранится явно: каждый шаг — отдельное состояние, переходы предсказуемы. Это упрощает обработку ошибок и редактирование отдельных полей.

**PDF с кастомными шрифтами.** FPDF2 + SF Compact с поддержкой жирного и курсивного начертания. Разметка парсится из Markdown, поэтому форматирование в документе соответствует предпросмотру.

**Конфигурация.** Токены и ключи — только через `.env`. Pydantic проверяет переменные окружения при старте и падает с внятной ошибкой, если что-то не задано.

## Запуск ⚙️
```bash
git clone https://github.com/Mksdnk/make_resume_bot.git
```

Создайте `.env`:
```env
BOT_TOKEN=your_telegram_bot_token
GITHUB_TOKEN=your_github_api_token
```

Запустите:
```bash
docker-compose up --build
```

## Команды ⌨️

| Команда | Действие |
|---------|----------|
| `/start` | Запуск бота |
| `/resume` | Начать создание резюме |
| `/help` | Справка |
| `/cancel` | Отменить текущую генерацию |

## Скриншоты

> Тестовые данные в скриншотах сгенерированы нейросетью

![Скриншот 1](https://raw.githubusercontent.com/Mksdnk/make_resume_bot/main/screenshots/screenshot1.png)
![Скриншот 2](https://raw.githubusercontent.com/Mksdnk/make_resume_bot/main/screenshots/screenshot2.png)
![Скриншот 3](https://raw.githubusercontent.com/Mksdnk/make_resume_bot/main/screenshots/screenshot3.png)
![Скриншот 4](https://raw.githubusercontent.com/Mksdnk/make_resume_bot/main/screenshots/screenshot4.png)
![Скриншот 5](https://raw.githubusercontent.com/Mksdnk/make_resume_bot/main/screenshots/screenshot5.png)
![Скриншот 6](https://raw.githubusercontent.com/Mksdnk/make_resume_bot/main/screenshots/screenshot6.png)
![Скриншот 7](https://raw.githubusercontent.com/Mksdnk/make_resume_bot/main/screenshots/screenshot7.png)
