FROM node:18.12.1

WORKDIR /app
COPY kin-frontend/package.json .
RUN npm install

COPY kin-frontend .

CMD npm start
