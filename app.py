# =============================================================================
# CINEMAPULSE - FLASK APPLICATION
# Real-Time Customer Feedback Analysis Platform
# =============================================================================
# 
# AWS DEPLOYMENT CONFIGURATION:
# - EC2 Instance: Amazon Linux 2 / Ubuntu 22.04
# - RDS: MySQL 8.0
# - Security Groups: Allow ports 22, 80, 443, 5000, 3306
# =============================================================================

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from datetime import datetime
import os

# =============================================================================
# AWS RDS MYSQL CONFIGURATION
# =============================================================================
# Uncomment and configure for production deployment:
#
# import mysql.connector
# from mysql.connector import pooling
#
# DB_CONFIG = {
#     'host': os.environ.get('DB_HOST', 'your-rds-endpoint.rds.amazonaws.com'),
#     'user': os.environ.get('DB_USER', 'admin'),
#     'password': os.environ.get('DB_PASSWORD', 'your-secure-password'),
#     'database': os.environ.get('DB_NAME', 'cinemapulse'),
#     'pool_name': 'cinemapulse_pool',
#     'pool_size': 5
# }
#
# def get_db_connection():
#     """Get a connection from the pool"""
#     try:
#         connection_pool = mysql.connector.pooling.MySQLConnectionPool(**DB_CONFIG)
#         return connection_pool.get_connection()
#     except mysql.connector.Error as err:
#         print(f"Database connection error: {err}")
#         return None
# =============================================================================

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'cinemapulse-secret-key-change-in-production')

# =============================================================================
# IN-MEMORY DATA STORAGE (Replace with RDS MySQL in production)
# =============================================================================
# 
# MySQL Schema for AWS RDS:
# 
# CREATE DATABASE cinemapulse;
# USE cinemapulse;
#
# CREATE TABLE movies (
#     id INT PRIMARY KEY AUTO_INCREMENT,
#     title VARCHAR(255) NOT NULL,
#     description TEXT,
#     image_url VARCHAR(500),
#     director VARCHAR(255),
#     duration VARCHAR(50),
#     year INT,
#     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
# );
#
# CREATE TABLE genres (
#     id INT PRIMARY KEY AUTO_INCREMENT,
#     name VARCHAR(100) NOT NULL UNIQUE
# );
#
# CREATE TABLE movie_genres (
#     movie_id INT,
#     genre_id INT,
#     PRIMARY KEY (movie_id, genre_id),
#     FOREIGN KEY (movie_id) REFERENCES movies(id) ON DELETE CASCADE,
#     FOREIGN KEY (genre_id) REFERENCES genres(id) ON DELETE CASCADE
# );
#
# CREATE TABLE feedbacks (
#     id INT PRIMARY KEY AUTO_INCREMENT,
#     movie_id INT NOT NULL,
#     user_name VARCHAR(255) NOT NULL,
#     user_email VARCHAR(255) NOT NULL,
#     rating INT NOT NULL CHECK (rating >= 1 AND rating <= 5),
#     comment TEXT,
#     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#     FOREIGN KEY (movie_id) REFERENCES movies(id) ON DELETE CASCADE,
#     INDEX idx_movie_id (movie_id),
#     INDEX idx_created_at (created_at)
# );
# =============================================================================

# In-memory movie data (Replace with: SELECT * FROM movies)
movies = [
    {
        'id': 1,
        'title': 'Inception',
        'description': 'A thief who steals corporate secrets through dream-sharing technology is given the inverse task of planting an idea into the mind of a C.E.O. Christopher Nolan\'s mind-bending masterpiece explores the depths of human consciousness.',
        'image': 'https://images.unsplash.com/photo-1536440136628-849c177e76a1?w=800',
        'director': 'Christopher Nolan',
        'duration': '2h 28min',
        'year': 2010,
        'genres': ['Sci-Fi', 'Action', 'Thriller']
    },
    {
        'id': 2,
        'title': 'The Dark Knight',
        'description': 'When the menace known as the Joker wreaks havoc and chaos on Gotham, Batman must accept one of the greatest psychological and physical tests of his ability to fight injustice.',
        'image': 'https://images.unsplash.com/photo-1509347528160-9a9e33742cdb?w=800',
        'director': 'Christopher Nolan',
        'duration': '2h 32min',
        'year': 2008,
        'genres': ['Action', 'Crime', 'Drama']
    },
    {
        'id': 3,
        'title': 'Interstellar',
        'description': 'A team of explorers travel through a wormhole in space in an attempt to ensure humanity\'s survival. A visually stunning journey through space and time.',
        'image': 'https://images.unsplash.com/photo-1419242902214-272b3f66ee7a?w=800',
        'director': 'Christopher Nolan',
        'duration': '2h 49min',
        'year': 2014,
        'genres': ['Sci-Fi', 'Adventure', 'Drama']
    },
    {
        'id': 4,
        'title': 'Pulp Fiction',
        'description': 'The lives of two mob hitmen, a boxer, a gangster and his wife, and a pair of diner bandits intertwine in four tales of violence and redemption.',
        'image': 'https://images.unsplash.com/photo-1594909122845-11baa439b7bf?w=800',
        'director': 'Quentin Tarantino',
        'duration': '2h 34min',
        'year': 1994,
        'genres': ['Crime', 'Drama']
    },
    {
        'id': 5,
        'title': 'The Matrix',
        'description': 'A computer programmer discovers that reality as he knows it is a simulation created by machines, and joins a rebellion to overthrow them.',
        'image': 'https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?w=800',
        'director': 'The Wachowskis',
        'duration': '2h 16min',
        'year': 1999,
        'genres': ['Sci-Fi', 'Action']
    },
    {
        'id': 6,
        'title': 'Parasite',
        'description': 'Greed and class discrimination threaten the newly formed symbiotic relationship between the wealthy Park family and the destitute Kim clan.',
        'image': 'https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?w=800',
        'director': 'Bong Joon-ho',
        'duration': '2h 12min',
        'year': 2019,
        'genres': ['Thriller', 'Drama', 'Comedy']
    }
]

# In-memory feedback storage (Replace with: SELECT * FROM feedbacks)
feedbacks = [
    {
        'id': 1,
        'movie_id': 1,
        'user_name': 'John Doe',
        'user_email': 'john@example.com',
        'rating': 5,
        'comment': 'Absolutely mind-blowing! Nolan has outdone himself with this masterpiece.',
        'created_at': '2024-01-15 10:30:00'
    },
    {
        'id': 2,
        'movie_id': 1,
        'user_name': 'Sarah Wilson',
        'user_email': 'sarah@example.com',
        'rating': 4,
        'comment': 'Great movie with stunning visuals. The plot can be confusing at times.',
        'created_at': '2024-01-14 15:45:00'
    },
    {
        'id': 3,
        'movie_id': 2,
        'user_name': 'Mike Chen',
        'user_email': 'mike@example.com',
        'rating': 5,
        'comment': 'Heath Ledger\'s Joker is legendary. Best superhero movie ever!',
        'created_at': '2024-01-13 09:00:00'
    },
    {
        'id': 4,
        'movie_id': 3,
        'user_name': 'Emily Brown',
        'user_email': 'emily@example.com',
        'rating': 5,
        'comment': 'Cried my eyes out. The father-daughter relationship is beautiful.',
        'created_at': '2024-01-12 20:15:00'
    }
]

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def get_movie_by_id(movie_id):
    """
    Get movie by ID
    MySQL: SELECT * FROM movies WHERE id = %s
    """
    for movie in movies:
        if movie['id'] == movie_id:
            return movie
    return None

def get_movie_feedbacks(movie_id):
    """
    Get all feedbacks for a movie
    MySQL: SELECT * FROM feedbacks WHERE movie_id = %s ORDER BY created_at DESC
    """
    return [f for f in feedbacks if f['movie_id'] == movie_id]

def calculate_average_rating(movie_id):
    """
    Calculate average rating for a movie
    MySQL: SELECT AVG(rating) FROM feedbacks WHERE movie_id = %s
    """
    movie_feedbacks = get_movie_feedbacks(movie_id)
    if not movie_feedbacks:
        return 0
    total = sum(f['rating'] for f in movie_feedbacks)
    return round(total / len(movie_feedbacks), 1)
def get_review_count(movie_id):
    """
    Get review count for a movie
    MySQL: SELECT COUNT(*) FROM feedbacks WHERE movie_id = %s
    """
    return len(get_movie_feedbacks(movie_id))

def get_total_reviews():
    """
    Get total reviews across all movies
    MySQL: SELECT COUNT(*) FROM feedbacks
    """
    return len(feedbacks)

def get_overall_average_rating():
    """
    Get overall average rating
    MySQL: SELECT AVG(rating) FROM feedbacks
    """
    if not feedbacks:
        return 0
    total = sum(f['rating'] for f in feedbacks)
    return round(total / len(feedbacks), 1)

def get_rating_distribution():
    """
    Get rating distribution
    MySQL: SELECT rating, COUNT(*) as count FROM feedbacks GROUP BY rating
    """
    distribution = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
    for f in feedbacks:
        distribution[f['rating']] += 1
    return distribution

def add_feedback(movie_id, user_name, user_email, rating, comment):
    """
    Add new feedback
    MySQL: INSERT INTO feedbacks (movie_id, user_name, user_email, rating, comment) VALUES (...)
    """
    new_feedback = {
        'id': len(feedbacks) + 1,
        'movie_id': movie_id,
        'user_name': user_name,
        'user_email': user_email,
        'rating': rating,
        'comment': comment,
        'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    feedbacks.append(new_feedback)
    return new_feedback

# =============================================================================
# ROUTES
# =============================================================================

@app.route('/')
def home():
    """
    Home page - Display all movies
    EC2 URL: http://your-ec2-public-ip:5000/
    """
    movies_with_ratings = []
    for movie in movies:
        movie_data = movie.copy()
        movie_data['avg_rating'] = calculate_average_rating(movie['id'])
        movie_data['review_count'] = get_review_count(movie['id'])
        movies_with_ratings.append(movie_data)
    
    return render_template('index.html', 
                         movies=movies_with_ratings,
                         total_reviews=get_total_reviews(),
                         overall_avg=get_overall_average_rating())

@app.route('/movie/<int:movie_id>')
def movie_detail(movie_id):
    """
    Movie detail page with feedback form
    EC2 URL: http://your-ec2-public-ip:5000/movie/1
    """
    movie = get_movie_by_id(movie_id)
    if not movie:
        flash('Movie not found!', 'error')
        return redirect(url_for('home'))
    
    movie_feedbacks = get_movie_feedbacks(movie_id)
    avg_rating = calculate_average_rating(movie_id)
    review_count = get_review_count(movie_id)
    
    return render_template('movie_detail.html',
                         movie=movie,
                         feedbacks=movie_feedbacks,
                         avg_rating=avg_rating,
                         review_count=review_count,
                         total_reviews=get_total_reviews())

@app.route('/submit_feedback', methods=['POST'])
def submit_feedback():
    """
    Handle feedback submission
    MySQL: INSERT INTO feedbacks (movie_id, user_name, user_email, rating, comment) VALUES (...)
    """
    movie_id = int(request.form.get('movie_id'))
    user_name = request.form.get('user_name', '').strip()
    user_email = request.form.get('user_email', '').strip()
    rating = int(request.form.get('rating', 0))
    comment = request.form.get('comment', '').strip()
    
    # Validation
    if not all([user_name, user_email, rating, comment]):
        flash('Please fill in all fields!', 'error')
        return redirect(url_for('movie_detail', movie_id=movie_id))
    
    if rating < 1 or rating > 5:
        flash('Invalid rating!', 'error')
        return redirect(url_for('movie_detail', movie_id=movie_id))
    
    # Add feedback
    new_feedback = add_feedback(movie_id, user_name, user_email, rating, comment)
    
    # Get movie for thank you page
    movie = get_movie_by_id(movie_id)
    
    return render_template('thank_you.html',
                         movie=movie,
                         feedback=new_feedback,
                         total_reviews=get_total_reviews())

@app.route('/analytics')
def analytics():
    """
    Analytics dashboard
    EC2 URL: http://your-ec2-public-ip:5000/analytics
    """
    # Get movie ratings
    movies_with_ratings = []
    for movie in movies:
        movie_data = movie.copy()
        movie_data['avg_rating'] = calculate_average_rating(movie['id'])
        movie_data['review_count'] = get_review_count(movie['id'])
        movies_with_ratings.append(movie_data)
    
    # Sort by rating
    movies_with_ratings.sort(key=lambda x: x['avg_rating'], reverse=True)
    
    # Get recent reviews
    recent_feedbacks = sorted(feedbacks, key=lambda x: x['created_at'], reverse=True)[:10]
    for feedback in recent_feedbacks:
        feedback['movie'] = get_movie_by_id(feedback['movie_id'])
    
    return render_template('analytics.html',
                         movies=movies_with_ratings,
                         rating_distribution=get_rating_distribution(),
                         recent_feedbacks=recent_feedbacks,
                         total_reviews=get_total_reviews(),
                         overall_avg=get_overall_average_rating())

@app.route('/api/stats')
def api_stats():
    """
    API endpoint for real-time stats (AJAX updates)
    """
    return jsonify({
        'total_reviews': get_total_reviews(),
        'overall_avg': get_overall_average_rating(),
        'movie_count': len(movies)
    })

# =============================================================================
# ERROR HANDLERS
# =============================================================================

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', error='Page not found'), 404

@app.errorhandler(500)
def internal_error(e):
    return render_template('error.html', error='Internal server error'), 500

# =============================================================================
# MAIN ENTRY POINT
# =============================================================================
# 
# LOCAL DEVELOPMENT:
#   python app.py
#   Access: http://127.0.0.1:5000
#
# EC2 PRODUCTION DEPLOYMENT:
#   gunicorn -w 4 -b 0.0.0.0:5000 app:app
#   Or with nginx reverse proxy on port 80
#
# =============================================================================
if __name__ == '__main__':
    # Development server
    # Set debug=False in production!
    app.run(host='0.0.0.0', port=5000, debug=True)
