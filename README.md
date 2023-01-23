# Menu application
 Homework for Ylab course.

Запуск:
<ul>
 <li>В файле database.py указываем данные для подключения к базе данных на локальном компьютере по следующей схеме (для PostgreSQL):<br>
  <b>SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserverhost:port/dbname"</b>,<br>
  где user, password - данные для подключения к базе данных, postgresserverhost:port - имя и порт сервера базы данных, dbname - название базы данных.</li>
 <li>В командной строке переходим в папку проекта, выполняем установку необходимых пакетов командой:<br>
  <b>$ pip install -r requirements.txt</b></li>
 <li>Запускаем проект из командной строки:<br>
  <b>$ python main.py</b><br>Запуск сервера выполняется с помощью Uvicorn и по умолчанию доступен на localhost "127.0.0.1:8000".</li>
