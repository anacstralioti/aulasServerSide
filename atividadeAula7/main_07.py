from flask import Flask, request, jsonify, Response
import json
from Customer import Customer

app = Flask(__name__)

# Customers list
customers = []


@app.route('/customers_list', methods=['GET'])
def get_customers_list():
    vetor = []
    vetor.append(Customer(1, "João").to_dict())
    vetor.append(Customer(2, "Fernando").to_dict())
    return Response(response=json.dumps(vetor), status=200, content_type="application/json")


@app.route('/customers', methods=['GET'])
def get_customers():
    response = jsonify({'customers': customers}), 200

    customers.append({'name': 'teste', 'email': 'email@.com'})

    return response


@app.route('/customers', methods=['POST'])
def new_customer():
    request_data = request.get_json()
    customer_data = request_data['customers']

    for data in customer_data:
        customers.append({'name': data['name'], 'email': data['email']})

    return 'OK', 201


if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5000", debug=True)