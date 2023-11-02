# imports - importam as bibliotecas necessárias para o aplicativo Flask,
# manipulação de banco de dados, medição de tempo, trabalho com datas, JSON,
# geração de números aleatórios
from flask import Flask, request, render_template, jsonify, flash, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
import time
import timeit
from datetime import datetime
import json
import random
import string
import sys


app = Flask(__name__, template_folder="templates")
app.config ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///estudantes.db' # cria uma instância do aplicativo
# Flask e configura o aplicativo para usar um banco de dados SQLite chamado "estudantes.db"
# e define uma chave secreta para criptografar sessões.
app.config['SECRET_KEY'] = "random string"


# Lista para armazenar os valores do vetor
valores = []


@app.route("/shellsort", methods=['GET', 'POST']) # rota "/shellsort" que pode lidar com
# solicitações GET e POST. A função vetor será executada quando essa rota for acessada.
def vetor():
   elapsed_time_ms = 0
   if request.method == 'POST':
       valor = request.form['valor']
       valores.extend(map(int, valor.replace(" ", "").split(","))) # aqui a transformação
   # de string para JSON não é usada diretamente. mas aqui há manipulação de dados que envolve transformar
   # uma string em uma lista de valores inteiros


       # Registre o tempo de início
       start_time = time.time()
       # Chame a função shellSort para classificar a lista de valores
       elapsed_time_ms = shellSort(valores)
       # Registre o tempo de término
       end_time = time.time()

   return render_template("index.html", valores=valores, tempo_decorrido=elapsed_time_ms)
   # Se o método for GET, retorna uma resposta vazia ou redirecione para a página onde você insere os valores iniciais.
   return render_template("shellsort.html")


def shellSort(alist): #definição da função shellSort, que implementa o algoritmo
   # de ordenação Shell Sort para classificar uma lista de valores.
   start_time = time.time()
   sublistcount = len(alist) // 2 # o código define sublistcount como metade do
   # comprimento da lista alist. o algoritmo Shell Sort funciona dividindo a lista
   # em sublistas menores e, inicialmente, usa sublistcount para determinar o tamanho
   # dessas sub-listas.
   while sublistcount > 0:
       for startposition in range(sublistcount):
           gapInsertionSort(alist, startposition, sublistcount)


       print("After increments of size", sublistcount, "The list is", alist)


       sublistcount = sublistcount // 2 # resumindo: o algoritmo Shell Sort
       # começa classificando sublistas maiores e gradualmente diminui o tamanho
       # dessas sublistas até que a lista inteira esteja ordenada.


   end_time = time.time()
   elapsed_time_ms = (end_time - start_time) * 1000
   print("Tempo: {} ms".format(elapsed_time_ms))


   return elapsed_time_ms


def gapInsertionSort(alist, start, gap): # a função gapInsertionSort é uma
   # função auxiliar para o Shell Sort, que implementa a ordenação por
   # inserção com um intervalo específico.
   for i in range(start + gap, len(alist), gap): # loop for que processa elementos em
       # intervalos de tamanho gap, pulando alguns elementos entre as comparações e movimentações.
       # pq ele começa com o start + gap e percorre toda a lista
       currentvalue = alist[i]
       position = i # inicia a posição do elemento atual em i


       while position >= gap and alist[position - gap] > currentvalue: # position >= gap: Garante que está
           # dentro dos limites da sublista e alist[position - gap]: verifica se o elemento anterior na
           # sublista é maior do que currentvalue.


           alist[position] = alist[position - gap]
           position = position - gap


       alist[position] = currentvalue


# Esta linha cria uma instância da classe SQLAlchemy que será usada para interagir com o banco de dados.
db = SQLAlchemy(app)


class Estudantes(db.Model): # define o modelo deo banco de dados usando
   # SQLAlchemy para armazenar informações sobre os estudantes. o modelo
   # possui campos 'id', 'nome', 'email', 'telefone' e 'observacao'.
   id = db.Column(db.Integer, primary_key=True)
   nome = db.Column(db.String(100))
   email = db.Column(db.String(200))
   telefone = db.Column(db.Integer)
   observacao = db.Column(db.String(255))


   def __init__(self, nome, email, telefone, observacao):
       self.nome = nome
       self.email = email
       self.telefone = telefone
       self.observacao = observacao
(app)
def generate_random_string(length): # a função generate_random_string gera uma
   # string aleatória de um comprimento especificado usando letras do alfabeto.
   return ''.join(random.choice(string.ascii_letters) for _ in range(length))


if __name__ == '__main__': # cria o banco de dados se ele ainda não existir.
   app.app_context().push()
   db.create_all()


   # criados 10.000 registros aleatórios e inseridos no banco de dados.
   for _ in range(10000):
       nome = generate_random_string(10)
       email = generate_random_string(15) + '@example.com'
       telefone = random.randint(100000000, 999999999)
       observacao = generate_random_string(50)
       estudante = Estudantes(nome, email, telefone, observacao)
       db.session.add(estudante)


   db.session.commit()


# lista todos os estudantes
# a rota "show_all" inclui paginação
@app.route("/show_all")
def show_all():
   page = request.args.get('page', 1, type=int)  # Recupera o número da página da consulta
   per_page = 10000  # Define o número de registros por página


   start_time = time.time()
   estudantes = Estudantes.query.paginate(page=page, per_page=per_page, error_out=False)
   end_time = time.time()
   elapsed_time_ms = (end_time - start_time) * 1000


   return render_template("show_all.html", estudantes=estudantes.items, elapsed_time=elapsed_time_ms)


# adiciona novo estudante
# GET para quando você errar o preenchimento e precisa informar ao usuário
# POST para recuperar e salvar os dados
@app.route('/new', methods=['GET', 'POST'])
def new():
   if request.method == 'POST':
       if not request.form['nome'] or not request.form['email'] or not request.form['telefone'] or not request.form[
           'observacao']:
           flash('Preencha todos os campos', 'Erro')
       else:
           estudante = Estudantes(request.form['nome'], request.form['email'], request.form['telefone'],
                                  request.form['observacao'])
           db.session.add(estudante)
           db.session.commit()
           flash('Registro salvo com sucesso')
           return redirect(url_for('show_all'))


   # Caso o método seja GET ou haja um problema com o POST, renderize o formulário.
   return render_template('new.html')


# atualiza um estudante
@app.route("/update/<int:id>", methods=['GET', 'POST'])
def update(id):
   estudante = Estudantes.query.get(id)  # recupera o estudando pelo Id


   # verifica os dados que foram preenchidos
   if request.method == 'POST':
       if not request.form['nome'] or not request.form['email'] or not request.form['telefone'] or not request.form['observacao']:
           # caso algum deles não for preenchido, avisa ao usuário
           flash('Preencha todo os campos', 'Erro')
       else:
           # atualiza o objeto os dados do objeto
           estudante.nome = request.form['nome']
           estudante.email = request.form['email']
           estudante.telefone = request.form['telefone']
           estudante.observacao = request.form['observacao']
           db.session.commit() # commit das atualizações
           flash('Registro salvo com sucesso')  # coloca uma mensagem para a próxima página
           return redirect(url_for('show_all')) # redireciona para a página que exibe os estudantes
   return render_template("update.html", estudante=estudante) # renderiza os dados em tela com os dados originais


# deleta um estudante
@app.route("/delete/<int:id>")
def delete(id):
   estudante = Estudantes.query.get(id) # recupera o estudando pelo Id
   db.session.delete(estudante) # deleta o estudante
   db.session.commit() # commit da operação
   flash('Estudate: ' + str(id) + ' foi deletado') # retorna a mensagem de sucesso ao deletar para a próxima página
   return redirect(url_for("show_all")) # redireciona para a página que exibe os estudantes


# {"A": {"B": 5, "C": 3, "D": 2}, "B": {"A": 5, "C": 2, "E": 4}, "C": {"A": 3, "B": 2, "D": 1}, "D": {"A": 2, "C": 1, "E": 7}, "E": {"B": 4, "D": 7}}


# Rota para a página inicial que interage com o grafo
@app.route('/grafo')
def grafo():
   origem = 'A'
   return render_template('grafo.html', caminhos={}, resultado_json=None)


# Rota para receber os valores do grafo via POST que  permite calcular caminhos
# mais curtos em um grafo usando o algoritmo de Dijkstra.
@app.route('/calcular_dijkstra', methods=['POST'])
def calcular_dijkstra_rota():
   grafo_json = request.form.get('grafo_json')
   if grafo_json:
       origem = 'A'
       grafo = json.loads(grafo_json)


       # Medição do tempo - registra o tempo de início
       tempo_inicio = timeit.default_timer()


       caminhos_mais_curto = calcular_dijkstra(grafo, origem)


       # Medição do tempo - registra o tempo de término
       tempo_fim = timeit.default_timer()


       # Calcula o tempo decorrido em milissegundos
       tempo_decorrido = (tempo_fim - tempo_inicio) * 1000


       # Converte o grafo de volta para JSON
       resultado_json = json.dumps(grafo)


       return render_template('grafo.html', caminhos=caminhos_mais_curto, origem=origem, resultado_json=resultado_json,
                              tempo_decorrido=tempo_decorrido)
   # Tratamento para o caso em que grafo_json está vazio
   return "Erro: O campo 'grafo_json' não pode estar vazio."


   return jsonify(caminhos_mais_curtos)


# Função do algoritmo de Dijkstra
def calcular_dijkstra(grafo, origem):


 # Inicialização das distâncias com infinito, exceto a origem que é zero
 distancias = {v: sys.maxsize for v in grafo}
 distancias[origem] = 0


 # Conjunto de vértices visitados
 visitados = set()


 while visitados != set(distancias):
     # Encontra o vértice não visitado com menor distância atual
     vertice_atual = None
     menor_distancia = sys.maxsize
     for v in grafo:
         if v not in visitados and distancias[v] < menor_distancia:
             vertice_atual = v
             menor_distancia = distancias[v]


     # Marca o vértice atual como visitado
     visitados.add(vertice_atual)


     # Atualiza as distâncias dos vértices vizinhos
     for vizinho, peso in grafo[vertice_atual].items():
         if distancias[vertice_atual] + peso < distancias[vizinho]:
             distancias[vizinho] = distancias[vertice_atual] + peso


 # Retorna as distâncias mais curtas a partir da origem
 return distancias


# Definindo o grafo com as conexões e custos
# grafo = {
#  'A': {'B': 5, 'C': 3, 'D': 2},
#  'B': {'A': 5, 'C': 2, 'E': 4},
#  'C': {'A': 3, 'B': 2, 'D': 1},
#  'D': {'A': 2, 'C': 1, 'E': 7},
#  'E': {'B': 4, 'D': 7}
#}


# Ponto de partida
# origem = 'A'


# Chamando o algoritmo de Dijkstra para encontrar os caminhos mais curtos a partir de A
# caminhos_mais_curtos = calcular_dijkstra(grafo, origem)


# Exibindo os caminhos mais curtos
#for destino, distancia in caminhos_mais_curtos.items():
#  print(f"Caminho mais curto de {origem} para {destino}: {distancia}")


# função principal
if __name__ == '__main__':
   app.run(debug=True)