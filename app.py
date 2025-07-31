from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "✅ Hello from Reality Roaster! Your API is running."

if __name__ == '__main__':
    app.run()
