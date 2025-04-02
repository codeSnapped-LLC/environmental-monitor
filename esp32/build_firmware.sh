#!/bin/bash
set -euo pipefail

# Get semantic version
VERSION=$(dotnet-gitversion | jq -r '.SemVer')

# Update firmware version in main.py
sed -i "s/FIRMWARE_VERSION = .*/FIRMWARE_VERSION = \"${VERSION}\"/" main.py

# Build package filename
FILENAME="environmental-monitor-firmware_${VERSION}.bin"

echo "Building firmware version ${VERSION}"
echo "Output file: ${FILENAME}"

# Here you would add your actual build commands for MicroPython
# For example:
# mpremote cp main.py :
# mpremote cp sensors.py :
# mpremote reset

# For this example, just create a dummy file
touch "${FILENAME}"

echo "Build complete!"
