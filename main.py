from fastapi import FastAPI, Request
from db.base_models.base import get_session
from db.bd_handlers import service

from movie_maker.moviemaker import MovieMaker

from datetime import datetime, timedelta, time
from random import randint

app = FastAPI()


@app.post("/alarm/")
async def alarm_send(request: Request):
    request_data = request.json
    alarm_time = datetime.now()
    try:
        place_id = request_data["place"]
        with get_session() as session:
            data = service.get_place(session, place_id) # получаем необходимые данные из таблицы
            place = data[0]  # Получение места аварии
            camera = eval(data[1])  # Получение настроек камеры
    except ImportError:
        place = (
            f'place = {request_data["place"]} типа {type(request_data["place"])} - не найден, '
            f"необходимо добавить в БД или изменить в PLC"
        )
        camera = None
    try:
        with get_session() as session:
            alarm_id = int(request_data["alarm_text"])
            data = service.get_alarm(session, alarm_id)
            alarm_text = data[0]  # Получение места аварии
            need_movie = bool(data[1])
    except ImportError:
        alarm_text = (
            f"Некорректный номер ошибки (Обратитесь к программистам)"
            f'запись типа: {type(request_data["alarm_text"])} значение: {request_data["alarm_text"]}'
        )
    # cборка сообщения
    message = (
        f"Место аварии:  {place}\n"
        f"Авария:  {alarm_text}\n"
        f"Точное время: {alarm_time}\n"
    )

    if "m" in request_data:
        message = f"{message} \n" f'Сообщение для сервиса: {request_data["m"]}'
    if "er" in request_data:
        message = f"{message} \n" f'Статус драйвера hex: {hex(int(request_data["er"]))}'
        message = f"{message} \n" f'Статус драйвера int: {(request_data["er"])}'
    if need_movie and camera:
        # Задержка
        time.sleep(10)

        # Создание имени файла
        fime_name = f"m{randint(0, 999999999)}"

        # Вытаскиваем видео аварии
        dt = datetime.now()
        dt_start = dt - timedelta(seconds=30)
        dt_finish = dt

        # Вызываем класс
        mm = MovieMaker(camera, "media")

        # Формируем видео в .mp4
        mm.get_video(dt_start, dt_finish, fime_name)

        # Открытие файла видео
        video = open(f"/media/{fime_name}.mp4", "rb")


@app.post("/statistic/")
async def statistic(request: Request):
    request_data = request.json

    # Задаем начальное условие
    item_counter_robot = "данных нет"
    item_counter_machine = "данных нет"
    alarm_counter = "данных нет"

    try:
        with get_session() as session:
            place_id = request_data["place"]
            data = service.get_place(session, place_id)
            place = data[0]  # Получение места аварии
    except ImportError:
        place = (
            f'place = {request_data["place"]} типа {type(request_data["place"])} - не найден, '
            f"необходимо добавить в БД или изменить в PLC"
        )
    # cборка сообщения
