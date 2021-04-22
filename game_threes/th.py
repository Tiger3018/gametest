import threading
from threading import Thread, Lock

lockTriggerMove = threading.Lock()
lockDisplay = threading.Lock()