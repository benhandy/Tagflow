# Need to add metrics collection
from prometheus_client import Counter, Histogram
import time

request_count = Counter('http_requests_total', 'Total HTTP requests')
request_latency = Histogram('http_request_duration_seconds', 'HTTP request latency') 