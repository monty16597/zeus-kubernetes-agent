FROM python:3.8
WORKDIR /opt/app
ENV APP_ENV=production
COPY requirements.txt Makefile .
RUN make init
COPY . .
EXPOSE 8000
CMD make run