from prometheus_client import Counter, Enum, Gauge, Info, Summary


info = Info("app", "Information about the application")
info.info({"version": "1.0", "language": "python", "framework": "django"})

requests_total = Counter(
    "app_requests_total", "Total number of various requests.", ["endpoint", "method", "user"]
)
last_user_activity_time = Gauge(
    "app_last_user_activity_time_seconds", "The last time when user was active.", ["user"]
)
coupon_create_last_status = Enum(
    "app_coupon_create_last_status",
    "Status of last coupon create endpoint call.",
    ["user"],
    states=["success", "error"],
)
coupon_create_time = Summary("app_coupon_create_time_seconds", "Time of creating coupon.")
