import jwt

# Dados do cabeçalho
header = {
    "alg" : "HS256",
    "typ" : "JWT"
}

# Dados do payload

payload = {
    "id" : "5465132118916541894",
    #não FAZER ISSO
    "name": "Andrei Carniel",
    "phone": "47984451016",
    "address": "Rua dos Imigrantes",
    "work" : "Univerdade Catolica"
}

# chave secreta
# exemplo de senha "segura"
secret = "Catolica20231"

# Geração do Token

token = jwt.encode(payload, secret, algorithm=header["alg"])

print(token)

print(jwt.decode(token, secret, algorithms="HS256"))