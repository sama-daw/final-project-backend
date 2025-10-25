# 🍰 Dessert Shop - Backend API

Django REST API for Dessert Shop E-commerce Platform

## 📌 Project Description

This is the backend API for the Dessert Shop e-commerce website. Built with Django and Django REST Framework, it provides endpoints for product management, order processing, and customer data handling.

## ✨ Features

- 🛍️ Product Management (CRUD operations)
- 📦 Order Processing System
- 👤 Customer Information Management
- 🔐 Admin Panel with Custom Views
- 🌐 RESTful API Architecture
- 📸 Media File Handling
- 🔍 Search and Filter Support

## 🛠️ Tech Stack

- **Framework:** Django 4.x
- **API:** Django REST Framework
- **Database:** SQLite (Development)
- **CORS:** django-cors-headers
- **Authentication:** JWT (Simple JWT)

## 📦 Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager
- Git

### Setup Instructions

1. **Clone the repository:**
```bash
git clone https://github.com/sama-daw/dessert-shop-backend.git
cd dessert-shop-backend
```

2. **Create virtual environment:**
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On Mac/Linux
source venv/bin/activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Run migrations:**
```bash
python manage.py migrate
```

5. **Create superuser (Admin):**
```bash
python manage.py createsuperuser
```

6. **Run development server:**
```bash
python manage.py runserver
```

The API will be available at: `http://127.0.0.1:8000/`

## 🔗 API Endpoints

### Products
- `GET /api/products/` - List all products
- `POST /api/products/` - Create new product (Admin only)
- `GET /api/products/{id}/` - Get product details
- `PUT /api/products/{id}/` - Update product (Admin only)
- `DELETE /api/products/{id}/` - Delete product (Admin only)

### Orders
- `POST /api/orders/` - Create new order
- `GET /api/orders/{id}/` - Get order details

### Admin
- `GET /admin/` - Django Admin Panel

### Authentication
- `POST /api/token/` - Obtain JWT token
- `POST /api/token/refresh/` - Refresh JWT token

## 📂 Project Structure

```
backend/
├── manage.py
├── requirements.txt
├── db.sqlite3
├── myproject/
│   ├── settings.py
│   ├── urls.py
│   └── views.py
├── shop/
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   ├── admin.py
│   └── urls.py
├── media/
│   └── products/
└── templates/
    └── home.html
```

## 🗄️ Database Models

### Product
- `name` - Product name
- `price` - Product price
- `description` - Product description
- `image` - Product image
- `stock` - Available quantity
- `is_active` - Active status

### Order
- `customer_name` - Customer name
- `phone` - Contact number
- `address` - Delivery address
- `status` - Order status
- `created_at` - Order date

### OrderItem
- `order` - Foreign key to Order
- `product` - Foreign key to Product
- `quantity` - Item quantity

## ⚙️ Configuration

### CORS Settings
Update `settings.py` to allow your frontend domain:

```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "https://your-frontend-domain.com",
]
```

### Media Files
Media files are stored in the `media/` directory. Make sure to configure your production server to serve these files properly.

## 🚀 Deployment

For production deployment, consider:
- Using PostgreSQL instead of SQLite
- Configuring environment variables
- Setting `DEBUG = False`
- Using a proper web server (Gunicorn, uWSGI)
- Setting up static and media file serving

## 👩‍💻 Author

**Sama Dawood**
- GitHub: [@sama-daw](https://github.com/sama-daw)
- Instagram: [@sama_daw](https://www.instagram.com/sama_daw)

## 📄 License

This project is licensed under the MIT License.

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

## 📞 Contact

For any questions or support, please contact: +20 101 691 0757