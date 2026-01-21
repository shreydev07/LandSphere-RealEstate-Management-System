
# 🏡 LandSphere – Smart Real Estate Management Platform

LandSphere is a full-stack Django-based real estate web application designed to manage property listings, owners, seekers (buyers/tenants), agents, and administrative operations through a secure and scalable system.

---

## 🚀 Project Overview

LandSphere provides a centralized digital platform where:

- Property owners can list and manage properties
- Property seekers can browse, search, and inquire about listings
- Admin manages users, properties, and documents
- Secure handling of property images and legal documents
- Modern UI with Django-powered backend

---

## 🛠️ Technology Stack

### Backend
- Python 3.x
- Django Framework
- Django ORM
- SQLite (default database)

### Frontend
- HTML5
- CSS3
- JavaScript
- Bootstrap

---

## 📁 Project Structure

LandSphere/
├── adminapp/
├── mainapp/
├── ownerapp/
├── seekerapp/
├── LandSphere/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── static/
├── photos/
├── property_images/
├── profile_photos/
├── id_proofs/
├── gov_id_proofs/
├── land_certificates/
├── db.sqlite3
├── manage.py
└── README.md

---

## 👥 User Roles & Features

### Admin
- Manage users and properties
- Approve or reject property listings
- View uploaded documents
- Full system control via Django Admin

### Property Owner
- Register and login
- Upload and manage properties
- Upload ID proofs and land certificates
- Manage personal profile

### Property Seeker
- Register and login
- Browse and search properties
- View property details
- Contact property owners

---

## 📸 Media & Document Management

Supports upload and management of:
- Property images
- Profile photos
- Government ID proofs
- Land ownership certificates

---

## ⚙️ Installation & Setup

### Step 1: Clone Repository
git clone https://github.com/shreydev07/LandSphere.git
cd LandSphere


### Step 3: Install Dependencies
pip install django

### Step 4: Database Migration
python manage.py makemigrations
python manage.py migrate

### Step 5: Create Admin User
python manage.py createsuperuser

### Step 6: Run Server
python manage.py runserver

---

## 🔑 Admin Panel
http://127.0.0.1:8000/admin/

---

## 🎯 Key Highlights
- Modular Django architecture
- Secure authentication
- Scalable and maintainable codebase
- Clean UI with responsive design

---

## 🔮 Future Enhancements
- Advanced search & filters
- Payment gateway integration
- Email & notification system
- REST API (DRF)
- Cloud storage integration

---

## 🤝 Contribution
Contributions are welcome via pull requests.

---

## 📜 License
This project is for educational and portfolio purposes.

---

## 👨‍💻 Developed By
Shreyansh Srivastava  
Django Developer  
Happy Learning 🚀
