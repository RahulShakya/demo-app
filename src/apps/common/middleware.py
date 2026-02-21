import logging
import time

logger = logging.getLogger("request")


class StructuredRequestLogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start = time.monotonic()
        response = self.get_response(request)
        duration_ms = int((time.monotonic() - start) * 1000)
        logger.info(
            "request_processed",
            extra={
                "method": request.method,
                "path": request.path,
                "status_code": response.status_code,
                "duration_ms": duration_ms,
                "tenant": getattr(getattr(request, "tenant", None), "schema_name", "public"),
            },
        )
        return response
