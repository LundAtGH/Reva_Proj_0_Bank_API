def route(app):

    @app.route("/", methods=['GET', 'POST'])
    def hello():
        return "Hello, Revature Banking customer!"

    @app.route("/contact")
    def contact():
        return "Revature Banking 24/7 customer service line: 555-555-5555."