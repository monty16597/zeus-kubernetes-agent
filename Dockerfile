FROM python:3.8
WORKDIR /opt/app
ENV APP_ENV=production
COPY . .
RUN make init
EXPOSE 8000
CMD make run