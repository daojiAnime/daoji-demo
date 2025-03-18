FROM registry.eu-west-1.aliyuncs.com/docker-clone/backend:4.0.0-base
COPY ./app /app/app
# 将 ARG 的值转换为 ENV
ARG VERSION
ENV VERSION=${VERSION:-"default_version"}

#ENTRYPOINT ["top", "-b"]
CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
