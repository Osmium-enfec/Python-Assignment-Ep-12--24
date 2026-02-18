FROM python:3.14-slim

WORKDIR /app

# Copy assignment files
COPY starter_code.py /app/starter_code.py
COPY solution.py /app/solution.py
COPY test_assignment.py /app/test_assignment.py
COPY runner_flow.sh /app/runner.sh
COPY generate_results.py /app/generate_results.py

# Install test dependencies
RUN pip install --no-cache-dir pytest requests && chmod +x /app/runner.sh

# Expose port for HTTP server
EXPOSE 8000

# Default command
CMD ["/app/runner.sh"]
