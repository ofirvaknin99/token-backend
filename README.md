# Tree Of Files Fullstack Assignment - Token Security

This project is the backend implementation of the Tree of Files Fullstack Assignment.
It provides an HTTP API to fetch the structure of files and directories from a public GitHub repository.

## Features

- **Single Endpoint**: `/fetch-repo-tree` (POST) accepts a GitHub repository URL and returns the directory tree structure.
- **GitHub API Integration**: Fetches repository data using the GitHub API, building the directory structure recursively.
- **Validation**: Validates GitHub URLs using Pydantic and regex.
- **CORS Support**: Allows cross-origin requests for frontend integration.
- **Token Authentication**: Uses a GitHub token for API authentication (stored in `.env`).

---

## Requirements

- Python 3.9+
- GitHub Personal Access Token (for API requests)

### Libraries Used

- **FastAPI**: For building the HTTP server.
- **Pydantic**: For request validation.
- **requests**: For making HTTP requests to the GitHub API.
- **python-dotenv**: For loading environment variables.
- **uvicorn**: For running the FastAPI application.

---

## API Endpoints

### `POST /fetch-repo-tree`

**Request Body**:

```json
{
  "url": "https://github.com/<owner>/<repository>"
}
```

**Response Example**:

```json
{
  "name": "repository-name",
  "type": "dir",
  "children": [
    {
      "name": "file1.txt",
      "type": "file",
      "path": "file1.txt"
    },
    {
      "name": "subdirectory",
      "type": "dir",
      "children": [
        {
          "name": "file2.txt",
          "type": "file",
          "path": "subdirectory/file2.txt"
        }
      ]
    }
  ]
}
```
