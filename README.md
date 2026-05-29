<p align="center">
  <img src="https://raw.githubusercontent.com/Vdograd/HiveLauncher/main/launcher/data/static/global/HLlogo.svg" alt="HiveLauncher Logo" width="120" height="120">
</p>

<h1 align="center">HiveLauncher</h1>

<p align="center">
  <b>Современный Minecraft лаунчер без рекламы и лишнего</b>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/version-3.3.1-blue?style=for-the-badge" alt="Version">
  <img src="https://img.shields.io/badge/python-3.10+-yellow?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/PyQt6-6.10-green?style=for-the-badge&logo=qt&logoColor=white" alt="PyQt6">
  <img src="https://img.shields.io/badge/platform-Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white" alt="Platform">
</p>

<p align="center">
  <img src="https://img.shields.io/github/license/Vdograd/HiveLauncher?style=flat-square" alt="License">
</p>

---

## ✨ Особенности

<table>
  <tr>
    <td align="center" width="33%">
      <h3>🚀 Быстрый запуск</h3>
      <p>Автоматическая установка и запуск любой версии Minecraft в один клик</p>
    </td>
    <td align="center" width="33%">
      <h3>🚫 Без рекламы</h3>
      <p>Чистый интерфейс без баннеров, всплывающих окон и навязчивой рекламы</p>
    </td>
    <td align="center" width="33%">
      <h3>🎨 Темы оформления</h3>
      <p>Светлая и тёмная темы для комфортной работы в любое время суток</p>
    </td>
  </tr>
  <tr>
    <td align="center" width="33%">
      <h3>⚙️ Fabric & Forge</h3>
      <p>Встроенная поддержка модлоадеров Fabric и Forge для всех версий</p>
    </td>
    <td align="center" width="33%">
      <h3>👤 Система аккаунтов</h3>
      <p>Регистрация, авторизация и безопасное хранение данных в облаке</p>
    </td>
    <td align="center" width="33%">
      <h3>🎭 Скины и плащи</h3>
      <p>Загрузка собственных скинов и плащей с поддержкой HD и анимации</p>
    </td>
  </tr>
</table>

---

## 🛠️ Технологии

| Компонент | Технология |
|-----------|------------|
| **UI Framework** | PyQt6 6.10 |
| **Minecraft Core** | minecraft-launcher-lib 8.0 |
| **База данных** | Supabase |
| **Изображения** | Pillow 12.0 |
| **HTTP клиент** | Requests 2.32 |
| **Системная информация** | psutil 7.1 |

---

## 📋 Основные возможности

### 🎮 Запуск игры
- Поддержка версий Minecraft: ≤ 1.21.x
- Автоматическая установка выбранной версии
- Настройка выделенной оперативной памяти
- Кастомное разрешение окна игры
- Отслеживание времени в игре

### 👥 Аккаунты
- Безопасная регистрация и авторизация
- Хранение данных в облаке (Supabase)
- Поддержка нескольких аккаунтов

### 🎨 Персонализация
- Загрузка скинов (64x64 / 1024x1024 PNG)
- Загрузка плащей (64x32 / 1024x512 PNG/GIF)
- Переключение между Classic и Slim моделями
- Предпросмотр головы персонажа в лаунчере

### ⚙️ Модлоадеры
- **Fabric** — автоматическая установка с Fabric API
- **Forge** — поддержка всех версий
- Автоматическая установка совместимых модов HLSkins

---

## 🚀 Установка

### Требования
- Windows 10/11
- Python 3.10+ (для запуска из исходников)
- Java (для запуска Minecraft)

### Из релиза (рекомендуется)
1. Скачайте последний релиз со страницы [Releases](https://github.com/Vdograd/HiveLauncher/releases)
2. Распакуйте архив в удобную папку
3. Запустите `HiveLauncher.exe`

### Из исходного кода
1. Клонируйте репозиторий:
```bash
git clone https://github.com/Vdograd/HiveLauncher.git
cd HiveLauncher
```
2. Установите зависимости:
```bash
pip install -r requirements.txt
```
3. Поместите в папку проекта файл .env с секретными ключами
4. Запустите HiveLauncher:
```bash
python main.py
```
---

## 📁 Структура проекта

```
HiveLauncher/
├── main.py                    # Точка входа
├── requirements.txt           # Зависимости Python
└── launcher/
    ├── auth/                  # Система авторизации
    │   ├── auth_manager.py    # Управление аккаунтами
    │   ├── auth_verify.py     # Верификация
    │   └── encryption.py      # Шифрование паролей
    ├── core/                  # Ядро лаунчера
    │   ├── launcher_game.py   # Установка и запуск игры
    │   ├── version_manager.py # Управление версиями
    │   ├── report_email.py    # Отправка ошибки на почту
    │   ├── skin_cape_manager.py # Скины и плащи
    │   └── texture_manager.py # Обрезка скинов
    ├── ui/                    # Пользовательский интерфейс
    │   ├── pages/             # Страницы
    │   ├── page_functions/    # Логика страниц
    │   ├── dialogs/           # Диалоговые окна
    │   └── style.py           # Установить стили и темы
    ├── utils/                 # Утилиты
    │   ├── configurator.py    # Конфигурация
    │   ├── download_update_file.py # Скачать update-файл
    │   ├── error_manager.py   # Обработка ошибок
    │   ├── font_manager.py    # Менеджер шрифтов
    │   ├── getenv.py          # Управление SECRET_KEY
    │   ├── logger.py          # Логирование
    │   └── helper.py          # Вспомогательные функции
    └── data/
        ├── static/            # Статические ресурсы
        └── themes/            # CSS темы оформления
```

---

## ⚙️ Настройки

| Параметр | Описание |
|----------|----------|
| **Директория игры** | Путь к папке с файлами Minecraft |
| **Разрешение экрана** | Размер окна игры при запуске |
| **Выделенная память** | Количество RAM для Java |
| **После запуска** | Скрыть/закрыть лаунчер или ничего не делать |
| **После установки** | Запустить игру или ничего не делать |
| **Тема оформления** | Светлая или тёмная тема |

---

## 🔐 Безопасность

- 🔒 Пароли хранятся в зашифрованном виде
- ☁️ Данные синхронизируются через защищённое соединение с Supabase
- 🛡️ Уникальные верификационные коды для каждого устройства
- 📝 Локальное логирование для диагностики проблем

---

## 📝 Лицензия

Распространяется под лицензией MIT. Смотрите файл `LICENSE` для подробностей.

---

## 📞 Контакты

**Vdograd** - [GitHub](https://github.com/Vdograd)<br>
**@drombaz** - [Telegram](https://t.me/drombaz)<br>
**dimafandu** - [ВКонтакте](https://vk.com/dimafandu)

Ссылка на проект: [https://github.com/Vdograd/HiveLauncher](https://github.com/Vdograd/HiveLauncher)

---

<p align="center">
  <b>Сделано с ❤️ для игроков Minecraft</b>
</p>