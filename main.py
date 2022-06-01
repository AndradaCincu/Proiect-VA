import numpy as np
import cv2
from collections import deque

#funcția trackbar numită implicit
def setValues(x):
   print("")

#Vom face Trackbars pentru a aranja valorile HSV în gama de culori necesară pentru obiectul colorat .
#cream trackbars pentru ajustarea culorilor
cv2.namedWindow("Color detectors", cv2.WINDOW_NORMAL)
cv2.createTrackbar("Upper Hue", "Color detectors", 153, 180,setValues)
cv2.createTrackbar("Upper Saturation", "Color detectors", 255, 255,setValues)
cv2.createTrackbar("Upper Value", "Color detectors", 255, 255,setValues)
cv2.createTrackbar("Lower Hue", "Color detectors", 64, 180,setValues)
cv2.createTrackbar("Lower Saturation", "Color detectors", 72, 255,setValues)
cv2.createTrackbar("Lower Value", "Color detectors", 49, 255,setValues)

#1
# Vom forma un deque python (o structură de date). Deque va stoca poziția conturului pe fiecare cadru succesiv
# și vom folosi aceste puncte stocate pentru a crea o linie folosind funcțiile de desen OpenCV.
#În primul rând, realizăm patru deque-uri, pentru patru culori distincte ale proiectului:

#Crearea de matrici diferite pentru a gestiona punctele de culoare de culori diferite
bpoints = [deque(maxlen=1024)]
ppoints = [deque(maxlen=1024)]
rpoints = [deque(maxlen=1024)]
ypoints = [deque(maxlen=1024)]

# Acești indici vor fi utilizați pentru a marca punctele din anumite matrice de culori specifice.
blue_index = 0
pink_index = 0
red_index = 0
yellow_index = 0

#The kernel to be used for dilation purpose
kernel = np.ones((5,5),np.uint8)

#Matrice de culori pentru modificarea culorilor de desen
colors = [(255, 0, 0), (255,0, 255), (0, 0, 255), (0, 255, 255)]
colorIndex = 0   #1

# Here is code for Canvas setup
paintWindow = np.zeros((471,636,3)) + 255
paintWindow = cv2.rectangle(paintWindow, (40,1), (140,65), (0,0,0), 2)
paintWindow = cv2.rectangle(paintWindow, (160,1), (255,65), colors[0], -1)
paintWindow = cv2.rectangle(paintWindow, (275,1), (370,65), colors[1], -1)
paintWindow = cv2.rectangle(paintWindow, (390,1), (485,65), colors[2], -1)
paintWindow = cv2.rectangle(paintWindow, (505,1), (600,65), colors[3], -1)

cv2.putText(paintWindow, "CLEAR", (49, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
cv2.putText(paintWindow, "BLUE", (185, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
cv2.putText(paintWindow, "PINK", (298, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
cv2.putText(paintWindow, "RED", (420, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
cv2.putText(paintWindow, "YELLOW", (520, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (150,150,150), 2, cv2.LINE_AA)
cv2.namedWindow('Paint', cv2.WINDOW_AUTOSIZE)

#2
#Imaginea primită de la camera web trebuie convertită în spațiul de culoare HSV pentru detectarea obiectului colorat.
# Fragmentul de cod de mai jos convertește imaginea primită în spațiul HSV, care este un spațiu de culoare
# potrivit pentru urmărirea culorilor.
# Accesam camera laptopului.
cap = cv2.VideoCapture(0)

while True:
    # Citim frame-ul din camera
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)  #2

  #3
    #Atunci când barele de urmărire sunt configurate, vom obține valoarea în timp real de la barele de urmărire și vom crea un interval.
    # Acest interval este o structură numpy care este utilizată pentru a fi transmisă în funcția cv2.inrange( ).
    # Această funcție returnează Masca pe obiectul colorat. Această mască este o imagine alb-negru cu pixeli albi în poziția culorii dorite.
    u_hue = cv2.getTrackbarPos("Upper Hue", "Color detectors")
    u_saturation = cv2.getTrackbarPos("Upper Saturation", "Color detectors")
    u_value = cv2.getTrackbarPos("Upper Value", "Color detectors")
    l_hue = cv2.getTrackbarPos("Lower Hue", "Color detectors")
    l_saturation = cv2.getTrackbarPos("Lower Saturation", "Color detectors")
    l_value = cv2.getTrackbarPos("Lower Value", "Color detectors")

    #Upper și lower sunt intervalele în care se poate găsi culoarea.
    Upper_hsv = np.array([u_hue,u_saturation,u_value])
    Lower_hsv = np.array([l_hue,l_saturation,l_value])


    # Adding the colour buttons to the live frame for colour access
    frame = cv2.rectangle(frame, (40,1), (140,65), (122,122,122), -1)
    frame = cv2.rectangle(frame, (160,1), (255,65), colors[0], -1)
    frame = cv2.rectangle(frame, (275,1), (370,65), colors[1], -1)
    frame = cv2.rectangle(frame, (390,1), (485,65), colors[2], -1)
    frame = cv2.rectangle(frame, (505,1), (600,65), colors[3], -1)
    cv2.putText(frame, "CLEAR ALL", (49, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(frame, "BLUE", (185, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(frame, "PINK", (298, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(frame, "RED", (420, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(frame, "YELLOW", (520, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (150,150,150), 2, cv2.LINE_AA)


    # Identificarea pointerului prin realizarea măștii acestuia
    Mask = cv2.inRange(hsv, Lower_hsv, Upper_hsv)                 #3
    #4
    #După detectarea măștii în Air Canvas, acum este momentul să localizăm poziția sa centrală pentru a desena linia.
    # În fragmentul de cod de mai jos, efectuăm câteva operații morfologice asupra măștii, pentru a o curăța de impurități
    # și pentru a detecta ușor conturul.
    Mask = cv2.erode(Mask, kernel, iterations=1)
    Mask = cv2.morphologyEx(Mask, cv2.MORPH_OPEN, kernel)
    Mask = cv2.dilate(Mask, kernel, iterations=1)

    # Găsește contururile pentru pointer după ce l-a identificat
    cnts,_ = cv2.findContours(Mask.copy(), cv2.RETR_EXTERNAL,
    	cv2.CHAIN_APPROX_SIMPLE)
    center = None

    # Dacă contururile sunt formate
    if len(cnts) > 0:
    	# sortarea contururilor pentru a găsi cele mai mari
        cnt = sorted(cnts, key = cv2.contourArea, reverse = True)[0]
        # Obține raza cercului care înconjoară conturul găsit
        ((x, y), radius) = cv2.minEnclosingCircle(cnt)
        # Desenați cercul în jurul conturului
        cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
        # Calcularea centrului conturului detectat
        M = cv2.moments(cnt)
        center = (int(M['m10'] / M['m00']), int(M['m01'] / M['m00']))  #4


       #5
        #Acum, vom folosi poziția conturului pentru a decide dacă dorim să facem clic pe un buton sau să desenăm pe foaie.
        # Am aranjat câteva butoane în partea de sus a Canvas-ului,
        # dacă indicatorul ajunge în zona lor, vom declanșa metoda lor. Avem patru butoane pe canvas, desenate cu ajutorul OpenCV.
        # Verificam dacă utilizatorul dorește să facă clic pe vreun buton de deasupra ecranului
        if center[1] <= 65:
            if 40 <= center[0] <= 140: # Butonul Clear
                bpoints = [deque(maxlen=512)]
                ppoints = [deque(maxlen=512)]
                rpoints = [deque(maxlen=512)]
                ypoints = [deque(maxlen=512)]

                blue_index = 0
                pink_index = 0
                red_index = 0
                yellow_index = 0

                paintWindow[67:,:,:] = 255
            elif 160 <= center[0] <= 255:
                    colorIndex = 0 # Blue
            elif 275 <= center[0] <= 370:
                    colorIndex = 1 # Pink
            elif 390 <= center[0] <= 485:
                    colorIndex = 2 # Red
            elif 505 <= center[0] <= 600:
                    colorIndex = 3 # Yellow
        else :
            if colorIndex == 0:
                bpoints[blue_index].appendleft(center)
            elif colorIndex == 1:
                ppoints[pink_index].appendleft(center)
            elif colorIndex == 2:
                rpoints[red_index].appendleft(center)
            elif colorIndex == 3:
                ypoints[yellow_index].appendleft(center)
    # Adăugăm următorul deques atunci când nu se detectează nimic pentru a evita încurcarea.
    else:
        bpoints.append(deque(maxlen=512))
        blue_index += 1
        ppoints.append(deque(maxlen=512))
        pink_index += 1
        rpoints.append(deque(maxlen=512))
        red_index += 1
        ypoints.append(deque(maxlen=512))
        yellow_index += 1   #5


   #Acum vom desena toate punctele pe pozițiile stocate în deques, cu culoarea respectivă.
    # Desenați linii de toate culorile pe pânză și cadru
    points = [bpoints, ppoints, rpoints, ypoints]
    for i in range(len(points)):
        for j in range(len(points[i])):
            for k in range(1, len(points[i][j])):
                if points[i][j][k - 1] is None or points[i][j][k] is None:
                    continue
                cv2.line(frame, points[i][j][k - 1], points[i][j][k], colors[i], 2)
                cv2.line(paintWindow, points[i][j][k - 1], points[i][j][k], colors[i], 2)

    # Afișarea tuturor ferestrelor
    cv2.imshow("Tracking", frame)
    cv2.imshow("Paint", paintWindow)
    cv2.imshow("mask",Mask)

	# Dacă este apăsată tasta "q", opriți aplicația.
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


# Se eliberează camera și toate resursele
cap.release()
cv2.destroyAllWindows()
