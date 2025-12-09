# Book Catalogue - IS211 Course Project

## Project Overview

This is a web application built with Flask that allows users to maintain a personal catalogue of books. Users can search for books by ISBN using the Google Books API, view their book collection, and delete books from their catalogue.

## Features Implemented

### Core Features
1. **User Authentication**: Users can log in to access their personal book collection
2. **ISBN Search**: Search for books using ISBN through the Google Books API
3. **Book Display**: View saved books with title, author, page count, and average rating
4. **Book Deletion**: Remove books from the collection
5. **Error Handling**: Comprehensive error handling for API requests and user inputs

### Extra Credit Features
1. **Multiple Users Support**: The application supports multiple user accounts with separate book collections
2. **Thumbnail Display**: Book cover thumbnails are fetched from the Google Books API and displayed
3. **User-specific Collections**: Each user has their own private book collection

## Database Schema

The application uses SQLite with two main tables:

### Users Table
- `id`: Primary key (INTEGER, AUTO INCREMENT)
- `username`: Unique username (TEXT, NOT NULL, UNIQUE)
- `password`: User password (TEXT, NOT NULL) - *Note: stored in plaintext for educational purposes*

### Books Table
- `id`: Primary key (INTEGER, AUTO INCREMENT)
- `user_id`: Foreign key referencing users table (INTEGER, NOT NULL)
- `isbn`: Book ISBN number (TEXT, NOT NULL)
- `title`: Book title (TEXT, NOT NULL)
- `author`: Book author(s) (TEXT, NOT NULL)
- `page_count`: Number of pages (INTEGER, DEFAULT 0)
- `average_rating`: Average rating from Google Books (REAL, DEFAULT 0.0)
- `thumbnail`: URL to book cover image (TEXT)
- `created_at`: Timestamp of when book was added (TIMESTAMP, DEFAULT CURRENT_TIMESTAMP)

## How It Works

### Application Flow

1. **Login**: Users are greeted with a login page. Three test accounts are pre-configured in the database
2. **Main Dashboard**: After login, users see their book collection (initially empty)
3. **Adding Books**: Users enter an ISBN in the search form
4. **API Integration**: The application queries the Google Books API with the provided ISBN
5. **Data Processing**: Book information (title, author, page count, rating, thumbnail) is extracted from the JSON response
6. **Database Storage**: The book details are saved to the SQLite database with the user's ID
7. **Display**: The book appears in the user's collection with thumbnail and all details
8. **Deletion**: Users can delete books with a confirmation dialog

### Technical Implementation

- **Flask Framework**: Handles routing, sessions, and template rendering
- **SQLite Database**: Stores user and book data persistently
- **Google Books API**: Provides book metadata based on ISBN
- **Session Management**: Maintains user login state
- **Template Inheritance**: Uses Jinja2 templates with a base layout
- **CSS Styling**: Responsive design with modern UI

### Error Handling

The application includes robust error handling for:
- Invalid or non-existent ISBNs
- API connection failures
- Missing book data in API responses
- Unauthorized access attempts
- Database errors

## Installation & Setup

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Installation Steps

1. **Clone or download the project files**

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python app.py
   ```

4. **Access the application**:
   - Open your web browser
   - Navigate to `http://127.0.0.1:5000/`

### Test Credentials

The application comes with three pre-configured test accounts:
- **Username**: `admin` | **Password**: `admin123`
- **Username**: `user1` | **Password**: `password1`
- **Username**: `user2` | **Password**: `password2`

## Project Structure

```
book-catalogue/
├── app.py              # Main Flask application
├── schema.sql          # Database schema
├── requirements.txt    # Python dependencies
├── README.md          # Project documentation
├── books.db           # SQLite database (created on first run)
├── static/
│   └── style.css      # CSS stylesheet
└── templates/
    ├── base.html      # Base template with navbar and layout
    ├── login.html     # Login page
    └── index.html     # Main dashboard page
```

## API Usage Example

The application uses the Google Books API to fetch book information. Example URL:
```
https://www.googleapis.com/books/v1/volumes?q=isbn:9781449372620
```

The API returns JSON data containing book metadata, from which we extract:
- Title
- Author(s)
- Page count
- Average rating
- Thumbnail image URL

## Security Considerations

**Important Note**: This application stores passwords in plaintext, which is NOT recommended for production use. In a real-world application, passwords should be hashed using libraries like `bcrypt` or `werkzeug.security`.

## Future Enhancements

Potential improvements for the application:
- Password hashing for secure authentication
- User registration functionality
- Search by title feature
- Multiple result selection when API returns multiple books
- Book categories/tags
- Export functionality (CSV, PDF)
- Book notes/reviews
- Reading status tracking

## Technologies Used

- **Python 3**: Programming language
- **Flask 2.3.0**: Web framework
- **SQLite**: Database
- **Requests 2.31.0**: HTTP library for API calls
- **Google Books API**: External book data source
- **HTML5/CSS3**: Frontend markup and styling
- **Jinja2**: Template engine

## Author

Created as part of the IS211 Course Project

## License

Educational project - free to use and modify
