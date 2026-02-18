FROM python:3.14-slim
WORKDIR /app
COPY starter_code.py solution.py test_assignment.py stores.py page.py runner_flow.sh /app/
RUN pip install --no-cache-dir pytest requests && chmod +x /app/runner_flow.sh
EXPOSE 8005
ENTRYPOINT ["/bin/sh", "/app/runner_flow.sh"]
