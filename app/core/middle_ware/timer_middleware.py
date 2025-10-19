from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
import time

class TimerMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, logger=None):  # <== thêm logger ở đây
        super().__init__(app)
        self.logger = logger

    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        if self.logger:
            self.logger.info(f"Request took {process_time:.4f} seconds")
        else:
            print(f"Request took {process_time:.4f} seconds")
        return response
