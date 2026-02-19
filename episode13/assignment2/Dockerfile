FROM python:3.14-slim

WORKDIR /app

# Copy assignment files
COPY starter_code.py /app/starter_code.py
COPY solution.py /app/solution.py
COPY test_assignment.py /app/test_assignment.py
COPY stores.py /app/stores.py
COPY page.py /app/page.py
COPY runner_flow.sh /app/runner_flow.sh

# Install test dependencies
RUN pip install --no-cache-dir pytest requests && chmod +x /app/runner_flow.sh

# Expose port for HTTP server
EXPOSE 8005

# Default command
CMD ["/app/runner_flow.sh"]
