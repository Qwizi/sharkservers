# Stage 1: Install Rust, build dependencies, and prepare the build environment
FROM python:3.11.3 AS builder

ARG TARGETPLATFORM
ENV CARGO_HOME=/usr/local/cargo
ENV RUSTUP_HOME=/usr/local/rustup

# Install Rust and its dependencies based on the platform
RUN if [ "$TARGETPLATFORM" = "linux/arm/v8" ]; then \
        apt-get update && apt-get install -y curl build-essential libssl-dev libffi-dev python3-dev pkg-config; \
        curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y --default-toolchain stable --target aarch64-unknown-linux-gnu; \
    fi

# Set up the working directory

ENV PATH="/usr/local/cargo/bin:${PATH}"

WORKDIR /code


# Install or upgrade pip and Poetry
RUN pip install --upgrade pip && pip install --no-cache-dir --upgrade poetry

# Disable Poetry virtualenv creation
RUN poetry config installer.max-workers 10
RUN poetry config virtualenvs.create false
#RUN poetry config installer.no-binary cryptography

# Copy the project files for dependency installation
COPY ./pyproject.toml ./poetry.lock /code/

# Install project dependencies using Poetry
RUN poetry install --no-interaction --no-ansi

# Stage 2: Runtime environment
FROM builder AS runtime
ENV PYTHONUNBUFFERED 1

# Create a dedicated user for running the application
RUN addgroup --system fastapi && adduser --system --ingroup fastapi fastapiuser

# Set the working directory
WORKDIR /app

# Copy only the necessary files from the build stage
COPY --from=builder /code /app

# Copy the source code
COPY . /app/

# Change ownership to the dedicated user
RUN chown -R fastapiuser:fastapi /app

# Set the PORT environment variable (customize as needed)
ENV PORT 80

# Switch to the dedicated user
USER fastapiuser