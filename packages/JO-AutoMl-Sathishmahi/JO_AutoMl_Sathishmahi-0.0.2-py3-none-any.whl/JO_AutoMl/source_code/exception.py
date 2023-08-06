import sys


class CustomException(Exception):
    def __init__(self, sys):

        self.exception_type, exception_object, exception_traceback = sys.exc_info()
        self.filename = exception_traceback.tb_frame.f_code.co_filename
        self.line_number = exception_traceback.tb_lineno

        super().__init__(
            f"LINE NUMBER OF ERROR ===>  [{self.line_number}] FILE NAME OF ERROR OCCURRED ===>  [{self.filename}]  EXCEPTION TYPE  ===>  [{self.exception_type}]"
        )
