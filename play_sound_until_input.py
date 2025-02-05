import threading
import time
import os
import subprocess
from pydub import AudioSegment
from pydub.playback import play

def play_sound_until_input(path_to_sound_file):
    """
    Play a sound in a loop until the user provides input.
    Returns the user's input as a string.
    """
    # Suppress ffmpeg output
    # Store the original stderr setting
    null_device = open(os.devnull, 'w')
    old_stderr = os.dup(2)
    os.dup2(null_device.fileno(), 2)
    
    def play_sound_loop():
        sound = AudioSegment.from_wav(path_to_sound_file)
        while not stop_event.is_set():
            play(sound)
            time.sleep(1)

    def get_user_input(prompt):
        user_input = input(prompt)
        stop_event.set()
        return user_input

    stop_event = threading.Event()
    sound_thread = threading.Thread(target=play_sound_loop)
    sound_thread.start()

    try:
        user_input = get_user_input("Please enter input until sound stops: ")
    finally:
        # Restore stderr
        os.dup2(old_stderr, 2)
        null_device.close()
        
    sound_thread.join()
    return user_input


if __name__ == "__main__":
    # Example usage
    user_input = play_sound_until_input('/home/scubamut1/Downloads/ring2.wav')
    print(f"User input: {user_input}")

# chtools/ch_utils/play_sound_until_input.py
# import os
# import time
# import platform
# import subprocess
# import logging
# import sys

# def play_sound_until_input(sound_file: str = "complete.wav"):
#     """
#     Plays a sound file repeatedly until the user presses Enter.
#     Args:
#         sound_file: The name of the sound file to play (default "complete.wav")
#     """
#     logging.info(f"Starting to play sound file {sound_file} until enter is pressed")
#     try:
#         while True:
#             if platform.system() == "Darwin":  # macOS
#                 subprocess.run(["afplay", sound_file], check=True)
#             elif platform.system() == "Windows":
#                 try:
#                     import winsound
#                     winsound.PlaySound(sound_file, winsound.SND_FILENAME)
#                 except ImportError:
#                     logging.warning("winsound module not available, cannot play sound")
#             elif platform.system() == "Linux":  # Linux
#                 subprocess.run(["aplay", sound_file], check=True)
#             else:
#                 logging.warning(f"Unsupported platform: {platform.system()}, cannot play sound")
            
#             if not sys.stdin.isatty(): # if not interactive exit loop
#                 return

#             if os.name == 'nt': # on windows we need to catch any exception
#                  import msvcrt
#                  if msvcrt.kbhit():
#                     if msvcrt.getch() == b'\r': # if they press return then exit loop
#                        return
#             else:
#                  # Check for input without blocking using select
#                  import select
#                  if select.select([sys.stdin], [], [], 0)[0]:
#                      if sys.stdin.readline() == '\n':  # Check for empty return
#                         return
            
#             time.sleep(0.1)
#     except Exception as e:
#         logging.error(f"Error playing sound: {e}")
#     logging.info("Sound player ended")
