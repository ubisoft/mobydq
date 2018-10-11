# Build images
docker-compose -f docker-compose.yml build api scripts
docker-compose -f ./test/docker-compose.yml build

# Run test on all files
docker-compose -f ./test/docker-compose.yml up test-db test-api test-scripts
