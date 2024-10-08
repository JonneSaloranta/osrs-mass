ARG PYTHON_VERSION=3.10.11
FROM python:${PYTHON_VERSION}-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory to /srv/app
WORKDIR /srv/app

# Copy project files to /srv/app
COPY . .

RUN apt-get update && apt-get upgrade -y && apt-get install -y gcc

# Add non-privileged user
ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN python -m pip install --no-cache-dir -r requirements.txt

# Ensure correct permissions and create necessary directories
RUN mkdir -p /srv/app/static /srv/app/staticfiles && chown -R appuser:appuser /srv/app/static /srv/app/staticfiles

# Switch to non-privileged user
USER appuser

# Collect static files
# RUN python manage.py collectstatic --noinput

EXPOSE 8000

# TODO: update to use gunicorn someday

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
