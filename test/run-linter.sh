# Build images
cd ..
docker-compose -f docker-compose.yml build scripts
docker-compose -f docker-compose.yml -f docker-compose.test.yml build test-scripts test-lint-python

# Run linter on all files
docker run --rm mobydq-test-lint-python pylint scripts test
