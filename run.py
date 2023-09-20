"""Stair Challenge Flask App."""
from app import app, socketio

if __name__ == "__main__":
    socketio.run(app, debug=True, use_reloader=False, host="0.0.0.0")
