# Outfit Recommendation System

## Overview
This is a Flask-based full-stack web application that recommends outfits based on weather conditions and occasion. Users can register, log in, receive outfit suggestions, and view their past selections.

The project is designed to provide a simple and interactive solution for choosing outfits in different situations.

---

## Features
- User authentication (Login and Register)
- Outfit recommendations based on:
  - Weather (Hot, Cold, Rainy)
  - Occasion (Casual, Formal, Party)
- Predefined outfit suggestion system
- History tracking of user selections
- SQLite database integration
- Simple and user-friendly interface

---

## Tech Stack

Backend:
- Python
- Flask

Frontend:
- HTML
- CSS
- Jinja Templates

Database:
- SQLite

---

## Project Structure

project/
│
├── static/
│   └── images/
│
├── templates/
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── recommend.html
│   ├── result.html
│   └── history.html
│
├── outfits.db
├── app.py
└── README.md

---

## Installation and Setup

1. Clone the repository
git clone https://github.com/your-username/outfit-recommender.git
cd outfit-recommender

2. Create a virtual environment
python -m venv venv

3. Activate the environment

Windows:
venv\Scripts\activate

Mac/Linux:
source venv/bin/activate

4. Install dependencies
pip install flask

5. Run the application
python app.py

---

## Usage

1. Open your browser  
2. Go to: http://127.0.0.1:5000/  
3. Register a new account  
4. Login  
5. Select weather and occasion  
6. View outfit recommendations  
7. Check history for previous selections  

---
<img width="1782" height="902" alt="Screenshot 2026-03-30 141532" src="https://github.com/user-attachments/assets/c8f04f7b-e1cb-435b-b468-ad7ea064d50c" />
<img width="1716" height="816" alt="image" src="https://github.com/user-attachments/assets/f07fd5ff-61ac-4580-8b81-6112783f7e15" />



## How It Works

- The user selects weather and occasion
- The backend processes the input using predefined outfit data
- Matching outfits are displayed with details such as name, description, and tags
- User selections are stored in the SQLite database for history tracking

---
<img width="1694" height="887" alt="image" src="https://github.com/user-attachments/assets/527a0cdd-b24c-4ea1-8326-e01d5e309fd8" />
<img width="1727" height="903" alt="image" src="https://github.com/user-attachments/assets/f6a13ecc-c661-4a96-bfdd-cbb2331deaad" />




## Database Schema

Users Table:
- id (INTEGER, Primary Key)
- username (TEXT, Unique)
- password (TEXT)

User Selections Table:
- id (INTEGER, Primary Key)
- weather (TEXT)
- occasion (TEXT)

---

## Future Enhancements

- Implement password hashing for better security
- Add AI/ML-based recommendation system
- Integrate real-time weather API
- Add favorites or saved outfits feature
- Improve UI/UX design

---

## Limitations

- Passwords are stored in plain text
- Recommendations are rule-based
- Limited dataset of outfits


---

## Author

Vishnu Priya

---
