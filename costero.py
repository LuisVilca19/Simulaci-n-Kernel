import random
import pygame
import numpy as np
import threading
from PIL import Image

from kernels import SOL, NUBE, BARCO, AVE_E1, BUQUE, HUMO1, HUMO2

lock = threading.Lock()

#---- DIMENSIONES ----
filas, columnas = 160, 300
tam_celda = 2

#---- MATRIS FONDO ----
fondo_imagen = Image.open("Algoritmos Paralelos/ProcesamientoImg/fondo2.avif").resize((columnas, filas))
FONDO_RGB = np.array(fondo_imagen)
print(FONDO_RGB)

#--- POSICIÓN PARA EL SOL---
POSX_SOL, POSY_SOL, PASOX_SOL = columnas-50, 7, 0

#--- POSICIÓN PARA LA NUVE --- 
POSX_NUBE, POSY_NUBE, PASOX_NUBE = 6, 12, 0

#--- POSICIÓN PARA EL BARCO --- 
POSX_BARCO, POSY_BARCO, PASOX_BARCO = 3, 72, 0

#--- POSICIÓN PARA EL BUQUE ---
POSX_BUQUE, POSY_BUQUE, PASOSX_BUQUE = columnas-30, 70, 0

#--- POSICIÓN PARA EL AVE ---
POSX_AVE, POSY_AVE, PASOSX_AVE = 190, 10, 0


#---- VENTANA ----
pygame.init()
ventana = pygame.display.set_mode((columnas * tam_celda, filas * tam_celda))
pygame.display.set_caption("Vista...")

#---- PALETA ----
COLORES = [(110,187,131), (227,143,83), (228,32,34), (215,233,134)]
COLORES2 = [(45,185,246), (0,98,211), (255,166,91)]

def dibujarMitadSol(nombre: str):
    if nombre == "left":
        for i in range(15):
            for j in range(len(SOL[0])):
                if SOL[i][j] == 1:
                    pygame.draw.rect(
                        ventana,
                        COLORES[3],
                        ((j+POSX_SOL+1+PASOX_SOL) * tam_celda, (i+POSY_SOL) * tam_celda, tam_celda, tam_celda)
                    )
    if nombre == "right":
        for i in range(15):
            for j in range(len(SOL[0])-1, -1, -1):
                if SOL[i][j] == 1:
                    pygame.draw.rect(
                        ventana,
                        COLORES[3],
                        ((len(SOL[0]*2)-j+POSX_SOL+PASOX_SOL) * tam_celda, (i+POSY_SOL) * tam_celda, tam_celda, tam_celda)
                    )

def dibujarSol():
        hiloSol1 = threading.Thread(target=dibujarMitadSol, args=("left",))
        hiloSol2 = threading.Thread(target=dibujarMitadSol, args=("right",))
        hiloSol1.start()
        hiloSol2.start()
        hiloSol1.join()
        hiloSol2.join()

def dibujarFranja(nombre: str, idx_inicio, idx_fin):
        #global columnas
        if nombre == "Cielo":
            for i in range(idx_inicio, idx_fin):
                for j in range(columnas):
                    pygame.draw.rect(
                        ventana,
                        FONDO_RGB[i][j],
                        (j * tam_celda, i * tam_celda, tam_celda, tam_celda)
                    )
                
        elif nombre == "Mar":
            for i in range(idx_inicio, idx_fin):
                for j in range(columnas):
                    pygame.draw.rect(
                        ventana,
                        FONDO_RGB[i][j],
                        (j * tam_celda, i * tam_celda, tam_celda, tam_celda)
                    )
        elif nombre == "Arena":
            for i in range(idx_inicio, idx_fin):
                for j in range(columnas):
                    pygame.draw.rect(
                        ventana,
                        FONDO_RGB[i][j],
                        (j * tam_celda, i * tam_celda, tam_celda, tam_celda)
                    )

def dibujarFondo():
    hilo1 = threading.Thread(target=dibujarFranja, args=("Cielo", 0, 50))
    hilo2 = threading.Thread(target=dibujarFranja, args=("Mar", 50, 90))
    hilo3 = threading.Thread(target=dibujarFranja, args=("Arena", 90, filas))
    hilo1.start()
    hilo2.start()
    hilo3.start()
    hilo1.join()
    hilo2.join()
    hilo3.join()


def dibujarNube():
    for i in range(6):
        for j in range(len(NUBE[0])):
            if NUBE[i][j]!='Z':
                pygame.draw.rect(
                    ventana,
                    NUBE[i][j],
                    ((j+POSX_NUBE+PASOX_NUBE) * tam_celda, (i+POSY_NUBE) * tam_celda, tam_celda, tam_celda)
                )

def colorBarco(number):
    color = (255,255,255)
    if number == 1:
        color = (255,128,35)
    
    if number == 2:
        color = (255,255,255)

    if number == 3:
        color = (185,228,255)

    if number == 4:
        color = (218,241,252)
    
    if number == 5:
        color = (255,170,96)
    
    if number ==7:
        color = (181,228,255)
    
    return color

def dibujarBarco():
    for i in range(26):
        for j in range(len(BARCO[0])):
            if BARCO[i][j] !=0 :
                color_usar = colorBarco(BARCO[i][j])
                pygame.draw.rect(
                    ventana,
                    color_usar,
                    ((j+POSX_BARCO+PASOX_BARCO) * tam_celda, (i+POSY_BARCO) * tam_celda, tam_celda, tam_celda)
                )
    
def dibujarAves():
    for i in range(3):
        for j in range(len(AVE_E1[0])):
            if AVE_E1[i][j] !=0 :
                pygame.draw.rect(
                    ventana,
                    (0,0,0),
                    ((j+POSX_AVE-PASOSX_AVE) * tam_celda, (i+POSY_AVE) * tam_celda, tam_celda, tam_celda)
                )

def colorBuque(color_buque: int):
    if color_buque == 1:
        color = (0,0,0)
    elif color_buque == 2:
        color = (191,27,44)
    elif color_buque == 3:
        color = (255,255,255)
    elif color_buque == 4:
        color = (0,0,0)
    elif color_buque == 5:
        color = (227,227,227)
    elif color_buque == 6:
        color = (170,170,170)
    elif color_buque == 7:
        color = (224,224,224)
    
    return color
    
def dibujarBuque(estado: int):
    if(estado == 0):
        for i in range(4):
            for j in range(len(HUMO2[0])):
                if HUMO2[i][j]!=0:
                    pygame.draw.rect(
                        ventana,
                        colorBuque(HUMO2[i][j]),
                        ((j+POSX_BUQUE-PASOSX_BUQUE) * tam_celda, (i+POSY_BUQUE-4) * tam_celda, tam_celda, tam_celda)
                    )
    else:
        for i in range(4):
            for j in range(len(HUMO1[0])):
                if HUMO1[i][j]!=0:
                    pygame.draw.rect(
                        ventana,
                        colorBuque(HUMO1[i][j]),
                        ((j+POSX_BUQUE-PASOSX_BUQUE) * tam_celda, (i+POSY_BUQUE-4) * tam_celda, tam_celda, tam_celda)
                    )

    
    for i in range(13):
        for j in range(len(BUQUE[0])):
            if BUQUE[i][j] !=0 :
                pygame.draw.rect(
                    ventana,
                    colorBuque(BUQUE[i][j]),
                    ((j+POSX_BUQUE-PASOSX_BUQUE) * tam_celda, (i+POSY_BUQUE) * tam_celda, tam_celda, tam_celda)
                )

def dibujarEfectoMar():
    cantidadEfectos = 30
    for ef in range(cantidadEfectos):
        alto = 2
        ancho = random.randint(5, 20)
        posx = random.randint(0, 380)
        posy = random.randint(50, 85)
        entrada = True
        for i in range(alto):
            if  random.randint(0, 1) == 0 and entrada:
                color = (15, 135, 220)
                entrada = False
            else:
                color = ((69,193,235))
                entrada = True
            for j in range(ancho):
                pygame.draw.rect(
                    ventana,
                    color,
                    ((posx+j) * tam_celda, (posy+i) * tam_celda, tam_celda, tam_celda)
                )



#----Bucle principal----
reloj = pygame.time.Clock()
corriendo = True
contador = 0
inicio = True


while corriendo:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            corriendo = False

    #--- Relojes ---
    contador += 1

    if contador >= 3 or inicio:
        dibujarFondo()
        dibujarSol()
        dibujarBuque(random.randint(0,4))
        PASOSX_BUQUE+=2
        dibujarBarco()
        dibujarNube()
        PASOX_SOL-=1
        PASOX_BARCO+=3
        PASOX_NUBE+=2
        pygame.display.flip()
        contador = 0
        inicio = False

    reloj.tick(60)

pygame.quit()