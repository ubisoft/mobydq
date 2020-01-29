# Build images
cd ..
docker-compose -f docker-compose.yml -f docker-compose.test.yml build

# Run test on all backend modules
docker-compose -f docker-compose.yml -f docker-compose.test.yml up test-db test-scripts
