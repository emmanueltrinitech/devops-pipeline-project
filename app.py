from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/")
def home():
    return """
    <h1>Trinitech DevOps CI/CD Pipeline</h1>
    <p>Application Status: Running</p>
    <p>Version: 1.2</p>
    """


@app.route("/health")
def health():
    return jsonify(
        application="trinitech-devops-app",
        status="healthy",
        version="1.2"
    ), 200


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=8081
    )
this is invalid python
