# Email Automation System

## Overview
This is a full-featured Blog App that allows users to create, read, update, and delete blog posts. The application features an interactive UI with a modern gradient-based design and smooth animations.

## Features
- User authentication (Login/Register)
- Create, edit, and delete blog posts
- Upvote and downvote system for posts
- Comment System for user engagement
- Responsive design for different screen sizes
- Styled using CSS with linear gradient effects
- Secure authentication and session management
- Interactive navigation menu

## Dependencies
- Python 3.x
- Flask
- Flask-Cors (for cross-origin requests)
- Celery (for asynchronous tasks)
- Redis (message broker for Celery)
- MongoDB (for storing user and email data)
- Requests (for HTTP requests)

## Setup
### Installation

### Prerequisites:
- Python 3.x
- Django framework
- Virtual environment (optional but recommended)

### Step 1: Clone the repository:
```bash
git clone https://github.com/yourusername/blog-app.git
cd blog-app/blogsite
```
### Step 2: Create a virtual environment (optional but recommended):
```bash
python -m venv env
source env/bin/activate  # For macOS/Linux
env\Scripts\activate  # For Windows
```
### Step 3: Install Required Libraries
Run the following command to install the required dependencies:
```bash
pip install -r requirements.txt
```
### Step 4: Run database migrations:
```bash
python manage.py migrate
```

### Step 5: Start the server:
```bash
python manage.py runserver
```

## Folder Structure
```bash
blogsite/
│── blog/                # Django app for blogs
│── blogsite/                # Django app for blogs
│── Media/               # Media files
│── users/               # Django app for authentication
│── static/              # CSS, JS, and image files
│── templates/           # HTML templates
│── manage.py            # Django management script
│── db.sqlite3           # SQLite database (if using SQLite)
│── requirements.txt     # Python dependencies
│── README.md            # Project documentation
```
