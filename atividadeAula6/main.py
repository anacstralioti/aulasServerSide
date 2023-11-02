# imports
from flask import Flask

# instância do site em flask
app = Flask(__name__)

# responde como index e embaixo coloca uma função
@app.route("/")
def index():
    return "Index"

@app.route("/ex01")
def mensagem():
    return "Hello World"

@app.route("/ex02")
def get_number():
    numero = int(input("Informe um número: "))
    return ("O numero informado foi: {0}".format(numero))

@app.route("/ex03")
def soma():
    numero = int(input("Informe um número inteiro: "))
    numero2 = int(input("Informe mais um número inteiro: "))
    soma = numero + numero2
    return format(soma)

@app.route("/ex04")
def media():
    numero = float(input("Informe a primeira nota: "))
    numero2 = float(input("Informe a segunda nota: "))
    numero3 = float(input("Informe a terceira nota: "))
    numero4 = float(input("Informe a quarta nota: "))
    media = (numero + numero2 + numero3 + numero4) / 4
    return format(media)

@app.route("/ex05")
def conversao():
    numero = float(input("Informe o numero: "))
    conversao = numero * 100
    return ("O numero informado em centímetros é: {0}".format(conversao))

@app.route("/ex06")
def areacirculo():
    raio = float(input("Digite o raio do círculo: "))
    areacirculo = 3.14 * (raio ** 2)
    return ("Área do círculo é: {0}".format(areacirculo))

@app.route("/ex07")
def areaquadrado():
    lado = int(input("Digite um lado do quadrado: "))
    lado2 = int(input("Digite o outro lado do quadrado: "))
    areaquadrado = lado * lado2
    return ("A área do quadrado é: {0}".format(areaquadrado))

@app.route("/ex08")
def salario():
    valorHora = float(input("Digite o valor da hora: "))
    hora = float(input("Digite as horas trabalhadas: "))
    salario = valorHora * hora
    return ("O salário é: {0}".format(salario))

@app.route("/ex09")
def temperaturacelsius():
    fahrenheit = float(input("Digite a temperatura em fahrenheit: "))
    celsius = (5 * (fahrenheit-32)) / 9
    return ("A temperatura em Celsius é: {0}".format(celsius))

@app.route("/ex10")
def temperaturafahrenheit():
    celsius = float(input("Digite a temperatura em celsius: "))
    fahrenheit = (celsius * 9 / 5) + 32
    return ("A temperatura em Fahrenheit é: {0}".format(fahrenheit))

# função principal
if __name__ == '__main__':
    #app.run(debug=True, port="3000")
    app.run(debug=True)


