# Events API: Full CRUD RESTful API with Flask

## Purpose

A small RESTful API for managing a list of events, built with Python and Flask. It supports creating, reading, updating, and deleting events (full CRUD). Data is stored **in memory** as a list of `Event` objects, so it resets every time the server restarts. A real database comes later.

## Setup

```bash
git clone <repo-url>
cd crud-app-flask
pipenv install
pipenv shell
python app.py
```

Or with pip:

```bash
pip install flask pytest
python app.py
```

The server runs at `http://localhost:5000`.

## Running the tests

```bash
pytest -v
```

## Data model

Each event has two fields:

| Field | Type | Description |
|---|---|---|
| `id` | integer | Assigned by the server (highest existing id + 1) |
| `title` | string | Provided by the client |

## Routes

| Method | Route | Description | Success status |
|---|---|---|---|
| GET | `/` | Welcome message | `200 OK` |
| GET | `/events` | List all events | `200 OK` |
| POST | `/events` | Create a new event | `201 Created` |
| PATCH | `/events/<id>` | Update an event's title | `200 OK` |
| DELETE | `/events/<id>` | Remove an event | `204 No Content` |

### Error responses

| Status | When | Body |
|---|---|---|
| `400 Bad Request` | POST or PATCH body is missing or has no `title` | `{"error": "Title is required"}` |
| `404 Not Found` | PATCH or DELETE with an id that does not exist | `{"error": "Event not found"}` |

## Example requests and responses

### GET `/`

**Response** `200 OK`
```json
{"message": "Welcome to the Events API"}
```

### GET `/events`

**Response** `200 OK`
```json
[
  {"id": 1, "title": "Tech Meetup"},
  {"id": 2, "title": "Python Workshop"}
]
```

### POST `/events`

**Request body**
```json
{"title": "Hackathon"}
```

**Response** `201 Created`
```json
{"id": 3, "title": "Hackathon"}
```

**Missing title** `400 Bad Request`
```json
{"error": "Title is required"}
```

### PATCH `/events/1`

**Request body**
```json
{"title": "Hackathon 2025"}
```

**Response** `200 OK`
```json
{"id": 1, "title": "Hackathon 2025"}
```

**Unknown id** (`PATCH /events/99`) `404 Not Found`
```json
{"error": "Event not found"}
```

### DELETE `/events/2`

**Response** `204 No Content` (empty body)

**Unknown id** (`DELETE /events/99`) `404 Not Found`
```json
{"error": "Event not found"}
```

## Testing with curl

```bash
curl http://localhost:5000/events
curl -X POST http://localhost:5000/events -H "Content-Type: application/json" -d '{"title": "Hackathon"}'
curl -X PATCH http://localhost:5000/events/1 -H "Content-Type: application/json" -d '{"title": "Hackathon 2025"}'
curl -X DELETE http://localhost:5000/events/2
```

On Windows PowerShell, use `curl.exe` and escape the inner quotes, or use Postman.

## Design notes

- **Helper function:** `find_event(event_id)` looks up an event by id, so PATCH and DELETE share one lookup instead of repeating the same loop.
- **ID generation:** new ids use the highest existing id plus one, rather than `len(events) + 1`, which would produce duplicate ids after a delete.
- **Input validation:** `request.get_json(silent=True)` returns `None` instead of crashing on a missing or invalid body, and the routes respond with a clear `400` message.
- **Scaling:** everything lives in `app.py` for now. As the API grows, routes, models, and data access should move into separate modules, and the in-memory list should be replaced by a database.