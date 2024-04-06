FROM node:20 as frontend-stage
WORKDIR /app
COPY ./frontend/ .
RUN yarn install
RUN yarn run build
# RUN cp -r dist/spa/icons dist/spa/assets/icons
# RUN cp dist/spa/favicon.ico dist/spa/assets/favicon.ico

FROM python:3.11-slim
ARG VERSION
ENV VERSION=$VERSION
WORKDIR /app

COPY ./backend/requirements.txt /app/requirements.txt
RUN pip3 install -U pip
RUN pip3 install -r requirements.txt

COPY ./backend/ /app
COPY --from=frontend-stage /app/dist /app/templates
WORKDIR /app

RUN mkdir -p /var/log/mdm/
RUN chmod +x /app/init.sh
EXPOSE 8000

CMD ["/app/init.sh"]