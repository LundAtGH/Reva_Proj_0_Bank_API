from controllers import bank_acct_controller, home_controller, client_controller


def route(app):

    client_controller.route(app)
    bank_acct_controller.route(app)
    home_controller.route(app)
