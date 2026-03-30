from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
import os
from functools import wraps

app = Flask(__name__)
app.secret_key = 'super_secret_key'

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Database initialization
DB_FILE = 'outfits.db'

def init_db():
    """Initializes the SQLite database with the required tables."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_selections (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            weather TEXT NOT NULL,
            occasion TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Initialize the database when the app starts
init_db()

@app.route('/')
def home():
    """Route for the Home page."""
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = cursor.fetchone()
        conn.close()
        
        if user:
            session['user'] = username
            flash('Logged in successfully.', 'success')
            return redirect(url_for('recommend'))
        else:
            flash('Invalid username or password, please try again.', 'danger')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if len(username) < 3 or len(password) < 6:
            flash('Username must be at least 3 characters and password at least 6 characters.', 'danger')
            return redirect(url_for('register'))
            
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            flash('Registration successful. Please log in.', 'success')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Username already exists. Please choose a different one.', 'danger')
        finally:
            conn.close()
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('Logged out successfully.', 'info')
    return redirect(url_for('home'))

@app.route('/recommend')
@login_required
def recommend():
    """Route for the Recommendation form page."""
    return render_template('recommend.html')

@app.route('/history')
@login_required
def history():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT weather, occasion FROM user_selections ORDER BY id DESC")
    data = cursor.fetchall()
    conn.close()
    return render_template('history.html', data=data)

@app.route('/result', methods=['POST'])
@login_required
def result():
    """Route for handling the form submission and displaying the result."""
    if request.method == 'POST':
        weather = request.form.get('weather')
        occasion = request.form.get('occasion')
        
        # Store user selection in SQLite database
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO user_selections (weather, occasion) VALUES (?, ?)', (weather, occasion))
        conn.commit()
        conn.close()

        # Outfit recommendation logic using dictionaries
        outfit_db = {
            'Hot': {
                'Casual': [
                    {'name': 'Linen Button-Down & Chinos', 'image': 'hot_casual_1.jpg', 'description': 'Light and breathable for hot days.', 'tags': ['Linen', 'Breathable']},
                    {'name': 'Graphic T-Shirt & Denim Shorts', 'image': 'hot_casual_2.jpg', 'description': 'A relaxed look for summer outings.', 'tags': ['Streetwear', 'Comfort']},
                    {'name': 'Polo Shirt & Khaki Shorts', 'image': 'hot_casual_3.jpg', 'description': 'Smart casual vibe, perfect for daytime.', 'tags': ['Smart Casual', 'Classic']},
                    {'name': 'Tank Top & Board Shorts', 'image': 'hot_casual_4.jpg', 'description': 'Ultimate beach or pool setup.', 'tags': ['Beach', 'Active']},
                ],
                'Formal': [
                    {'name': 'Light Grey Cotton Suit', 'image': 'hot_formal_1.jpg', 'description': 'Keeps you cool during summer formal events.', 'tags': ['Cotton', 'Summer Wedding']},
                    {'name': 'Linen Blazer & Dress Pants', 'image': 'hot_formal_2.jpg', 'description': 'A lightweight option for formal meetings.', 'tags': ['Linen', 'Elegant']},
                    {'name': 'Seersucker Suit', 'image': 'hot_formal_3.jpg', 'description': 'Classic summer formal wear.', 'tags': ['Seersucker', 'Classic']},
                    {'name': 'Short Sleeve Dress Shirt & Trousers', 'image': 'hot_formal_4.jpg', 'description': 'A crisp look that beats the heat.', 'tags': ['Business', 'Cool']},
                ],
                'Party': [
                    {'name': 'Short Sleeve Printed Shirt & Chinos', 'image': 'hot_party_1.jpg', 'description': 'Fun and vibrant for summer nights.', 'tags': ['Printed', 'Night Out']},
                    {'name': 'Lightweight Bomber & T-Shirt', 'image': 'hot_party_2.jpg', 'description': 'A stylish layered look without overheating.', 'tags': ['Layering', 'Stylish']},
                    {'name': 'Cuban Collar Shirt & Tailored Shorts', 'image': 'hot_party_3.jpg', 'description': 'Retro vibes for a rooftop party.', 'tags': ['Retro', 'Trendy']},
                    {'name': 'Silk Blend Shirt & Dark Jeans', 'image': 'hot_party_4.jpg', 'description': 'Luxurious feel, perfect for a club setting.', 'tags': ['Silk', 'Clubwear']},
                ]
            },
            'Cold': {
                'Casual': [
                    {'name': 'Chunky Knit Sweater & Dark Jeans', 'image': 'cold_casual_1.jpg', 'description': 'Cozy and warm for a relaxed day.', 'tags': ['Knit', 'Cozy']},
                    {'name': 'Puffer Jacket & Joggers', 'image': 'cold_casual_2.jpg', 'description': 'Sporty and insulated against the cold.', 'tags': ['Sporty', 'Insulated']},
                    {'name': 'Flannel Shirt & Corduroy Pants', 'image': 'cold_casual_3.jpg', 'description': 'A textured, casual winter look.', 'tags': ['Flannel', 'Textured']},
                    {'name': 'Hoodie & Denim Jacket Layer', 'image': 'cold_casual_4.jpg', 'description': 'Classic streetwear layering.', 'tags': ['Layering', 'Streetwear']},
                ],
                'Formal': [
                    {'name': 'Wool Suit & Cashmere Overcoat', 'image': 'cold_formal_1.jpg', 'description': 'The ultimate winter formal combination.', 'tags': ['Wool', 'Overcoat']},
                    {'name': 'Turtleneck & Tailored Suit', 'image': 'cold_formal_2.jpg', 'description': 'Sleek, modern, and warm.', 'tags': ['Turtleneck', 'Modern']},
                    {'name': 'Tweed Blazer & Dress Trousers', 'image': 'cold_formal_3.jpg', 'description': 'A classic and highly formal choice.', 'tags': ['Tweed', 'Heritage']},
                    {'name': 'Peacoat over Dress Shirt & Tie', 'image': 'cold_formal_4.jpg', 'description': 'Nautical heritage combined with formal wear.', 'tags': ['Peacoat', 'Classic']},
                ],
                'Party': [
                    {'name': 'Velvet Blazer & Dark Jeans', 'image': 'cold_party_1.jpg', 'description': 'Rich texture perfect for winter parties.', 'tags': ['Velvet', 'Rich Vibes']},
                    {'name': 'Leather Jacket over Graphic Tee', 'image': 'cold_party_2.jpg', 'description': 'Edgy and warm for a night out.', 'tags': ['Leather', 'Edgy']},
                    {'name': 'Fleece-lined Denim Jacket & Chinos', 'image': 'cold_party_3.jpg', 'description': 'Casual party vibe with extra warmth.', 'tags': ['Fleece', 'Warm']},
                    {'name': 'Cashmere Sweater & Tailored Trousers', 'image': 'cold_party_4.jpg', 'description': 'Understated luxury for an indoor event.', 'tags': ['Cashmere', 'Luxury']},
                ]
            },
            'Rainy': {
                'Casual': [
                    {'name': 'Waterproof Windbreaker & Jeans', 'image': 'rainy_casual_1.jpg', 'description': 'Lightweight protection against the rain.', 'tags': ['Waterproof', 'Lightweight']},
                    {'name': 'Raincoat & Rubber Boots', 'image': 'rainy_casual_2.jpg', 'description': 'The classic foul-weather setup.', 'tags': ['Classic', 'Dry']},
                    {'name': 'Anorak & Cargo Pants', 'image': 'rainy_casual_3.jpg', 'description': 'Utilitarian style for dreary days.', 'tags': ['Utilitarian', 'Practical']},
                    {'name': 'Water-Resistant Hoodie & Joggers', 'image': 'rainy_casual_4.jpg', 'description': 'Everyday comfort with rain readiness.', 'tags': ['Comfort', 'Ready']},
                ],
                'Formal': [
                    {'name': 'Trench Coat over Suit', 'image': 'rainy_formal_1.jpg', 'description': 'Timeless elegance in the pouring rain.', 'tags': ['Trench Coat', 'Timeless']},
                    {'name': 'Mac Coat & Dress Trousers', 'image': 'rainy_formal_2.jpg', 'description': 'Minimalist rain protection.', 'tags': ['Minimalist', 'Sleek']},
                    {'name': 'Water-Repellent Blazer & Trousers', 'image': 'rainy_formal_3.jpg', 'description': 'Smart choice for damp commutes.', 'tags': ['Repellent', 'Smart']},
                    {'name': 'Galoshes over Dress Shoes', 'image': 'rainy_formal_4.jpg', 'description': 'Protect your formal footwear.', 'tags': ['Protective', 'Footwear']},
                ],
                'Party': [
                    {'name': 'Sleek Rain Jacket over Party Wear', 'image': 'rainy_party_1.jpg', 'description': 'Stay dry without ruining your look.', 'tags': ['Sleek', 'Party-Ready']},
                    {'name': 'Dark Water-Resistant Bomber', 'image': 'rainy_party_2.jpg', 'description': 'Nightlife approved rain gear.', 'tags': ['Nightlife', 'Resistant']},
                    {'name': 'Lightweight Parka & Dark Jeans', 'image': 'rainy_party_3.jpg', 'description': 'Easy to shed once you get inside.', 'tags': ['Parka', 'Easy']},
                    {'name': 'Waterproof Chelsea Boots & Overcoat', 'image': 'rainy_party_4.jpg', 'description': 'Keep your feet dry in style.', 'tags': ['Boots', 'Stylish']},
                ]
            }
        }

        # Fetch matching outfits or default to an empty list
        recommended_outfits = outfit_db.get(weather, {}).get(occasion, [])
        
        # Fallback if somehow there's no match
        if not recommended_outfits:
            recommended_outfits = [{'name': 'Standard Everyday Wear', 'image': 'default.jpg', 'description': 'A versatile outfit for any condition.', 'tags': ['Versatile', 'Standard']}]

        return render_template('result.html', weather=weather, occasion=occasion, outfits=recommended_outfits)
    
    return redirect(url_for('recommend'))

if __name__ == '__main__':
    # Ensure static/images directory exists where users can put images
    os.makedirs('static/images', exist_ok=True)
    app.run(debug=True)
