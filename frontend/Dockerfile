FROM node:22-alpine

WORKDIR /app
COPY package*.json ./

RUN npm install -g npm@11.4.2
RUN npm -v
RUN npm install

COPY . .

RUN npm run build