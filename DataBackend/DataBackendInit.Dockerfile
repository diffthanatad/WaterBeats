# Rust as the base image
FROM rust:1 as build

# Create a new empty shell project
RUN USER=root cargo new --bin data_backend
WORKDIR /data_backend

# Copy our manifests
COPY ./Cargo.lock ./Cargo.lock
COPY ./Cargo.toml ./Cargo.toml

# Build only the dependencies to cache them
RUN cargo build --release
RUN rm src/*.rs

# Copy the source code
COPY ./src ./src

# Build for release.
RUN rm ./target/release/deps/data_backend*
RUN cargo build --release

# The final base image, rust image is also base on debian:bullseye
FROM debian:bullseye-slim
RUN apt-get update
RUN apt-get install -y openssl ca-certificates
RUN update-ca-certificates
RUN apt-get install -y python3 python3-pip
RUN pip install --upgrade pip && pip install requests

# Copy from the previous build
COPY --from=build /data_backend/target/release/data_backend /bin/data_backend
WORKDIR /app/
# Run the binary
CMD ["data_backend"]