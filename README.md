# Телеграм бот и бэкенд апи для формы обратной связи компании **МосГорТранс**
___
## Установка
Здесь и далее команды будут только для Linux, операционной системы, преимущественно используемую на серверах.
___
### Проверка наличия нужного програмного обеспечения
Перед установкой убедитесь в наличии **python** версии **3.10** и модуля **venv** у него на устройстве. Это можно сделать введя эту команду:
```
python3.10 --version &&
python3.10 -m venv --help
```
Если нужная версия и модуль уже присутствуют на устройстве, то вы увидите(вместо х может быть любое число):
```
Python 3.10.x
usage: venv [-h] [--system-site-packages] [--symlinks | --copies] [--clear]
            [--upgrade] [--without-pip] [--prompt PROMPT] [--upgrade-deps]
            ENV_DIR [ENV_DIR ...]

Creates virtual Python environments in one or more target directories.

positional arguments:
  ENV_DIR               A directory to create the environment in.

options:
  -h, --help            show this help message and exit
  --system-site-packages
                        Give the virtual environment access to the system
                        site-packages dir.
  --symlinks            Try to use symlinks rather than copies, when symlinks
                        are not the default for the platform.
  --copies              Try to use copies rather than symlinks, even when
                        symlinks are the default for the platform.
  --clear               Delete the contents of the environment directory if it
                        already exists, before environment creation.
  --upgrade             Upgrade the environment directory to use this version
                        of Python, assuming Python has been upgraded in-place.
  --without-pip         Skips installing or upgrading pip in the virtual
                        environment (pip is bootstrapped by default)
  --prompt PROMPT       Provides an alternative prompt prefix for this
                        environment.
  --upgrade-deps        Upgrade core dependencies: pip setuptools to the
                        latest version in PyPI

Once an environment has been created, you may wish to activate it, e.g. by
sourcing an activate script in its bin directory.
```
Если вы этого не увидели и/или вылезла ошибка, используйте эту команду для установки:
```
sudo apt update &&
sudo apt upgrade &&
sudo apt install python3.10 &&
sudo apt install python3.10-venv
```
___
### Непосредственная установка проекта
Чтобы установить проект введите приведёную ниже комманду:
```
git clone https://github.com/GaganovAlexander/mosgortrans-reviews-back-bot &&
cd ./mosgortrans-reviews-back-bot &&
mkdir ./run_scripts/pid &&
python3.10 -m venv venv &&
source ./venv/bin/activate &&
pip install -r requirements.txt
```
Если возникла ошибка, то вероятно, вы не прочли пункт "Проверка наличия нужного програмного обеспечения". В случае возникновения неописанных там проблем, обратитесь к системному администратору

Так же не забудьте настроить веб сервер для связи бэкенда со внешним миром. В случае с nginx, добавьте этот блок:
```nginx
location /api/mosgortrans {

    proxy_pass http://127.0.0.1:8000;

}
```
___
### Создание .env файла
В кореной папке проекта создайте файл **.env** со следующим содержанием:
```
BOT_TOKEN=XXX
DB_USER=XXX
DB_PASSWORD=XXX
DB_NAME=XXX
```
Вместо ХХХ здесь должны быть ваши данные.

### Для получения BOT_TOKEN
Напишите официальному ["отцу"](https://t.me/BotFather) всех ботов телеграма и следуйте его инструкциям
___
### Для получения остальных полей, потребуется настроить postgreSQL сервер на устройстве
Если он уже есть, просто создайте отдельного пользователя и базу данных для него(в целях безопасности, но можно и оставить пользователя root, если ничего не боитесь).

Для этого следуйте следующим инструкциям:

В терминале введите
```
sudo -u postgres psql
```
В открывшемся терминале psql введите(вместо фигурных скобок и всего что между ними вставьте придуманные вами значения):
```
CREATE USER {имя пользователя}
WITH LOGIN PASSWORD '{пароль}';
CREATE DATABASE {название бд};
GRANT ALL PRIVILEGES ON DATABASE
{название бд} TO {имя пользователя};
```
- имя пользователя - DB_USER
- пароль - DB_PASSWORD
- название бд - DB_NAME

Если всё прошло хорошо, введите
```
exit
```
___
### Если на устройстве нет postgresql
В терминале введите команду:
```
sudo apt update &&
sudo apt upgrade &&
sudo apt install postgresql &&
sudo systemctl eneble postgresql.service &&
sudo systemctl start postgresql.service
```
После этого posgreSQL сервер будет сам включаться при включении устройства
___
## Запуск
Находясь в директории проекта, введите данную команду:
```
source ./run_scripts/start_back &&
source ./run_scripts/start_bot
```
В случе успешного выполнения, вы увидите подобный вывод:
```
[2023-05-28 20:35:06 +0300] [907] [INFO] Starting gunicorn 20.1.0
[2023-05-28 20:35:06 +0300] [907] [INFO] Listening at: http://127.0.0.1:8000 (907)
[2023-05-28 20:35:06 +0300] [907] [INFO] Using worker: sync
[2023-05-28 20:35:06 +0300] [909] [INFO] Booting worker with pid: 909
Бот запущен
```
___
## Остановка
Находясь в директории проекта, введите данную команду:
```
source ./run_scripts/stop_bot &&
source ./run_scripts/stop_back
```
В случае успешного завершения вам либо ничего не напишется, либо вы увидите подобные сообщения:
```
[2023-05-28 20:51:41 +0300] [1191] [INFO] Worker exiting (pid: 1191)
[2023-05-28 20:51:41 +0300] [1190] [INFO] Shutting down: Master

[1]-  Done                    python run_bot.py  (wd: ~/mosgortrans)
(wd now: ~)
[2]+  Done                    gunicorn run_back:app  (wd: ~/mosgortrans)
(wd now: ~)
```
___
## Использование апи
### При заполнении формы на вашем фронтенде, нужно отослать запрос:
**POST** http(s)://{ваш.домен}/api/mosgortrans/reviews 

**BODY**(JSON): 
```
{
    "telegram_id": number,
    "route_number": string,

    // 1-5 "звёзд"
    "rating": number, 

    // здесь и далее, true = лайк, false = дизлайк, null = не было отмечено
    "clearness": boolean, 
    "smoothness": boolean,
    "conductors_work": boolean,
    "occupancy": boolean,

    // Айди инновации для поля innovation_id и его текст для отображения пользователю
    // можно получить по инструкции ниже
    "innovation_id": number,
    "innovation": boolean,
    "text_review": string
}
```
___
### Требования к полям:
- Обязательные поля: 
  - **telegram_id**
  - **route_number** 
  - **rating**
- Длина **route_number** <= 15

### Если какое-то из требований не было соблюдено, вы получите ответ:
Response("There not enough required fields", 400)
___
### В случае успеха, в ответ вы получите 
Response("OK", 200)
### или
Response("User already did review last 10m", 200), если пользователь уже оставлял отзыв за последнии 10м.
___
### Для проверки
Можно отправить запрос со своим айди телеграма(его можно узнать [тут](https://t.me/getmyid_bot)), не забудьте соблюсти требования по полям.

Если всё хорошо, то ваш бот напишет вам.
___
## Как получить innovation_id и текст инновации
### Отправьте запрос:
GET http(s)://{ваш.домен}/api/mosgortrans/innovation?route_number={*string*}
### Требования к полям:
- длина **route_number** <= 15

### В ответ вы получите:
Response({**id**: *number*, **name**: *string*}, 200)

Где
- **id** - это **innovation_id**
- **name** - это текст инновации

Если для выбранного маршрута никогда не вводились инновации, ответ будет:

Response(*null*, 200)
