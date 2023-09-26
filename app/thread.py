"""Thread module for stair challenge app."""
import threading

sandglass_thread = None
thread_stop_event = threading.Event()
