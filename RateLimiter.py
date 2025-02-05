# import time
# from datetime import datetime, timedelta
# from collections import deque

# # logger = chtools.ch_utils.setup_logging()

# class RateLimiter:
#     def __init__(self, max_requests=590, time_window=300, 
#                  time_sleep=0.1, min_time_per_req=0.5):

#         self.max_requests = max_requests
#         self.time_window = time_window
#         self.requests = deque()
#         self.request_count = 0
#         self.total_wait_time = 0
#         self.wait_count = 0
#         self.min_time_per_req = min_time_per_req  # New attribute for min_time
#         self.time_sleep = time_sleep  # New attribute for time_sleep

#     def can_make_request(self):
#         now = datetime.utcnow()
#         while self.requests and self.requests[0] < now - timedelta(seconds=self.time_window):
#             self.requests.popleft()
#         if len(self.requests) < self.max_requests:
#             self.requests.append(now)
#             return True
#         return False

#     def wait_if_needed(self):
#         start_wait = time.time()
#         while not self.can_make_request():
#             time.sleep(self.time_sleep)
#         end_wait = time.time()
#         wait_time = end_wait - start_wait
        
#         self.total_wait_time += wait_time
#         if wait_time > 0:
#             self.wait_count += 1
#         self.request_count += 1
#         return len(self.requests)

# def main(max_requests=590, time_window=300, min_time_per_req=0.5, time_sleep=0.1):
#     #limiter = RateLimiter(max_requests=600, time_window=300, min_time_per_req=min_time_per_req
#         limiter = RateLimiter(max_requests, time_window, min_time_per_req)
#         start_time = time.time()
#         previous_time = start_time
#         total_requests = 0

#         num_requests = 20
#         for i in range(num_requests):
#             count = limiter.wait_if_needed()
#             total_requests += 1
#             current_time = time.time()
#             time_diff = current_time - previous_time

#             if time_diff >= 1:
#                 requests_per_sec = limiter.request_count / time_diff
#                 avg_wait_time = limiter.total_wait_time / limiter.wait_count if limiter.wait_count > 0 else 0
#                 print(f"Request {i+1}: Allowed, Requests in window: {count}, Requests per sec: {requests_per_sec:.2f} (total req: {total_requests}), Avg. Wait time: {avg_wait_time:.4f} s")
#                 limiter.request_count = 0
#                 limiter.total_wait_time = 0
#                 limiter.wait_count = 0
#                 previous_time = current_time
#             else:
#                 print(f"Request {i+1}: Allowed, Requests in window: {count}, (total req: {total_requests})")
#             time.sleep(limiter.min_time_per_req)


#         end_time = time.time()
#         total_time = end_time - start_time

#         print(f"\nTotal time to make all requests: {total_time:.4f} seconds")

# if __name__ == "__main__":
#         # Example Usage
#         # To minimize total time, use this
#         # limiter = RateLimiter(max_requests=600, time_window=300, min_time_per_req=0.1)
#         # To achieve around 2 req/sec use this
#         # limiter = RateLimiter(max_requests=600, time_window=300, min_time_per_req=0.1)
#         # To maximize time:
#         #limiter = RateLimiter(max_requests=2, time_window=5, min_time_per_req=0.5)
#         max_requests=590
#         time_window=300
#         min_time_per_req = 0.1
#         time_sleep = 0.1
#         main(max_requests, time_window, min_time_per_req, time_sleep)    

# chtools/ch_basics/rate_limiter.py
import time
from datetime import datetime, timedelta
from collections import deque
import logging

class RateLimiter:
    """
    A class to manage rate limiting for the Companies House API.
    """
    def __init__(self, max_requests: int, time_window: int, logger: logging.Logger, min_time_per_req: float = 0.1, time_sleep:float = 0.1):
        """
        Initializes the rate limiter.

        Args:
            max_requests: The maximum number of requests in a time window.
            time_window: The window time in seconds.
            logger: the logger to log events.
             min_time_per_req: The minimum time that should elapse between requests. Default is 0.1.
            time_sleep: The time that the class should sleep while waiting to make requests. Default is 0.1.

        """
        self.max_requests = max_requests
        self.time_window = time_window
        self.requests = deque()
        self.logger = logger
        self.min_time_per_req = min_time_per_req
        self.time_sleep = time_sleep
        self.logger.debug(f"RateLimiter initialized with max_requests={max_requests}, time_window={time_window}")

    def can_make_request(self) -> bool:
        """Check if a request can be made based on rate limit."""
        now = datetime.utcnow()
        while self.requests and self.requests[0] < now - timedelta(seconds=self.time_window):
            self.requests.popleft() # remove old request times
        if len(self.requests) < self.max_requests:
            self.requests.append(now)  # Record request time
            return True
        return False

    def wait_if_needed(self) -> int:
        """Wait if needed before allowing a new request."""
        start_wait = time.time()
        while not self.can_make_request():
            time.sleep(self.time_sleep) # wait until a request can be made
        end_wait = time.time()
        wait_time = end_wait - start_wait
        if wait_time > 0:
          self.logger.info(f"Waiting for rate limit: {wait_time:.2f} seconds") # log if we have to wait
        return len(self.requests) # return the number of requests