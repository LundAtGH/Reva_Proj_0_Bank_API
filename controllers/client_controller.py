from flask import jsonify, request
from exceptions.resource_not_found import ResourceNotFound
from exceptions.resource_unavailable import ResourceUnavailable
from models.client import Client
from services.client_service import ClientService


def route(app):

    @app.route("/clients", methods=['GET'])
    def get_all_clients():
        return jsonify(ClientService.all_clients()), 200

    @app.route("/clients/<client_id>", methods=['GET'])
    def get_client(client_id):
        try:
            client = ClientService.get_client_by_id(int(client_id))
            return jsonify(client.json()), 200
        except ValueError as e:
            return "Not a valid client ID.", 400
            # Bad request
        except ResourceNotFound as r:
            return r.message, 404

    @app.route("/clients", methods=['POST'])
    def post_client():
        client = Client.json_parse(request.json)
        client = ClientService.create_client(client)
        return jsonify(client.json()), 201

    @app.route("/clients/<client_id>", methods=['PUT'])
    def put_client(client_id):
        client = Client.json_parse(request.json)
        client.holder_id = int(client_id)

        try:
            client = ClientService.update_client(client)
            return jsonify(client.json()), 200

        except ResourceNotFound as r:
            return r.message, 404

    @app.route("/clients/<client_id>", methods=['DELETE'])
    def del_client(client_id):
        try:
            ClientService.delete_client(int(client_id))
            return "", 205

        except ResourceNotFound as r:
            return r.message, 404
