import sys
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def error_message_details(error, error_detail: sys):
    _, _, exc_tb = error_detail.exc_info()
    file_name = exc_tb.tb_frame.f_code.co_filename
    line_number = exc_tb.tb_lineno
    error_message = (
        f"Error occurred in Python script: [{file_name}], "
        f"line number: [{line_number}], error message: [{error}]"
    )
    return error_message

class CustomError(Exception):
    def __init__(self, error, error_detail: sys):
        self.error_message = error_message_details(error, error_detail)
        super().__init__(self.error_message)

    def __str__(self):
        return self.error_message
