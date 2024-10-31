from PyQt5.QtCore import QObject, QThread, pyqtSlot
import queue
from datetime import datetime
from fatsia_growth.utils.logger import logger
import json  # For serializing results
import os  # For handling file paths


class ResultsLogger(QObject):
    """
    A QObject-based logger that runs in a separate QThread.
    It processes results from a queue and writes them to a log file with timestamps.
    """

    def __init__(
        self,
        config=None,
    ):
        """
        Initializes the ResultsLogger.

        :param config: Optional configuration dictionary.
                       Can include settings like log directory, file naming conventions, etc.
        """
        super().__init__()

        self.config = config
        self._running = False

        # Initialize the queue as an instance variable
        self.results_queue = queue.Queue(maxsize=10)

        # Set up the QThread
        self.thread = QThread()
        self.moveToThread(self.thread)
        self.thread.started.connect(self._results_log_thread)

    def _results_log_thread(self):
        """
        The main loop that runs in the separate thread.
        It continuously processes results from the queue and writes them to the log file.
        """
        logger.info("Results logger thread started.")
        self._running = True

        # Create a log file with creation datetime
        current_datetime = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_filename = f"results_{current_datetime}.log"

        # Determine log directory from config or use current directory
        log_directory = self.config.get("log_directory", ".") if self.config else "."
        log_filepath = os.path.join(log_directory, log_filename)

        # Ensure the log directory exists
        os.makedirs(log_directory, exist_ok=True)

        try:
            with open(log_filepath, 'a', encoding='utf-8') as log_file:
                logger.info(f"Logging results to file: {log_filepath}")

                while self._running:
                    try:
                        # Attempt to get a result from the queue with a timeout
                        result = self.results_queue.get(timeout=1)  # Wait for 1 second

                        # Get current timestamp
                        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                        # Serialize the result to JSON if it's a dict, else convert to string
                        if isinstance(result, dict):
                            result_str = json.dumps(result)
                        else:
                            result_str = str(result)

                        # Write the result with timestamp to the log file
                        log_entry = f"[{timestamp}] {result_str}\n"
                        log_file.write(log_entry)
                        log_file.flush()  # Ensure it's written to disk

                        logger.debug(f"Logged result: {log_entry.strip()}")

                        # Mark the task as done
                        self.results_queue.task_done()

                    except queue.Empty:
                        # No result received in the last second; continue the loop
                        continue
                    except Exception as e:
                        # Log any unexpected exceptions and continue
                        logger.error(f"Error writing result to log file: {e}")

        except Exception as e:
            logger.error(f"Failed to open log file {log_filepath}: {e}")

        logger.info("Results logger thread stopping.")


    def start(self):
        """
        Starts the logging thread.
        """
        if not self.thread.isRunning():
            self.thread.start()
            logger.info("Results logger thread started.")

    def stop(self):
        """
        Stops the logging thread gracefully.
        Waits until all pending results are processed.
        """
        self._running = False
        if self.thread.isRunning():
            self.thread.quit()
            self.thread.wait()
            logger.info("Results logger thread stopped.")

    # def __del__(self):
    #     """
    #     Ensures that the thread is stopped when the object is deleted.
    #     """
    #     self.stop()
