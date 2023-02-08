# Menu application
 Homework for Ylab course.

# Запуск на локальном компьютере:
<ul>
 <li>В корневом каталоге проекта создаём файл с именем .env и помещаем в него следующие переменные окружения (см. example_env):<br>
  <b>SQLALCHEMY_DATABASE_URL=postgresql://user:password@postgresserverhost:port/dbname</b>,<br>
  где <b>user:password</b> - данные для подключения к базе данных, <b>postgresserverhost:port</b> - имя и порт сервера базы данных, <b>dbname</b> - название базы данных.<br>
  <b>REDIS_HOST=redis_host</b>,<br>
  где <b>redis_host</b> - имя хоста Redis<br>
  <b>REDIS_PORT=redis_port</b>,<br>
  где <b>redis_port</b> - номер порта Redis<br>
  <b>SPECIAL_PASSWORD=password</b>,<br>
  где <b>password</b> - пароль для создания тестового меню<br>
  <b>RABBIT_BROKER=rabbit_broker</b>,<br>
  где <b>rabbit_broker</b> - адрес брокера для Celery<br>
  <b>RABBIT_BACKEND=rabbit_backend</b>,<br>
  где <b>rabbit_backend</b> - адрес бекэнда для Celery<br>
 </li>
 <li>В командной строке переходим в папку проекта, выполняем установку необходимых пакетов командой:<br>
  <b>$ pip install -r requirements.txt</b></li>
 <li>Запускаем проект из командной строки:<br>
  <b>$ uvicorn menuapp.main:app</b><br>Проект по умолчанию доступен на localhost:8000/docs.
 </li>
</ul>

# Запуск в контейнере:
<ul>
 <li>Запускаем проект в контейнере командой:<br>
  <b>$ docker-compose -f docker-compose.yml up -d</b><br>
  После запуска API будет доступен на localhost:8000/docs,
  база данных - по схеме posrgres:postgres@localhost:9000/postgres.
 </li>
 <li>Запускаем тесты проекта в контейнере командой:<br>
  <b>$ docker-compose -f docker-compose-test.yml up</b>
 </li>
</ul>

# Порядок создания и печати тестового меню
<ul>
 <li>POST-запрос "Создать тестовое меню"<br></li>
 <li>POST-запрос "Запрос на генерацию эксель файла"<br></li>
 <li>GET-запрос "Скачать файл или получить статус"<br></li>
</ul>
