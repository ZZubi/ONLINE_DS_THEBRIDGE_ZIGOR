import math

def get_area_cuadrado(lado:float):
    return lado * lado

def get_area_triangulo(base:float, altura:float):
    return (base * altura) / 2

def get_area_circulo(radio:float):
    return math.pi * radio**2