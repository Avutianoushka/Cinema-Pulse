-- =============================================================================
-- CINEMAPULSE - AWS RDS MySQL Database Setup
-- =============================================================================
-- 
-- USAGE:
-- 1. Connect to your RDS MySQL instance:
--    mysql -h your-rds-endpoint.rds.amazonaws.com -u admin -p
-- 2. Run this script:
--    source setup_rds.sql
-- =============================================================================

-- Create database
CREATE DATABASE IF NOT EXISTS cinemapulse;
USE cinemapulse;

-- =============================================================================
-- MOVIES TABLE
-- =============================================================================
CREATE TABLE IF NOT EXISTS movies (
    id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    image_url VARCHAR(500),
    director VARCHAR(255),
    duration VARCHAR(50),
    year INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_title (title),
    INDEX idx_year (year)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =============================================================================
-- GENRES TABLE
-- =============================================================================
CREATE TABLE IF NOT EXISTS genres (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL UNIQUE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =============================================================================
-- MOVIE_GENRES TABLE (Many-to-Many Relationship)
-- =============================================================================
CREATE TABLE IF NOT EXISTS movie_genres (
    movie_id INT NOT NULL,
    genre_id INT NOT NULL,
    PRIMARY KEY (movie_id, genre_id),
    FOREIGN KEY (movie_id) REFERENCES movies(id) ON DELETE CASCADE,
    FOREIGN KEY (genre_id) REFERENCES genres(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =============================================================================
-- FEEDBACKS TABLE
-- =============================================================================
CREATE TABLE IF NOT EXISTS feedbacks (
    id INT PRIMARY KEY AUTO_INCREMENT,
    movie_id INT NOT NULL,
    user_name VARCHAR(255) NOT NULL,
    user_email VARCHAR(255) NOT NULL,
    rating INT NOT NULL,
    comment TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (movie_id) REFERENCES movies(id) ON DELETE CASCADE,
    INDEX idx_movie_id (movie_id),
    INDEX idx_rating (rating),
    INDEX idx_created_at (created_at),
    CONSTRAINT chk_rating CHECK (rating >= 1 AND rating <= 5)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =============================================================================
-- INSERT SAMPLE DATA
-- =============================================================================

-- Insert Genres
INSERT INTO genres (name) VALUES 
    ('Sci-Fi'), ('Action'), ('Thriller'), ('Crime'), 
    ('Drama'), ('Adventure'), ('Comedy')
ON DUPLICATE KEY UPDATE name=name;

-- Insert Movies
INSERT INTO movies (id, title, description, image_url, director, duration, year) VALUES
(1, 'Inception', 'A thief who steals corporate secrets through dream-sharing technology is given the inverse task of planting an idea into the mind of a C.E.O. Christopher Nolan''s mind-bending masterpiece explores the depths of human consciousness.', 'https://images.unsplash.com/photo-1536440136628-849c177e76a1?w=800', 'Christopher Nolan', '2h 28min', 2010),
(2, 'The Dark Knight', 'When the menace known as the Joker wreaks havoc and chaos on Gotham, Batman must accept one of the greatest psychological and physical tests of his ability to fight injustice.', 'https://images.unsplash.com/photo-1509347528160-9a9e33742cdb?w=800', 'Christopher Nolan', '2h 32min', 2008),
(3, 'Interstellar', 'A team of explorers travel through a wormhole in space in an attempt to ensure humanity''s survival. A visually stunning journey through space and time.', 'https://images.unsplash.com/photo-1419242902214-272b3f66ee7a?w=800', 'Christopher Nolan', '2h 49min', 2014),
(4, 'Pulp Fiction', 'The lives of two mob hitmen, a boxer, a gangster and his wife, and a pair of diner bandits intertwine in four tales of violence and redemption.', 'https://images.unsplash.com/photo-1594909122845-11baa439b7bf?w=800', 'Quentin Tarantino', '2h 34min', 1994),
(5, 'The Matrix', 'A computer programmer discovers that reality as he knows it is a simulation created by machines, and joins a rebellion to overthrow them.', 'https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?w=800', 'The Wachowskis', '2h 16min', 1999),
(6, 'Parasite', 'Greed and class discrimination threaten the newly formed symbiotic relationship between the wealthy Park family and the destitute Kim clan.', 'https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?w=800', 'Bong Joon-ho', '2h 12min', 2019)
ON DUPLICATE KEY UPDATE title=VALUES(title);

-- Link Movies to Genres
INSERT INTO movie_genres (movie_id, genre_id) VALUES
(1, 1), (1, 2), (1, 3),  -- Inception: Sci-Fi, Action, Thriller
(2, 2), (2, 4), (2, 5),  -- Dark Knight: Action, Crime, Drama
(3, 1), (3, 6), (3, 5),  -- Interstellar: Sci-Fi, Adventure, Drama
(4, 4), (4, 5),          -- Pulp Fiction: Crime, Drama
(5, 1), (5, 2),          -- Matrix: Sci-Fi, Action
(6, 3), (6, 5), (6, 7)   -- Parasite: Thriller, Drama, Comedy
ON DUPLICATE KEY UPDATE movie_id=movie_id;

-- Insert Sample Feedbacks
INSERT INTO feedbacks (movie_id, user_name, user_email, rating, comment) VALUES
(1, 'John Doe', 'john@example.com', 5, 'Absolutely mind-blowing! Nolan has outdone himself with this masterpiece.'),
(1, 'Sarah Wilson', 'sarah@example.com', 4, 'Great movie with stunning visuals. The plot can be confusing at times.'),
(2, 'Mike Chen', 'mike@example.com', 5, 'Heath Ledger''s Joker is legendary. Best superhero movie ever!'),
(3, 'Emily Brown', 'emily@example.com', 5, 'Cried my eyes out. The father-daughter relationship is beautiful.');

-- =============================================================================
-- USEFUL QUERIES
-- =============================================================================

-- Get movie with average rating
-- SELECT m.*, AVG(f.rating) as avg_rating, COUNT(f.id) as review_count
-- FROM movies m
-- LEFT JOIN feedbacks f ON m.id = f.movie_id
-- GROUP BY m.id;

-- Get rating distribution
-- SELECT rating, COUNT(*) as count FROM feedbacks GROUP BY rating ORDER BY rating DESC;

-- Get recent feedbacks with movie info
-- SELECT f.*, m.title as movie_title
-- FROM feedbacks f
-- JOIN movies m ON f.movie_id = m.id
-- ORDER BY f.created_at DESC
-- LIMIT 10;

-- =============================================================================
-- VERIFICATION
-- =============================================================================
SELECT 'Database setup complete!' as status;
SELECT COUNT(*) as movie_count FROM movies;
SELECT COUNT(*) as feedback_count FROM feedbacks;
SELECT COUNT(*) as genre_count FROM genres;
