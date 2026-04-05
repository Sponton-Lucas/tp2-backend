from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello():
    return "¡Hola, Flask está funcionando!"

if __name__ == "__main__":
    app.run(debug=True)
