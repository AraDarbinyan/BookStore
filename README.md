# Bookstore 🛒📚

**Bookstore** is a fully functional demo online bookstore built with Django.  
It allows users to browse books by category, add them to a shopping cart, register/login, and place orders.

This project is intended as a portfolio piece and learning project for a junior Django developer.

---

## 🚀 Features

- User registration and login
- Book catalog with images, descriptions, and prices
- Category-based filtering
- Search functionality
- Shopping cart (session-based)
- Checkout and order creation
- Admin interface for managing books and orders
- Clean design with simple CSS per page


## 📁 Tech Stack

- **Backend**: Django (Python 3.13)
- **Frontend**: HTML, CSS (custom per-page files), Django templates
- **Database**: SQLite (default)
- **Admin**: Django admin panel
- **Other**: Django static & media file handling


## 🧱 Pages

- `/` – Home (book listing)
- `/books/` – All books
- `/about/` – About the project
- `/contact/` – Contact form
- `/login/` – login form
- `/register/` – register form
- `/progile/` – profile page
- `/cart/` – user's cart
- `/thank-you/` – thank you for ordering

---

## 🐳 Run with Docker

### 1. Build the Docker image
```bash
docker build -t bookstore:latest .
```

### 2. Run database migrations
```bash
docker run --rm -it -v ${PWD}:/app bookstore:latest python manage.py migrate
```

### 3. (Optional) Load sample data
```bash
docker run --rm -it -v ${PWD}:/app bookstore:latest python manage.py loaddata authors.json books.json categories.json
```

### 4. Start the Django server
```bash
docker run -it --rm -p 8000:8000 -v ${PWD}:/app bookstore:latest
```

Open your browser and go to 👉 [http://localhost:8000](http://localhost:8000)

---

## 🧑‍💻 Local Installation (without Docker)

### 1. Clone the repository
```bash
git clone https://github.com/<your-username>/bookstore.git
cd bookstore
```

### 2. Create and activate a virtual environment
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run migrations and load data
```bash
python manage.py migrate
python manage.py loaddata authors.json books.json categories.json
```

### 5. Start the development server
```bash
python manage.py runserver
```

Visit [http://127.0.0.1:8000](http://127.0.0.1:8000)