FROM node:20-slim AS build

WORKDIR /app
COPY app/package.json app/pnpm-lock.yaml* ./
RUN npm install -g pnpm && pnpm install

COPY app/ ./
RUN pnpm build

FROM caddy:2.7-alpine

RUN apk add --no-cache curl
COPY Caddyfile /etc/caddy/Caddyfile
COPY --from=build /app/dist /srv
