from waitress import serve
from app import app



app.run(debug=True)

# Trigger build v.0.0.1

if __name__ == '__main__':
    serve(app)
