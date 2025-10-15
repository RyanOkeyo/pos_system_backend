import sys
import os

# Add the backend directory to the path
backend_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, backend_dir)

from app import create_app
from dotenv import load_dotenv

load_dotenv()

app = create_app()

if __name__ == '__main__':
    print("Starting Flask server...")
    print("Server running on http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
