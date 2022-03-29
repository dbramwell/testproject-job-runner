FROM python:3.10

COPY runner.py /runner.py
RUN pip install requests

ENTRYPOINT [ "python", "/runner.py" ]