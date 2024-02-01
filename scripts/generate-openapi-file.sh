#!/bin/bash
# Hook ID: generate-openapi-file
echo "Generating OpenAPI file."


# Define the name of the service you want to check
SERVICE_NAME="backend"

# Check if the service container is running using docker-compose
if docker compose ps --services --filter "status=running" | grep "$SERVICE_NAME"; then
    echo "Backend service container is running."
    # Create openapi.json file
    RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8080/generate-openapi)
    if [ "$RESPONSE" -eq 200 ]; then
        cd js-client
        npm install
        npm run generate-client
        tsc .
        echo "Client generated."
        exit 0
    else
        echo "Error: Service is up, but HTTP Status is not 200. Status: $RESPONSE"
        exit 1
    fi
else
    echo "Error: $SERVICE_NAME service container is not running."
    exit 1
fi

exit 0