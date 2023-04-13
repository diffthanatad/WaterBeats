from flask import Flask,request

app = Flask(__name__)

@app.route("/new_data", methods=["POST"])
def test():
    print(request.json)
    return "OK"

if __name__ == "__main__":
    app.run(host="localhost", port=23333, debug=True)