# Performance Tests

This directory contains performance tests for the Talemo platform. Performance tests evaluate the system's responsiveness, stability, and resource usage under various conditions.

## Overview

Performance testing is crucial for ensuring that the Talemo platform can handle the expected load and provide a good user experience. These tests help identify bottlenecks, verify scalability, and ensure the application meets performance requirements.

## Directory Structure

The performance tests are organized by test type and target component:

```
performance/
├── locust/                # Locust load testing scripts
│   ├── locustfile.py      # Main Locust configuration
│   ├── stories.py         # Story-related load tests
│   ├── agents.py          # Agent-related load tests
│   └── assets.py          # Asset-related load tests
├── benchmarks/            # Benchmark tests for specific components
│   ├── database.py        # Database performance benchmarks
│   ├── api.py             # API performance benchmarks
│   └── agent_processing.py # Agent processing benchmarks
└── monitoring/            # Performance monitoring scripts
    ├── resource_usage.py  # Resource usage monitoring
    └── response_times.py  # Response time monitoring
```

## Test Framework

The performance tests primarily use [Locust](https://locust.io/), a Python-based load testing tool. Locust allows you to define user behavior in code and run distributed load tests to simulate thousands of users.

## Types of Performance Tests

### Load Testing

Load tests simulate multiple users accessing the application simultaneously to verify that the system can handle the expected load.

Example Locust script for testing the stories API:

```python
# locust/stories.py
from locust import HttpUser, task, between

class StoryUser(HttpUser):
    wait_time = between(1, 5)  # Wait 1-5 seconds between tasks
    
    def on_start(self):
        # Log in before running tasks
        self.client.post("/accounts/login/", {
            "username": "testuser",
            "password": "testpassword"
        })
    
    @task(3)
    def view_stories(self):
        # Browse stories (weight: 3)
        self.client.get("/api/v1/stories/")
    
    @task(1)
    def view_story_detail(self):
        # View story detail (weight: 1)
        # In a real test, you would use a story ID from a list
        self.client.get("/api/v1/stories/1/")
    
    @task(1)
    def create_story(self):
        # Create a new story (weight: 1)
        self.client.post("/api/v1/stories/", json={
            "prompt": "A story about a curious cat",
            "age_range": "4-8"
        })
```

### Stress Testing

Stress tests push the system beyond its normal operating capacity to identify breaking points and failure modes.

Example stress test configuration:

```python
# locust/stress_test.py
from locust import HttpUser, task, between
import random

class StressTestUser(HttpUser):
    wait_time = between(0.1, 1)  # Very short wait times
    
    @task
    def random_request(self):
        # Make random requests to various endpoints
        endpoints = [
            "/api/v1/stories/",
            "/api/v1/agents/",
            "/api/v1/assets/",
            "/stories/",
            "/agents/playground/"
        ]
        self.client.get(random.choice(endpoints))
```

### Endurance Testing

Endurance tests run for extended periods to identify issues that might only appear after prolonged use, such as memory leaks.

### Benchmark Testing

Benchmark tests measure the performance of specific components or operations to establish baselines and track improvements or regressions.

Example benchmark test for database queries:

```python
# benchmarks/database.py
import time
import statistics
from django.db import connection
from talemo.stories.models import Story

def benchmark_story_query():
    """Benchmark story listing query performance."""
    query_times = []
    
    for _ in range(100):
        start_time = time.time()
        
        # Execute the query
        stories = list(Story.objects.all()[:100])
        
        end_time = time.time()
        query_times.append(end_time - start_time)
    
    # Calculate statistics
    avg_time = statistics.mean(query_times)
    median_time = statistics.median(query_times)
    p95_time = sorted(query_times)[int(len(query_times) * 0.95)]
    
    return {
        "average": avg_time,
        "median": median_time,
        "p95": p95_time,
        "min": min(query_times),
        "max": max(query_times)
    }
```

## Running Performance Tests

### Running Locust Tests

To run Locust tests:

```bash
# Start Locust with the specified locustfile
docker-compose -f docker/docker-compose.dev.yml exec web locust -f tests/performance/locust/locustfile.py

# Start Locust with a specific host
docker-compose -f docker/docker-compose.dev.yml exec web locust -f tests/performance/locust/locustfile.py --host=http://localhost:8000
```

Then open http://localhost:8089 in your browser to access the Locust web interface.

### Running Benchmark Tests

To run benchmark tests:

```bash
docker-compose -f docker/docker-compose.dev.yml exec web python -m tests.performance.benchmarks.database
```

## Performance Metrics

Key metrics to monitor during performance testing:

- **Response Time**: Time taken to respond to a request
- **Throughput**: Number of requests processed per second
- **Error Rate**: Percentage of requests that result in errors
- **CPU Usage**: CPU utilization during the test
- **Memory Usage**: Memory consumption during the test
- **Database Performance**: Query execution times and connection pool usage
- **Network I/O**: Network traffic generated by the application

## Best Practices

- **Define clear performance requirements**: Establish specific, measurable performance goals.
- **Test in an environment similar to production**: Use similar hardware and configuration.
- **Isolate tests**: Ensure other activities don't interfere with test results.
- **Monitor system resources**: Track CPU, memory, disk I/O, and network usage during tests.
- **Start with a baseline**: Establish baseline performance before making changes.
- **Test regularly**: Run performance tests regularly to catch regressions early.
- **Focus on realistic scenarios**: Test user journeys that reflect actual usage patterns.
- **Analyze results thoroughly**: Look beyond averages to percentiles and outliers.

## Related Documentation

- [Locust Documentation](https://docs.locust.io/)
- [Django Performance Optimization](https://docs.djangoproject.com/en/4.2/topics/performance/)
- [PostgreSQL Performance Tuning](https://www.postgresql.org/docs/current/performance-tips.html)
- [Web Performance Optimization](https://web.dev/fast/)