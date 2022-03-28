from prometheus_client import Counter, Enum, Gauge, Info, Summary


info = Info(name="app", documentation="Information about the application")
info.info({"version": "1.0", "language": "python", "framework": "django"})

requests_total = Counter(
    name="app_requests_total",
    documentation="Total number of various requests.",
    labelnames=["endpoint", "method", "user"],
)
last_user_activity_time = Gauge(
    name="app_last_user_activity_time_seconds",
    documentation="The last time when user was active.",
    labelnames=["user"],
)
coupon_create_last_status = Enum(
    name="app_coupon_create_last_status",
    documentation="Status of last coupon create endpoint call.",
    labelnames=["user"],
    states=["success", "error"],
)
coupon_create_time = Summary(
    name="app_coupon_create_time_seconds", documentation="Time of creating coupon."
)
