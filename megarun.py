docker-compose down --remove-orphans && ./bootstrap.py && docker-compose up -d && docker-compose run autogentoo-builder /bin/bash
