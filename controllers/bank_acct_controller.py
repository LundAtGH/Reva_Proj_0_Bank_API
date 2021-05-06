from flask import jsonify, request
from exceptions.resource_not_found import ResourceNotFound
from exceptions.resource_unavailable import ResourceUnavailable
from models.bank_acct import BankAcct
from services.bank_acct_service import BankAcctService


def route(app):

    @app.route("/clients/<client_id>/accounts", methods=['GET'])
    def get_all_bank_accts(client_id):
        if not request.args:
            try:
                return jsonify(BankAcctService.all_bank_accts(int(client_id))), 200
            except ResourceNotFound as r:
                return r.message, 404
        else:
            try:
                conditions = "something"
                return jsonify(BankAcctService.some_bank_accts(int(client_id), conditions)), 200
            except ResourceNotFound as r:
                return r.message, 404

    @app.route("/clients/<client_id>/accounts?<conditions>", methods=['GET'])
    def get_some_bank_accts(client_id, conditions):
        try:
            return jsonify(BankAcctService.some_bank_accts(int(client_id), conditions)), 200
        except ResourceNotFound as r:
            return r.message, 404

    @app.route("/clients/<client_id>/accounts/<bank_acct_id>", methods=['GET'])
    def get_bank_acct(client_id, bank_acct_id):
        try:
            bank_acct = BankAcctService.get_bank_acct_by_id(int(client_id), int(bank_acct_id))
            return jsonify(bank_acct.json()), 200
        except ValueError as e:
            return "Client or account ID invalid.", 400
            # Bad request
        except ResourceNotFound as r:
            return r.message, 404

    @app.route("/clients/<client_id>/accounts", methods=['POST'])
    def post_bank_acct(client_id):
        bank_acct = BankAcct.json_parse(request.json)
        bank_acct.holder_id = int(client_id)
        bank_acct = BankAcctService.create_bank_acct(bank_acct)

        return jsonify(bank_acct.json()), 201

    @app.route("/clients/<client_id>/accounts/<bank_acct_id>", methods=['PUT'])
    def put_bank_acct(client_id, bank_acct_id):
        try:
            bank_acct = BankAcct.json_parse(request.json)
            bank_acct.bank_acct_id = int(bank_acct_id)
            bank_acct.holder_id = int(client_id)
            BankAcctService.update_bank_acct(bank_acct)

            return jsonify(bank_acct.json()), 200
        except ResourceNotFound as r:
            return r.message, 404

    @app.route("/clients/<client_id>/accounts/<bank_acct_id>", methods=['DELETE'])
    def del_bank_acct(client_id, bank_acct_id):
        try:
            BankAcctService.delete_bank_acct(int(client_id), int(bank_acct_id))
            return "", 204
        except ResourceNotFound as r:
            return r.message, 404

    @app.route("/clients/<client_id>/accounts/<bank_acct_id>", methods=['PATCH'])
    def patch_bank_acct(client_id, bank_acct_id):

        depo_req = float(request.json['deposit'])
        with_req = float(request.json['withdraw'])

        if depo_req > 0:
            try:
                bank_acct = BankAcctService.deposit_funds(int(client_id), int(bank_acct_id), depo_req)
                return jsonify(bank_acct.json()), 200
            except ResourceNotFound as r:
                return r.message, 404

        elif with_req > 0:
            try:
                bank_acct = BankAcctService.withdraw_funds(int(client_id), int(bank_acct_id), with_req)
                return jsonify(bank_acct.json()), 200
            except ResourceUnavailable as e:
                return e.message, 422
            except ResourceNotFound as r:
                return r.message, 404

    @app.route("/clients/<client_id>/accounts/<id_of_BA_taken_from>/transfer/<id_of_BA_depos_into>",
               methods=['PATCH'])
    def tran_betw_bank_accts(client_id, id_of_BA_taken_from, id_of_BA_depos_into):

        amount = float(request.json['amount'])

        try:
            bank_acct = BankAcctService.transfer_funds(
                int(client_id), int(id_of_BA_taken_from), int(id_of_BA_depos_into), amount
            )
            return jsonify(bank_acct.json()), 200
        except ResourceUnavailable as e:
            return e.message, 422
        except ResourceNotFound as r:
            return r.message, 404
