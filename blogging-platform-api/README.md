# Blogging Platform API

Python sample solution for the Blogging Platform API challenge from roadmap.sh.

This project is a FastAPI-based Blogging Platform API that provides secure CRUD operations for managing blog posts. The API supports creating, reading, updating, and deleting blog posts with rich metadata including categories, tags, and timestamps. It also includes fuzzy database searching to help users find posts efficiently and comprehensive error handling for a reliable experience.

## Features

- **Create Blog Posts:** Add new blog posts with title, content, category, and tags.
- **Read Blog Posts:** Retrieve all blog posts or fetch a specific blog post by ID.
- **Update Blog Posts:** Modify existing blog posts with new content, categories, or tags.
- **Delete Blog Posts:** Remove blog posts from the database.
- **Search Functionality:** Perform fuzzy database searching to find blog posts by search terms.
- **Tag Support:** Organize posts with multiple tags for better categorization.
- **Timestamp Tracking:** Automatically track creation and update timestamps for each post.
- **Error Handling:** Comprehensive error handling with appropriate HTTP status codes.

## Technologies Used

- **FastAPI:** Modern Python web framework for building APIs.
- **SQLite:** Lightweight database for storing blog posts and metadata.
- **Pydantic:** Data validation and serialization for request/response models.
- **Python 3.10+:** Latest Python version for modern language features.

## API Usage

### Base URL

The API is hosted locally at: `http://localhost:8000`

### Endpoints

#### Create a Blog Post

```bash
curl -X POST "http://localhost:8000/posts" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "My First Blog Post",
    "content": "This is the content of my first blog post.",
    "category": "Technology",
    "tags": ["Tech", "Programming"]
  }'
```

**Request Body:**

- `title` (required, string): The title of the blog post.
- `content` (required, string): The main content of the blog post.
- `category` (required, string): The category of the blog post.
- `tags` (required, array of strings): Tags associated with the blog post.

**Response:** Returns `201 Created` with the newly created blog post.

#### Get All Blog Posts

```bash
curl "http://localhost:8000/posts"
```

**Query Parameters:**

- `search_query` (optional, string): Filter posts by search term.

**Response:** Returns `200 OK` with a list of all blog posts.

#### Get a Specific Blog Post

```bash
curl "http://localhost:8000/posts/1"
```

**Path Parameters:**

- `post_id` (required, integer): The ID of the blog post to retrieve.

**Response:** Returns `200 OK` with the requested blog post, or `404 Not Found` if the post doesn't exist.

#### Update a Blog Post

```bash
curl -X PUT "http://localhost:8000/posts/1" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "My Updated Blog Post",
    "content": "This is the updated content.",
    "category": "Technology",
    "tags": ["Tech", "Updates"]
  }'
```

**Path Parameters:**

- `post_id` (required, integer): The ID of the blog post to update.

**Request Body:** Same as Create Blog Post.

**Response:** Returns `200 OK` with the updated blog post, or `404 Not Found` if the post doesn't exist.

#### Delete a Blog Post

```bash
curl -X DELETE "http://localhost:8000/posts/1"
```

**Path Parameters:**

- `post_id` (required, integer): The ID of the blog post to delete.

**Response:** Returns `204 No Content` on success, or `404 Not Found` if the post doesn't exist.

### Response Example

```json
{
  "id": 1,
  "title": "My First Blog Post",
  "content": "This is the content of my first blog post.",
  "category": "Technology",
  "tags": ["Tech", "Programming"],
  "created_at": "2026-06-19T10:30:00Z",
  "updated_at": "2026-06-19T10:30:00Z"
}
```

## Installation

### Prerequisites

- Python 3.10+

### Steps

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/yourusername/blogging-platform-api.git
   cd blogging-platform-api
   ```

2. **Set Up Virtual Environment:**

   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install Dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the App:**

   ```bash
   uvicorn main:app --reload
   ```

5. **Access the API:**
   - Base URL: `http://localhost:8000`
   - Interactive API Documentation: `http://localhost:8000/docs`
   - Alternative API Documentation: `http://localhost:8000/redoc`

## Project Structure

```
blogging-platform-api/
├── main.py              # FastAPI app initialization and health check endpoint
├── api.py               # API route definitions (endpoints)
├── models.py            # Pydantic data models for request/response validation
├── services.py          # Business logic and database operations
├── utils.py             # Utility functions for timestamps and data formatting
├── test_db.py           # Database testing utilities
├── requirements.txt     # Project dependencies
└── blog.db              # SQLite database (created automatically)
```

## Error Handling

The API includes error handling for the following scenarios:

- **404 Not Found:** Returned when a blog post with the specified ID doesn't exist.
- **400 Bad Request:** Returned when the request body contains invalid data or missing required fields.
- **500 Internal Server Error:** Returned for unexpected server errors.

## Database

The application uses SQLite (`blog.db`) to store blog posts. The database is automatically initialized on first run with the necessary table structure. Each blog post record includes:

- `id`: Unique identifier (auto-incremented)
- `title`: Post title
- `content`: Post content
- `category`: Post category
- `tags`: Comma-separated string of tags
- `created_at`: ISO 8601 timestamp of creation
- `updated_at`: ISO 8601 timestamp of last update

<!-- ## Future Enhancements

Potential improvements to the project could include:

- User authentication and authorization
- Comments and discussion on blog posts
- Pagination for large datasets
- Advanced filtering and sorting options
- Database migrations with Alembic
- Unit and integration tests
- Deployment to cloud platforms (AWS, Azure, etc.) -->
