# utils/timer.py

import threading
import time

# -------------------------
# Countdown Timer Class
# -------------------------
class CountdownTimer:
    """
    Countdown timer runs in a background thread.
    Can trigger update_callback every second and finish_callback when time is up.
    """

    def __init__(self, seconds=20, update_callback=None, finish_callback=None):
        """
        seconds: duration of timer
        update_callback: called every second with remaining time
        finish_callback: called when timer ends
        """
        self.seconds = seconds
        self.remaining = seconds
        self.update_callback = update_callback
        self.finish_callback = finish_callback
        self._running = False
        self._thread = None

    def _run(self):
        """Internal thread function"""
        self.remaining = self.seconds
        while self._running and self.remaining > 0:
            time.sleep(1)
            self.remaining -= 1
            if self.update_callback:
                self.update_callback(self.remaining)
        if self._running and self.finish_callback:
            self.finish_callback()
        self._running = False

    def start(self):
        """Start the countdown timer"""
        if not self._running:
            self._running = True
            self._thread = threading.Thread(target=self._run, daemon=True)
            self._thread.start()

    def stop(self):
        """Stop the timer"""
        self._running = False

    def reset(self, seconds=None):
        """Reset timer with optional new duration"""
        self.stop()
        if seconds is not None:
            self.seconds = seconds
        self.remaining = self.seconds

# -------------------------
# Helper functions for app_ui.py
# -------------------------
_timers = {}

def start_timer(seconds, label_widget, on_timer_end):
    """
    Start a countdown timer and bind it to a label widget
    Returns a unique timer ID for later stopping or resetting
    """
    def update_label(remaining):
        label_widget.config(text=f"Time Left: {remaining} sec")

    timer_obj = CountdownTimer(
        seconds=seconds,
        update_callback=update_label,
        finish_callback=on_timer_end
    )
    timer_obj.start()

    # Generate unique ID for this timer object
    timer_id = id(timer_obj)
    _timers[timer_id] = timer_obj
    return timer_id

def stop_timer(timer_id):
    """Stop timer by its ID"""
    if timer_id in _timers:
        _timers[timer_id].stop()
        del _timers[timer_id]

def reset_timer(timer_id, seconds=None):
    """Reset timer by its ID, optionally with new duration"""
    if timer_id in _timers:
        _timers[timer_id].reset(seconds)

# -------------------------
# Example usage
# -------------------------
if __name__ == "__main__":
    import tkinter as tk

    def on_tick(remaining):
        label.config(text=f"Time Left: {remaining}s")

    def on_finish():
        print("Timer finished!")

    root = tk.Tk()
    root.geometry("300x100")
    label = tk.Label(root, text="Time Left: 10s", font=("Helvetica", 14))
    label.pack(pady=20)

    # Start 10-second timer
    tid = start_timer(10, label, on_finish)

    root.mainloop()
