# Build images
docker-compose -f docker-compose.yml build scripts
docker-compose -f ./test/docker-compose.yml build test-scripts
docker-compose -f ./test/docker-compose.yml build test-lint-python

# Run linter on all files
docker run --rm mobydq-lint-python pylint scripts test api/api.py api/proxy api/health api/security
