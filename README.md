# 📧 Temporary Email Service

<div align="center">

![Temporary Email Logo](https://img.shields.io/badge/📧-Temporary%20Email-blue?style=for-the-badge)

**Создавайте одноразовые email адреса для регистрации на сайтах, тестирования и защиты вашей конфиденциальности**

[![React](https://img.shields.io/badge/React-18.2.0-61DAFB?style=flat-square&logo=react)](https://reactjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-009688?style=flat-square&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=flat-square&logo=python)](https://python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg?style=flat-square)](LICENSE)

[🌐 Live Demo](https://temp-email-demo.com) | [📖 Documentation](#api-documentation) | [🐛 Report Bug](../../issues) | [💡 Request Feature](../../issues)

</div>

## ✨ Особенности

- 🚀 **Мгновенное создание** - email адрес готов за секунды
- 📨 **Реальные письма** - получайте настоящие email сообщения
- 🔄 **Автообновление** - письма появляются в реальном времени
- 📋 **Копирование одним кликом** - легко используйте созданный адрес
- 🎨 **Современный UI** - красивый интерфейс с анимациями
- 📱 **Адаптивный дизайн** - работает на всех устройствах
- 🔒 **Полная приватность** - не требует регистрации и личных данных
- 🆓 **Полностью бесплатно** - без ограничений и платежей

## 🎯 Зачем использовать?

✅ Регистрация на сайтах без спама в основном email  
✅ Тестирование email функциональности в приложениях  
✅ Получение одноразовых кодов подтверждения  
✅ Защита личного email адреса от утечек  
✅ Временная переписка без раскрытия личности  

## 🛠️ Технологии

### Frontend
- **React 18** - UI библиотека
- **Tailwind CSS** - Стилизация
- **JavaScript ES6+** - Современный синтаксис

### Backend  
- **FastAPI** - Современный Python веб-фреймворк
- **Mail.tm API** - Бесплатный сервис временных email
- **aiohttp** - Асинхронные HTTP запросы
- **Pydantic** - Валидация данных

### DevOps
- **Docker** - Контейнеризация
- **Supervisor** - Управление процессами

## 🚀 Быстрый старт

### Предварительные требования

- Python 3.11+
- Node.js 18+
- Git

### Установка

1. **Клонируйте репозиторий**
```bash
git clone https://github.com/switchgearuser/TempMail/
cd temporary-email-service
```

2. **Установите зависимости backend**
```bash
cd backend
pip install -r requirements.txt
```

3. **Установите зависимости frontend**
```bash
cd ../frontend
npm install
# или
yarn install
```

4. **Настройте environment переменные**
```bash
# Backend (.env)
cp backend/.env.example backend/.env

# Frontend (.env)
cp frontend/.env.example frontend/.env
```

5. **Запустите приложение**

**Development mode:**
```bash
# Backend (Terminal 1)
cd backend
uvicorn server:app --reload --host 0.0.0.0 --port 8001

# Frontend (Terminal 2)  
cd frontend
npm start
```

**Production mode:**
```bash
docker-compose up -d
```

Откройте [http://localhost:3000](http://localhost:3000) в браузере.

## 📖 Использование

### Создание временного email

1. Откройте главную страницу
2. (Опционально) Введите желаемое имя пользователя
3. Нажмите **"✨ Создать Email"**
4. Скопируйте созданный email адрес
5. Используйте его для регистраций или получения писем

### Просмотр писем

- Письма автоматически появляются в списке
- Включите **автообновление** для получения писем в реальном времени
- Кликните на письмо для детального просмотра
- Поддерживается как текстовый, так и HTML контент

### Управление inbox

- **Обновить** - получить новые письма вручную
- **Копировать** - скопировать email адрес в буфер обмена
- **Закрыть** - создать новый временный email

## 🔌 API Documentation

### Создание временного email

```http
POST /api/inbox/create
Content-Type: application/json

{
  "custom_name": "myname"  // опционально
}
```

**Ответ:**
```json
{
  "inbox": {
    "id": "inbox_id",
    "email": "myname1234567890@somoj.com",
    "domain": "somoj.com", 
    "password": "password12345",
    "created_at": "2025-01-04T16:44:22.123456",
    "token": "jwt_token_here"
  },
  "messages": [],
  "message_count": 0
}
```

### Получение писем

```http
GET /api/inbox/{inbox_id}/messages?token={jwt_token}
```

**Ответ:**
```json
[
  {
    "id": "message_id",
    "from_address": "sender@example.com",
    "to_address": "myname1234567890@somoj.com",
    "subject": "Тема письма",
    "body": "Текст письма",
    "html_body": "<p>HTML контент</p>",
    "received_at": "2025-01-04T16:45:00.123456",
    "attachments": []
  }
]
```

### Получение доступных доменов

```http
GET /api/domains
```

### Health Check

```http
GET /api/health
```

## 📁 Структура проекта

```
temporary-email-service/
├── 📁 backend/                 # FastAPI backend
│   ├── server.py              # Главный файл приложения
│   ├── requirements.txt       # Python зависимости
│   └── .env                   # Environment переменные
├── 📁 frontend/               # React frontend
│   ├── 📁 public/            # Статические файлы
│   ├── 📁 src/               # Исходный код
│   │   ├── App.js            # Главный компонент
│   │   ├── App.css           # Стили
│   │   └── index.js          # Точка входа
│   ├── package.json          # Node.js зависимости
│   ├── tailwind.config.js    # Конфигурация Tailwind
│   └── .env                  # Environment переменные
├── 📁 tests/                 # Тесты
├── backend_test.py          # Backend тесты
├── test_result.md           # Результаты тестов
└── README.md               # Этот файл
```

## 🧪 Тестирование

### Запуск тестов

```bash
# Backend тесты
python backend_test.py

# Frontend тесты  
cd frontend
npm test
```

### Результаты тестов

✅ **Backend API (100% успешно):**
- Health Check endpoint
- Получение доступных доменов
- Создание inbox без параметров
- Создание inbox с кастомным именем
- Получение сообщений из inbox
- Реальная интеграция с Mail.tm API

## 🔧 Конфигурация

### Backend Environment Variables

```bash
# backend/.env
CORS_ORIGINS=http://localhost:3000
API_VERSION=1.0.0
DEBUG=true
```

### Frontend Environment Variables

```bash
# frontend/.env
REACT_APP_BACKEND_URL=http://localhost:8001
REACT_APP_API_VERSION=1.0.0
REACT_APP_TITLE=Temporary Email Service
```

## 🐛 Troubleshooting

### Частые проблемы

**Проблема**: Email не создается
```bash
# Проверьте логи backend
tail -f /var/log/supervisor/backend*.log

# Проверьте доступность Mail.tm API
curl https://api.mail.tm/domains
```

**Проблема**: Письма не приходят
- Убедитесь что используете правильный inbox_id и token
- Проверьте лимиты Mail.tm API
- Письма могут приходить с задержкой до 30 секунд

**Проблема**: Frontend не подключается к Backend
- Проверьте REACT_APP_BACKEND_URL в .env
- Убедитесь что Backend запущен на порту 8001
- Проверьте CORS настройки

## 📊 Производительность

- ⚡ **Время создания email**: < 2 секунды
- 📨 **Время получения письма**: 1-30 секунд (зависит от отправителя)
- 🔄 **Автообновление**: каждые 5 секунд
- 💾 **Размер приложения**: ~2MB (frontend), ~50MB (backend)

## 🔒 Безопасность

- 🚫 **Нет хранения паролей** - все генерируется временно
- 🔐 **JWT токены** - безопасная авторизация
- 🌐 **HTTPS поддержка** - шифрованная передача данных
- 🕒 **Автоудаление** - временные данные удаляются автоматически

## 🤝 Contributing

Мы приветствуем вклад в проект! Пожалуйста, следуйте следующим шагам:

1. Fork проект
2. Создайте feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit изменения (`git commit -m 'Add some AmazingFeature'`)
4. Push в branch (`git push origin feature/AmazingFeature`)
5. Создайте Pull Request

### Правила разработки

- Используйте осмысленные commit сообщения
- Добавляйте тесты для новой функциональности
- Обновляйте документацию при необходимости
- Следуйте существующему стилю кодирования

## 📈 Roadmap

- [ ] 🌍 **Мультиязычность** - поддержка английского языка
- [ ] 📧 **Отправка писем** - возможность отвечать на письма  
- [ ] 🔔 **Push уведомления** - мгновенные уведомления о новых письмах
- [ ] 📱 **Мобильное приложение** - React Native версия
- [ ] 🎨 **Темы оформления** - светлая/темная тема
- [ ] 💾 **Экспорт писем** - сохранение писем в файл
- [ ] 🔍 **Поиск по письмам** - поиск по содержимому

## 📝 Changelog

### v1.0.0 (2025-01-04)
- ✨ Начальный релиз
- 🎨 React frontend с Tailwind CSS
- ⚡ FastAPI backend
- 📧 Интеграция с Mail.tm API
- 🔄 Автообновление писем
- 📋 Копирование в буфер обмена
- 📱 Адаптивный дизайн

## 📄 License

Этот проект лицензирован под MIT License.

## 🙏 Acknowledgments

- [Mail.tm](https://mail.tm) - За предоставление бесплатного API
- [FastAPI](https://fastapi.tiangolo.com/) - За отличный Python фреймворк
- [React](https://reactjs.org/) - За мощную UI библиотеку
- [Tailwind CSS](https://tailwindcss.com/) - За удобную стилизацию

## 📞 Support

Если у вас есть вопросы или проблемы:

- 🐛 [Создайте Issue](../../issues/new)
- 💬 [Обсуждения](../../discussions)  

---

<div align="center">

**⭐ Поставьте звезду если проект был полезен! ⭐**

Made with ❤️ for privacy and convenience

</div>
