#!/usr/bin/env python
"""
Test script for the monitoring setup.
This script generates test metrics and logs to verify that the monitoring stack is working correctly.
"""

import os
import sys
import time
import logging
import random
import argparse
from datetime import datetime

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('monitoring_test')

def test_statsd():
    """Test StatsD metrics collection."""
    try:
        from django_statsd.clients import statsd
        logger.info("Testing StatsD metrics collection...")
        
        # Generate random metrics
        for i in range(10):
            # Increment a counter
            statsd.incr('talemo.test.counter')
            logger.info(f"Incremented counter talemo.test.counter")
            
            # Record a timing
            timing = random.randint(10, 500)
            statsd.timing('talemo.test.timing', timing)
            logger.info(f"Recorded timing talemo.test.timing: {timing}ms")
            
            # Set a gauge
            gauge = random.randint(1, 100)
            statsd.gauge('talemo.test.gauge', gauge)
            logger.info(f"Set gauge talemo.test.gauge: {gauge}")
            
            time.sleep(1)
        
        logger.info("StatsD metrics test completed.")
        return True
    except Exception as e:
        logger.error(f"Error testing StatsD metrics: {e}")
        return False

def test_apm():
    """Test APM transaction and error collection."""
    try:
        from elasticapm.contrib.django.client import client
        logger.info("Testing APM transaction and error collection...")
        
        # Record custom transactions
        for i in range(5):
            transaction_name = f"test_transaction_{i}"
            with client.capture_transaction(transaction_name):
                logger.info(f"Recording transaction {transaction_name}")
                
                # Add some spans
                with client.capture_span(f"span_1_{i}"):
                    time.sleep(random.uniform(0.1, 0.3))
                
                with client.capture_span(f"span_2_{i}"):
                    time.sleep(random.uniform(0.2, 0.5))
                
                # Randomly generate an error
                if random.random() < 0.3:
                    try:
                        raise ValueError(f"Test error in transaction {transaction_name}")
                    except ValueError as e:
                        client.capture_exception()
                        logger.warning(f"Generated test error: {e}")
        
        logger.info("APM test completed.")
        return True
    except Exception as e:
        logger.error(f"Error testing APM: {e}")
        return False

def test_logging():
    """Test logging to Logstash."""
    try:
        logger.info("Testing logging to Logstash...")
        
        # Generate logs at different levels
        log_levels = [
            (logging.DEBUG, "This is a debug message"),
            (logging.INFO, "This is an info message"),
            (logging.WARNING, "This is a warning message"),
            (logging.ERROR, "This is an error message"),
            (logging.CRITICAL, "This is a critical message")
        ]
        
        for level, message in log_levels:
            logger.log(level, f"{message} - {datetime.now().isoformat()}")
            time.sleep(0.5)
        
        # Generate some structured logs
        for i in range(5):
            logger.info(
                "Structured log message",
                extra={
                    'user_id': f"user_{random.randint(1, 1000)}",
                    'action': random.choice(['login', 'logout', 'view', 'edit', 'delete']),
                    'resource': random.choice(['story', 'user', 'asset', 'profile']),
                    'status': random.choice(['success', 'failure', 'pending']),
                    'duration_ms': random.randint(10, 1000)
                }
            )
            time.sleep(0.5)
        
        logger.info("Logging test completed.")
        return True
    except Exception as e:
        logger.error(f"Error testing logging: {e}")
        return False

def main():
    """Main function to run the tests."""
    parser = argparse.ArgumentParser(description='Test the monitoring setup.')
    parser.add_argument('--statsd', action='store_true', help='Test StatsD metrics collection')
    parser.add_argument('--apm', action='store_true', help='Test APM transaction and error collection')
    parser.add_argument('--logging', action='store_true', help='Test logging to Logstash')
    parser.add_argument('--all', action='store_true', help='Run all tests')
    
    args = parser.parse_args()
    
    # If no arguments are provided, show help
    if not (args.statsd or args.apm or args.logging or args.all):
        parser.print_help()
        return
    
    # Set environment variable to enable monitoring
    os.environ['MONITORING_ENABLED'] = 'true'
    
    # Run the tests
    results = []
    
    if args.statsd or args.all:
        results.append(('StatsD', test_statsd()))
    
    if args.apm or args.all:
        results.append(('APM', test_apm()))
    
    if args.logging or args.all:
        results.append(('Logging', test_logging()))
    
    # Print the results
    print("\nTest Results:")
    print("-------------")
    for test, result in results:
        status = "PASSED" if result else "FAILED"
        print(f"{test}: {status}")

if __name__ == '__main__':
    main()