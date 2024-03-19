import os
import subprocess
import requests
import logging
import traceback
import msgpack
from requests.auth import HTTPDigestAuth
from datetime import datetime, timedelta
# from .config import login, password, maxduration

login = 'kipia'  # логин для системы видеонаблюдения
password = '6450300'  # пароль для системы видеонаблюдения

header = {
    'Content-type': 'application/x-msgpack'}  # не трогать - способ кодирования запроса/ответа сервера видеонаблюдения
maxduration = 180  # максимальная длина видео


class MovieMaker:
    def __init__(self, camera: dict, filepath=None):
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(format="[%(asctime)s: %(filename)s:%(lineno)s  - %(funcName)20s() ] %(message)s",
                            level=logging.DEBUG, datefmt='%Y-%m-%d %H:%M:%S')
        self.camera = camera
        self.filepath = filepath
        self.link = None
        self.logger.info(f"Экземпляр MovieMaker создан, файлы расположены {self.filepath}*")

    def get_video(self, start_timeframe, finish_timeframe, file_name):
        # Формируем временные метки
        self.link = f"{file_name}.mp4"
        timeframe = self.timeframe_creation(start_timeframe, finish_timeframe)
        if not timeframe:
            return False

        self.logger.info(f"Время начала записи: {timeframe['start']}, время конца записи: {timeframe['finish']}. "
                         f"Камера {self.camera['cameraId']} {self.camera['cameraURL']}."
                         f" Длина {timeframe['duration']} сек")

        # Проверяем существует ли локальный каталог, если не существует, то создаем.
        if self.filepath:
            try:
                if not os.path.exists(self.filepath):
                    os.makedirs(self.filepath)
            except OSError as error:
                self.logger.error(f"Ошибка {str(error)} {traceback.format_exc()}")
                return False

        # имя файла видео без расширения. Например video1.mp4 -> video1
        self.logger.info(f"{self.link}")
        filename_wo_format = self.link.split('.')[0]

        self.logger.info(f"Качаем видео с сервера...")
        result = self.get_video_from_server(timeframe, self.camera, os.path.join(self.filepath,
                                                                                 f'{filename_wo_format}.h264'))

        if result > 0:
            self.logger.info(f"Конвертируем видео...")
            self.convert(os.path.join(self.filepath, f'{filename_wo_format}.h264'), os.path.join(self.filepath,
                                                                                                 self.link))
            self.logger.info(f"Видео готово...")
            return 1
        self.logger.info(f"В архиве нет видео с такими параметрами...")
        return 0

    def convert(self, input_file, output_file):
        self.logger.debug(f"Выполняем конвертацию исходного файла {input_file} в {output_file}")
        try:
            if os.name == 'nt':
                command = [r'C:\Program Files\ffmpeg\ffmpeg.exe',
                           '-i', input_file,
                           '-preset', 'ultrafast',
                           '-y', output_file]
            else:
                command = ['ffmpeg',
                           '-i', input_file,
                           '-preset', 'ultrafast',
                           '-y', output_file]

            subprocess.call(command,
                            stderr=subprocess.STDOUT)

            self.logger.info(f"Конвертация прошла успешно")
            os.remove(input_file)
            self.logger.info(f"Удалили h264")
        except subprocess.CalledProcessError as error:
            self.logger.error("Ошибка:\ncmd:{}\noutput:{}".format(error.cmd, error.output))
            self.logger.error(f"Ошибка {str(error)} {traceback.format_exc()}")
            raise
        self.logger.debug(f"Конвертация выполнена")

    def get_video_from_server(self, timeframe, camera, result_file_name):
        # Собираем запрос для получения списка id всех кадров с нужной камеры за указанный период времени:
        request_data = msgpack.packb({"method": "archive.get_frames_list",
                                      "params":
                                          {"channel": self.camera['cameraId'],
                                           # id этой камеры на сервере видеонаблюдения
                                           "stream": "video",
                                           # у всех камер из списка есть только один поток с видео - "video"
                                           "start_time": timeframe["start"],  # дата и время начала записи в формате
                                           "end_time": timeframe["finish"]  # дата и время начала записи
                                           },
                                      "version": 22
                                      })

        # Получаем список id всех кадров с нужной камеры за указанный период времени:
        try:
            frame_list = requests.post(url=self.camera["cameraURL"], auth=HTTPDigestAuth(login, password),
                                       data=request_data, headers={'Content-Type': 'application/x-msgpack'})
            frames = msgpack.unpackb(frame_list.content)  # Распаковываем ответ сервера с помощью msgpack
        except Exception as error:
            self.logger.error(f"Ошибка запроса. {error}")
            return False

        if frames.__contains__("result"):
            # создаем массив gop(групп кадров) для скачивания,
            # отбрасываем в начале списка все кадры до первого опорного - они не нужны:
            frames_id = []  # массив gop(групп кадров)
            key_frame = 0
            for frame in frames['result']['frames_list']:
                if (key_frame == 0) and (frame['gop_index'] != 0):  # не ключевой кадр в начале видео, отбрасываем
                    pass
                else:
                    if frame['gop_index'] == 0:
                        key_frame += 1
                        frames_id.append([])
                    frames_id[key_frame - 1].append(frame['id'])

            if len(frames_id) > 0:
                session = requests.Session()
                session.auth = HTTPDigestAuth(login, password)
                session.headers.update({'Content-Type': 'application/x-msgpack'})

                # создаем список запросов для упаковки в пакетный запрос
                request_args = [{"method": "archive.get_frame",
                                 "params": {"channel": camera['cameraId'], "stream": "video",
                                            "id": frame},
                                 "version": 22} for frame_keys in frames_id for frame in frame_keys]

                request_args = msgpack.packb(request_args)

                response = session.post(camera['cameraURL'], data=request_args)

                frames = msgpack.unpackb(response.content, raw=True)

                with open(result_file_name, 'wb') as result_file:
                    [result_file.write(frame[b'result'][b'frame'][b'data']) for frame in frames]

            self.logger.info(f"Если кейфреймы найдены, то они были скачаны")
            return len(frames_id)
        else:
            return 0

    def timeframe_creation(self, start_time, finish_time):
        if isinstance(start_time, datetime) and isinstance(finish_time, datetime):
            duration = int((finish_time - start_time).total_seconds())
            self.logger.info(f"Итоговая длина видео {duration} секунд")
            start_time = start_time + timedelta(seconds=self.camera["cameraTimeShift"] - 2)
            finish_time = finish_time + timedelta(seconds=self.camera["cameraTimeShift"] + 2)
            if duration <= maxduration:
                start = [start_time.year,
                         start_time.month,
                         start_time.day,
                         start_time.hour,
                         start_time.minute,
                         start_time.second]
                finish = [finish_time.year,
                          finish_time.month,
                          finish_time.day,
                          finish_time.hour,
                          finish_time.minute,
                          finish_time.second]
                return {"start": start, "finish": finish, "duration": duration}

            self.logger.error(f"Длина видео: {duration} сек. Это больше разрешенного {maxduration} сек")
            return False

        self.logger.error(f"Не корректный формат времени dt_start: {start_time} {type(start_time)} или "
                          f"dt_finish: {finish_time} {type(finish_time)}. {traceback.format_exc()}")
        return False
