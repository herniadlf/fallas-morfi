FROM python:2


EXPOSE 5000

COPY . .
RUN pip install http://www.antlr3.org/download/Python/antlr_python_runtime-3.1.3.tar.gz
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "-m", "flask", "run", "--host=0.0.0.0"]