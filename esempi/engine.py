"for running these via key board one chars hortcuts write a while loop that prints the input"
import sys

def _read_char():
    """Read a single character (cross-platform)."""
    try:
        import msvcrt
        return msvcrt.getwch()  # Windows
    except ImportError:
        import tty, termios
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
            if ch == '\x1b': # arrow keys
                ch += sys.stdin.read(2)
            return ch
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)

def run_key_loop():
    print("Press keys (press 'q' to quit).")
    while True:
        c = _read_char()
        print("Got:", repr(c))
        if c == 'q':
            break

if __name__ == "__main__":
    run_key_loop()

    
    