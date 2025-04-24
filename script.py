import cv2
import mediapipe as mp
import serial
import time

ser = serial.Serial('COM5', 9600)  
time.sleep(2)

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils

# Inicializa a captura de vídeo
cap = cv2.VideoCapture(0)

# Variável para armazenar o último gesto enviado
ultimo_gesto = ""
gesto_atual = ""

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Desenha os marcos da mão
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Lógica para detectar os gestos
            thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
            index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            middle_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]

            # Calcula a distância entre os dedos (para detectar gestos)
            thumb_index_distance = ((thumb_tip.x - index_tip.x) ** 2 + (thumb_tip.y - index_tip.y) ** 2) ** 0.5
            thumb_middle_distance = ((thumb_tip.x - middle_tip.x) ** 2 + (thumb_tip.y - middle_tip.y) ** 2) ** 0.5

            # Lógica para gesto "joia" 
            if thumb_index_distance > 0.1 and thumb_middle_distance > 0.1:
                gesto_atual = "joia"
            

            # Verifica se o gesto foi alterado
            if gesto_atual != ultimo_gesto:
                if gesto_atual != "desconhecido":
                    ser.write(gesto_atual.encode())  # Envia o gesto para o Arduino
                else:
                    ser.write("Aguardando gesto...".encode())  # Envia mensagem de "Aguardando gesto..." quando não há gesto

                ultimo_gesto = gesto_atual  

    else:
        # Caso não detecte mais mãos (gesto desaparecendo)
        if ultimo_gesto != "desconhecido":
            ser.write("Aguardando gesto...".encode())  # Envia "Aguardando gesto..." para o LCD
            ultimo_gesto = "desconhecido"  # Atualiza o último gesto para "desconhecido"

    cv2.imshow("Mediapipe Hand Tracking", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
