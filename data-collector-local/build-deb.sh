#!/bin/bash
set -euo pipefail

# Variables
PACKAGE_NAME="data-collector-local"
VERSION="1.0.0"
ARCH="all"
DOCKER_IMAGE="debian:bullseye"

# Create build directory
BUILD_DIR="$(mktemp -d)"
echo "Building in $BUILD_DIR"

# Copy debian directory to build location
mkdir -p "$BUILD_DIR/debian/DEBIAN"
cp -r debian/* "$BUILD_DIR/debian/"
chmod 755 "$BUILD_DIR/debian/DEBIAN/postinst"

# Create Dockerfile
cat > "$BUILD_DIR/Dockerfile" <<EOF
FROM $DOCKER_IMAGE
RUN apt-get update && apt-get install -y dpkg-dev
COPY . /build
WORKDIR /build
RUN dpkg-deb --build debian ${PACKAGE_NAME}_${VERSION}_${ARCH}.deb
EOF

# Build package in Docker
docker build -t deb-builder "$BUILD_DIR"
docker run --rm -v "$(pwd):/output" deb-builder \
    sh -c "cp /build/${PACKAGE_NAME}_${VERSION}_${ARCH}.deb /output"

# Clean up
rm -rf "$BUILD_DIR"

echo "Package built: ${PACKAGE_NAME}_${VERSION}_${ARCH}.deb"
