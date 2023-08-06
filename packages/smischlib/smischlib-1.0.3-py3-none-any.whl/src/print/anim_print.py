import time,sys

def animated_print(text, delay=0.05):
    for character in text:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(delay)
    print()