# Building My Personal Blog with FastAPI

Alright so for this project I built a personal blog that renders all its content from the server. Essentially, I'm rendering HTML directly from FastAPI instead of building an API. Pretty cool stuff!

## What I Built

**Guest Section (Public):**

- Homepage with a list of all articles
- Individual article pages where you can read the full content

**Admin Section (Protected):**

- Dashboard where I can see all articles
- Add new articles
- Edit existing articles
- Delete articles
- All of this requires authentication

## The Tech Stack

Here's what I used:

- **FastAPI** - the web framework 
- **Uvicorn** - the ASGI server that runs FastAPI
- **Jinja2** - templating engine for rendering HTML
- **Pydantic** - for data validation (comes with FastAPI)
- **starlette** - for session management (also comes with FastAPI)...that's actually kinda new to me 

```bash
pip install fastapi uvicorn jinja2 pydantic
```

## Project Structure

```
personal-blog/
├── templates/          # HTML files with Jinja2
│   ├── base.html
│   ├── home.html
│   ├── article.html
│   ├── login.html
│   ├── dashboard.html
│   ├── add_article.html
│   └── edit_article.html
├── static/             # CSS and other static files,
│   └── style.css
├── content/            # Where articles are stored as JSON
│   └── articles.json
├── main.py             # FastAPI app with all routes
├── auth.py             # Authentication helpers
├── models.py           # Pydantic models
├── utils.py            # CRUD operations for articles
└── requirements.txt    # Dependencies
```

## How Authentication Works (The Simple Version)

Okay so here's the thing - I kept authentication **really simple** for this project. No JWT, no database, no password hashing. Just basic session-based auth with hardcoded credentials.

### Why Not JWT?

JWT (JSON Web Tokens) is great for APIs and microservices, but for this project it would be overkill. JWT is stateless, which means:

- More complex to implement
- Need to handle token expiration
- Need to sign and verify tokens
- Overkill for a simple personal blog

### Why Session-Based Auth?

Sessions are simpler and perfect for a traditional server-rendered app:

- The server keeps track of logged-in users
- Just set a flag in the session when someone logs in
- Check that flag on protected routes
- Done!

### How Sessions Work

1. When you visit the site, the server creates a **session** for you (basically a cookie with a random ID)
2. The server stores data associated with that session ID
3. When you login successfully, the server sets `session["authenticated"] = True`
4. On every request to a protected route, we check if that flag is `True`
5. When you logout, we clear the session

The session data is stored in a signed cookie, so the user can't tamper with it. Starlette (which FastAPI uses under the hood) handles all of this with the `SessionMiddleware`.

### The Hardcoded Admin

In `auth.py`, I have:

```python
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "password123"
```

Yeah, I know - hardcoded credentials are a no-no for production. But for this project:

- It's a learning project, not a real production app
- Keeps things simple to understand
- Easy to change later if needed

In a real app, you'd:

- Store credentials in environment variables
- Hash passwords with something like `passlib` or `bcrypt`
- Maybe use a database for multiple users

But for now? Simple works.

## The Routes (Endpoints)

Here's how everything flows:

### Public Routes

| Route           | Method | What It Does                     |
| --------------- | ------ | -------------------------------- |
| `/`             | GET    | Shows homepage with all articles |
| `/article/{id}` | GET    | Shows a single article           |

### Auth Routes

| Route     | Method | What It Does                     |
| --------- | ------ | -------------------------------- |
| `/login`  | GET    | Shows login form                 |
| `/login`  | POST   | Checks credentials, sets session |
| `/logout` | GET    | Clears session, redirects home   |

### Admin Routes (Protected)

| Route                        | Method | What It Does                                |
| ---------------------------- | ------ | ------------------------------------------- |
| `/dashboard`                 | GET    | Shows all articles with edit/delete buttons |
| `/admin/article/new`         | GET    | Shows "add article" form                    |
| `/admin/article/new`         | POST   | Saves new article                           |
| `/admin/article/{id}/edit`   | GET    | Shows edit form with current data           |
| `/admin/article/{id}/edit`   | POST   | Updates article                             |
| `/admin/article/{id}/delete` | POST   | Deletes article                             |

## How The Flow Works

### Reading Articles (Public)

1. User visits homepage (`/`)
2. Server loads all articles from `content/articles.json`
3. Renders `home.html` with the article list
4. User clicks an article
5. Server loads that specific article
6. Renders `article.html` with full content

### Admin Login

1. User visits `/login`
2. Sees a simple form (username + password)
3. Submits the form
4. Server checks if credentials match `admin` / `password123`
5. If correct: sets `request.session["authenticated"] = True`
6. Redirects to dashboard
7. If wrong: shows error message

### Dashboard (Protected)

1. User visits `/dashboard`
2. Server checks `request.session.get("authenticated")`
3. If not authenticated → redirect to `/login`
4. If authenticated → load articles and show dashboard
5. Dashboard has Add/Edit/Delete buttons for each article

### Adding an Article

1. Click "Add Article" on dashboard
2. Fill out form (ID, title, content, author)
3. Submit form
4. Server creates a new `Article` object with current timestamp
5. Saves to `articles.json`
6. Redirects back to dashboard

### Editing an Article

1. Click "Edit" on an article in dashboard
2. Form loads with current article data
3. Make changes
4. Submit form
5. Server updates the article with new `updated_at` timestamp
6. Saves to `articles.json`
7. Redirects back to dashboard

### Deleting an Article

1. Click "Delete" on an article
2. JavaScript confirms you really want to delete
3. Server removes article from `articles.json`
4. Redirects back to dashboard

## Storage: JSON Files

Instead of a database, I'm using a simple JSON file (`content/articles.json`). Each article looks like:

```json
{
  "id": "my-first-post",
  "title": "Welcome to My Blog",
  "content": "This is my first article...",
  "author": "Jaimz",
  "created_at": "2026-03-24T10:00:00",
  "updated_at": "2026-03-24T10:00:00"
}
```

The `utils.py` file has helper functions:

- `_load_articles()` - reads the JSON file
- `_save_articles()` - writes to the JSON file
- `get_all_articles()` - returns all articles as Pydantic models
- `get_article_by_id()` - finds one article
- `create_article()` - adds a new one
- `update_article()` - updates an existing one
- `delete_article()` - removes one

Super simple, no database needed for this scale.

## Templates: Jinja2

All HTML is in the `templates/` folder. I'm using template inheritance:

- `base.html` - has the navbar, footer, and common structure
- All other templates extend `base.html` and just fill in the content

Example:

```html
{% extends "base.html" %} {% block title %}Home - My Blog{% endblock %} {% block
content %}
<h1>Welcome!</h1>
<!-- more content -->
{% endblock %}
```

The navbar in `base.html` checks if you're logged in:

```html
{% if request.session.get("authenticated") %}
<a href="/dashboard">Dashboard</a>
<a href="/logout">Logout</a>
{% else %}
<a href="/login">Admin Login</a>
{% endif %}
```

## CSS: Minimalist Black & White

Went with a clean, minimalist design:

- Black and white color scheme
- Simple typography
- Clean cards for articles
- Responsive layout

All in `static/style.css` - no frameworks, just plain CSS.

## What I Learned

1. **Server-side rendering** - How to render HTML directly from the server (old school but effective)
2. **Session management** - How sessions work and why they're useful for simple auth
3. **Jinja2 templating** - Template inheritance, loops, conditionals
4. **Form handling** - GET for showing forms, POST for submitting
5. **File-based storage** - When you can skip the database
6. **CRUD operations** - Create, Read, Update, Delete with JSON

## What Could Be Better (Future Improvements)

If I wanted to take this further:

- Add password hashing with `passlib`
- Use environment variables for credentials
- Add Markdown support for article content
- Add categories/tags for articles
- Add a search feature
- Move to a real database (SQLite, PostgreSQL)
- Add image uploads
- Add comments on articles

But for now, this is a solid foundation. It works, it's clean, and I learned a ton building it!

---

**Credentials to test:**

- Username: `admin`
- Password: `password123`

Go check it out at `http://127.0.0.1:8000` 🚀
