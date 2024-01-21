ARG PORT=443
FROM cypress/browsers:latest
RUN apt-get install python3 -y
run echo $(python3 -m site --user-base)
COPY requirements.txt .
ENV PATH /home/root/.local/bin:${PATH}
run apt-get update && apt-get install -y python3-pip && pip install -r requirements.txt
COPY . .
CMD gunicorn main:app --host 0.0.0.0 --port ${PORT}