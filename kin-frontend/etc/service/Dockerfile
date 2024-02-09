# Build stage
FROM node:18.12.1 as build

WORKDIR /app

COPY etc/service/env/build-env /etc/kin-frontend/env/build-env
COPY scripts/set-envs-for-build.sh scripts/set-envs-for-build.sh
RUN chmod +x scripts/set-envs-for-build.sh
RUN ./scripts/set-envs-for-build.sh

COPY kin-frontend/package.json .
RUN npm install

COPY kin-frontend .
RUN npm run build

# Serve stage
FROM nginx:alpine
COPY --from=build /app/build /usr/share/nginx/html

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
