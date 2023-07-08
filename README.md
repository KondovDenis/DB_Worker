# 1.Описание модулей

## 1.1 DBConnection.py
Реализует механизм доступа к БД. Необходимые параметры для подлючения получает из конфиг файла. .env

Список функций:

- init() - при создании Dbconnection принимает 1 параметр - наименование БД из 2 вариантов ('E2C', 'SVFE', 'BUSTER').
- connect() - создает подключение к БД. БД выбирается дял каждого обекта dbconnection отдельно.
- query(query) - выполняет запрос query к установлеенной БД.

## 1.2 EnumsType.py
Хранит в себе различные типизации Enum.

## 1.3 QueryParser.py
Парсит SQL запрос и изменяет условия оператора BETWEEN.

- init() - при создании QueryParser принимается 1 параметр - запрос в строчном формате.
- extract_data() - извлекает из SQL запроса диапазон дат.
- split_data_in_query_on_periods() - разбивает большой диапазон дат на более мелкие опционально(день, неделя)


## 1.4 Sheduler.py
Модуль для взаимодействия с командной строкой и ОС.

- get_all_query_sql() - считывание файла с  SQL запросом
- get_execution_mode() - считывание опций(флагов) передаваемых через командную строку


## 1.5 WorkerDB.py
Модуль генерирующий и отправляющий запросы в БД синхронными запросами.

- init() - при создании WorkerDB инициируется подключение к БД.
- query_generator() - финальная генерация запроса.
- sync_execute_sql() - отправка запроса и запись результата в *.csv файл



# 2. Описание опций
- --synchro - последовательность выполняемых запросов к БД. По умолчанию
- --week - недельная выгрузка за 1 запрос
- --day - дневная выгрузка за 1 запрос


# 3. Строгие правила
Принимает строго 2 формата даты в операторе BEWTWEEN:
- "YYYY-MM-DD HH24:MI:SS"
- "yyyy-mm-dd"

Старайтесь давать на вход легкие запросы без рекурсий и джойнов т.к библиотека cx_Oracle очень примитивна !!!!!

# 4. Запуск
Перед запуском нужно установить необходимые зависимости с помощью: "pip install -r requirements.txt" или "python -m pip install -r requirements.txt".
Добавить необходимые данные *.env и поместить в корень проекта для успешной авторизации в БД. 

Запуск осуществляется в корневой директории командой:  "python main.py"