FROM python:3.6 as python-base
COPY requirements.txt .
COPY templates/index.html .
COPY b.py .
RUN pip install -r requirements.txt

FROM python:3.6-alpine
COPY --from=python-base /root/.cache /root/.cache
COPY --from=python-base requirements.txt .
COPY --from=python-base index.html templates/
COPY --from=python-base b.py .
RUN pip install -r requirements.txt
ENTRYPOINT ["python3"]
CMD ["b.py"]

