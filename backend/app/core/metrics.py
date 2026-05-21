from prometheus_client import Counter, Gauge, Histogram

HTTP_REQUESTS_TOTAL = Counter(
    "app_http_requests_total",
    "HTTP requests handled by the API",
    ["method", "path", "status"],
)

HTTP_REQUEST_DURATION_SECONDS = Histogram(
    "app_http_request_duration_seconds",
    "HTTP request latency in seconds",
    ["method", "path"],
)

JOBS_CREATED_TOTAL = Counter(
    "app_jobs_created_total",
    "Jobs created by each source",
    ["type", "source"],
)

JOBS_PROCESSED_TOTAL = Counter(
    "app_jobs_processed_total",
    "Jobs processed by the broker",
    ["type", "status"],
)

JOB_PROCESSING_DURATION_SECONDS = Histogram(
    "app_job_processing_duration_seconds",
    "Broker job processing latency in seconds",
    ["type", "status"],
)

JOBS_PENDING_GAUGE = Gauge(
    "app_jobs_pending",
    "Number of pending jobs currently visible to the broker",
)

SCRAPE_RUNS_TOTAL = Counter(
    "app_scrape_runs_total",
    "Scrape runs by source and outcome",
    ["source", "status"],
)

SCRAPE_DURATION_SECONDS = Histogram(
    "app_scrape_duration_seconds",
    "Scraper duration in seconds",
    ["source", "status"],
)