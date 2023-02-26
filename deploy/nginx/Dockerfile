FROM registry.gitlab.com/atnartur.uni/discipline-program-automation/app:latest AS app
FROM nginx:1.21-alpine

RUN rm -rf /etc/nginx/conf.d
COPY deploy/nginx/host.conf /etc/nginx/conf.d/default.conf
COPY --from=app /app/static /app/static

