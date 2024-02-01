#!/bin/bash
# Hook ID: generate-js-client
echo "Generating JS client..."

cd js-client

# Generate the client
npm run generate-client

exit 0  # To allow the commit