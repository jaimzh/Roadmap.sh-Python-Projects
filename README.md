# Python Projects

A collection of Python and full-stack projects for learning and practice, all from [roadmap.sh](https://roadmap.sh).

> Note to self: deploy all these projects when you're done 

## Table of Contents

- [Expense Tracker](./expense-tracker)
- [Task Tracker CLI](./task-tracker-cli)
- [Unit Converter](./unit-converter)
- [GitHub Activity](./github-activity)
- [Personal Blog](./personal-blog)
- [Weather API](./weather-api)

## Projects

### [Expense Tracker](https://roadmap.sh/projects/expense-tracker)

A command-line expense management tool with budget tracking features.

- Track income and expenses
- Manage budgets
- Export to CSV

### [Task Tracker CLI](https://roadmap.sh/projects/task-tracker)

A CLI tool for managing tasks and to-do lists.

- Add, edit, and delete tasks
- Mark tasks as complete
- Store tasks in JSON format

### [Unit Converter](https://roadmap.sh/projects/unit-converter)

A full-stack unit converter application.

- **Backend**: FastAPI (Python)
- **Frontend**: React + Vite + TypeScript
- Convert between different units of measurement

### [GitHub Activity](https://roadmap.sh/projects/github-user-activity)

A simple GitHub activity tracker.

### [Personal Blog](https://roadmap.sh/projects/personal-blog)

A full-stack personal blogging platform with a minimalist UI.

- Admin dashboard and session-based authentication
- **Backend**: FastAPI (Python)
- **Frontend**: HTML5, CSS3, Jinja2

### [Weather API](https://roadmap.sh/projects/weather-api-wrapper-service)

A FastAPI-based Weather API that fetches weather data from the Visual Crossing Weather API.

- Implements caching with Redis to reduce external API calls
- Includes rate limiting and comprehensive logging
- **Backend**: FastAPI (Python)


## Getting Started

Each project has its own README with specific setup instructions. Generally:

**Python projects:**

```bash
cd <project-folder>
python main.py
```

**Unit Converter Frontend:**

```bash
cd unit-converter/frontend/unit-converter-fe
pnpm install
pnpm dev
```

**Unit Converter Backend:**

```bash
cd unit-converter/backend
python main.py
```

**Personal Blog:**

```bash
cd personal-blog
uvicorn main:app --reload
```

**Weather API:**

```bash
cd weather-api
uvicorn main:app --reload
```

## License

MIT
