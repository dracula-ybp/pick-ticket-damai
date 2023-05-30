
import logging
import tkinter as tk


class TkinterTextHandler(logging.Handler):
    """Custom logging handler that writes log messages to a Tkinter Text widget"""

    def __init__(self, text_widget):
        super().__init__()
        self.text_widget = text_widget

    def emit(self, record):
        # Get the log message and append it to the widget
        msg = self.format(record)
        self.text_widget.insert(tk.END, msg + "\n")
        # Scroll to the bottom of the widget
        self.text_widget.see(tk.END)


class App(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)

        self.example_frame = tk.Frame(master)
        self.example_frame.pack(expand=True, fill='both')

        self.log_text = tk.Text(self.example_frame)
        self.log_text.pack(expand=True, fill='both')

        # Create a custom logger
        logger = logging.getLogger("myapp")
        logger.setLevel(logging.DEBUG)

        # Create a formatter
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

        # Create a StreamHandler and set the formatter
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)

        # Create a TkinterTextHandler and set the formatter
        tkinter_handler = TkinterTextHandler(self.log_text)
        tkinter_handler.setFormatter(formatter)

        # Add the handlers to the logger
        logger.addHandler(stream_handler)
        logger.addHandler(tkinter_handler)

        # Log some messages
        logger.debug("This is a debug message")
        logger.info("This is an info message")
        logger.warning("This is a warning message")
        logger.error("This is an error message")
        logger.critical("This is a critical message")


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    app.mainloop()
