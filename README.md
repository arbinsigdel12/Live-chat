Follow the steps below to set up and run the project on your local machine.

### 1. Clone the repository
git clone https://github.com/arbinsigdel12/Live-chat.git
cd Live-chat

### 2. Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate

### 3. Install dependencies
pip install -r requirements.txt

### 4. Apply migration
python manage.py makemigrations
python manage.py migrate

### 5. Run the development server
daphne core.asgi:application

### 6. Access the application
http://127.0.0.1:8000/

