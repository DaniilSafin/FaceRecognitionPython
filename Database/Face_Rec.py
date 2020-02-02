import face_recognition  # Заранее обученная нейронная сеть c с точностью распознования 99.38%
import numpy as np  # Используется для быстрого вычисления декартого расстояния двух матриц
import os  # Получение списка файлов
import cv2  # Используется для работы с матрицами

all_face = []
# Получаем список лиц
for file in os.listdir("/Users/safindaniil/PycharmProjects/Visible/Face/"):
    if file.endswith(".jpg"):
        all_face.append(os.path.join("/Users/safindaniil/PycharmProjects/Visible/Face/", file)[48:])

# Загружаем базу лиц для распознования
face_image = []
known_face_encodings = []
known_face_names = []

for i in range(0, (len(all_face)) - 1, 1):
    face_image.append(face_recognition.load_image_file
                      ('/Users/safindaniil/PycharmProjects/Visible/Face/' + all_face[i]))
    known_face_encodings.append(face_recognition.face_encodings(face_image[i])[0])
    known_face_names.append(all_face[i][2:-4])
face_image.clear()
all_face.clear()

# Получение изображения с Webcam;
video_capture = cv2.VideoCapture(0)


def video():
    # Потоковое определение лиц
    # Инициализируем List, т.к в кадре может быть множество обьектов
    face_locations = []
    face_encodings = []
    output_names = []
    face_names = []
    # Берем каждый кадр видеопотока
    ret, frame = video_capture.read()
    # Уменьшаем кадр изображания до 1/4 изначального
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    # Конверитруем BGR в RGB, т.к кадр изначально в BGR
    rgb_frame = small_frame[:, :, ::-1]

    if True:
        # Ищем лица
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
        for face_encoding in face_encodings:
            # Проверяем соответсвие
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"
            # Декартово расстояние между обьектом сравнения и эталонным изображением
            best_match_index = np.argmin(face_recognition.face_distance(known_face_encodings, face_encoding))
            # Записываем присуствующих
            if matches[best_match_index]:
                name = known_face_names[best_match_index]
                for i in range(0, len(all_face)):
                    if name != all_face[i]:
                        if name not in output_names:
                            output_names.append(name)
            face_names.append(name)
    # Отображаем результат
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Уыеличиваем кадр обратно
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Рисуем вокруг лица
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 0), 2)

        # Рисуем label
        cv2.rectangle(frame, (left + 2, bottom - 35), (right - 2, bottom - 2), (255, 255, 255), cv2.FILLED)
        cv2.putText(frame, name, (left + 6, bottom - 6),
                    cv2.FONT_HERSHEY_DUPLEX, 0.9, (0, 0, 0), 1)

    frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    return frame, face_names
    # return frame
