from flask import Flask, jsonify, request

app = Flask(__name__)

# Simulated data
class Event:
    def __init__(self, id, title):
        self.id = id
        self.title = title

    def to_dict(self):
        return {"id": self.id, "title": self.title}

# In-memory "database"
events = [
    Event(1, "Tech Meetup"),
    Event(2, "Python Workshop")
]



def find_event(event_id):
    for ev in events:
        if ev.id == event_id:
            return ev
    return None  



@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Welcome to the Events API"}), 200



@app.route("/events", methods=["GET"])
def get_events():
    return jsonify([ev.to_dict() for ev in events]), 200



@app.route("/events", methods=["POST"])
def create_event():
    
    data = request.get_json(silent=True)

   
    if not data or not data.get("title"):
        return jsonify({"error": "Title is required"}), 400

   
    new_id = max((ev.id for ev in events), default=0) + 1

    new_event = Event(new_id, data["title"])
    events.append(new_event)

    return jsonify(new_event.to_dict()), 201  



@app.route("/events/<int:event_id>", methods=["PATCH"])
def update_event(event_id):
    event = find_event(event_id)
    if event is None:
        return jsonify({"error": "Event not found"}), 404

    data = request.get_json(silent=True)
    if not data or not data.get("title"):
        return jsonify({"error": "Title is required"}), 400

    event.title = data["title"]  
    return jsonify(event.to_dict()), 200



@app.route("/events/<int:event_id>", methods=["DELETE"])
def delete_event(event_id):
    event = find_event(event_id)
    if event is None:
        return jsonify({"error": "Event not found"}), 404

    events.remove(event)
    return "", 204 


if __name__ == "__main__":
    app.run(debug=True)