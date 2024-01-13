import os
current_directory = os.path.dirname(os.path.abspath(__file__))
os.makedirs(os.path.join(current_directory,"models","funasr"),exist_ok=True)
os.makedirs(os.path.join(current_directory,"models","whisper_model"),exist_ok=True)