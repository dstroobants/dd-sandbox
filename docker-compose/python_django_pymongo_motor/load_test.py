#!/usr/bin/env python3
"""
Load Testing Script for Django + PyMongo + Motor + Celery Application

Simulates heavy production traffic with:
- Concurrent HTTP requests
- Database operations (reads/writes)
- Celery task triggering
- Mixed workload patterns

Usage:
    python load_test.py --users 50 --duration 60
    python load_test.py --quick  # Quick test with default settings
"""

import argparse
import asyncio
import aiohttp
import time
import random
import statistics
from typing import List, Dict, Any
from datetime import datetime
from collections import defaultdict


class LoadTester:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.results = defaultdict(list)
        self.errors = []
        self.total_requests = 0
        self.successful_requests = 0
        self.failed_requests = 0
        
    async def make_request(self, session: aiohttp.ClientSession, method: str, 
                          endpoint: str, json_data: Dict = None) -> Dict[str, Any]:
        """Make a single HTTP request and record metrics"""
        start_time = time.time()
        url = f"{self.base_url}{endpoint}"
        
        try:
            if method == "GET":
                async with session.get(url, timeout=aiohttp.ClientTimeout(total=30)) as response:
                    response_time = time.time() - start_time
                    status = response.status
                    try:
                        data = await response.json()
                    except:
                        data = await response.text()
            else:  # POST
                async with session.post(url, json=json_data, 
                                       timeout=aiohttp.ClientTimeout(total=30)) as response:
                    response_time = time.time() - start_time
                    status = response.status
                    try:
                        data = await response.json()
                    except:
                        data = await response.text()
            
            self.total_requests += 1
            if status < 400:
                self.successful_requests += 1
            else:
                self.failed_requests += 1
                
            return {
                'endpoint': endpoint,
                'method': method,
                'status': status,
                'response_time': response_time,
                'success': status < 400
            }
            
        except Exception as e:
            response_time = time.time() - start_time
            self.total_requests += 1
            self.failed_requests += 1
            self.errors.append(f"{endpoint}: {str(e)}")
            return {
                'endpoint': endpoint,
                'method': method,
                'status': 0,
                'response_time': response_time,
                'success': False,
                'error': str(e)
            }
    
    async def user_browsing_session(self, session: aiohttp.ClientSession, user_id: int):
        """Simulate a user browsing the application"""
        endpoints = [
            ('GET', '/'),
            ('GET', '/hello/'),
            ('GET', '/sync/'),
            ('GET', '/async/'),
            ('GET', '/celery/'),
        ]
        
        for method, endpoint in endpoints:
            result = await self.make_request(session, method, endpoint)
            self.results[endpoint].append(result['response_time'])
            await asyncio.sleep(random.uniform(0.1, 0.5))  # Think time
    
    async def api_read_operations(self, session: aiohttp.ClientSession, user_id: int):
        """Simulate API read operations"""
        endpoints = [
            '/api/users/',
            '/api/posts/',
        ]
        
        for _ in range(random.randint(3, 8)):
            endpoint = random.choice(endpoints)
            result = await self.make_request(session, 'GET', endpoint)
            self.results[endpoint].append(result['response_time'])
            await asyncio.sleep(random.uniform(0.05, 0.2))
    
    async def api_write_operations(self, session: aiohttp.ClientSession, user_id: int):
        """Simulate API write operations (creating users and posts)"""
        # Create a user
        user_data = {
            'name': f'LoadTest User {user_id}',
            'email': f'loadtest{user_id}@example.com',
            'age': random.randint(18, 65)
        }
        
        result = await self.make_request(session, 'POST', '/api/users/', user_data)
        self.results['/api/users/ (POST)'].append(result['response_time'])
        await asyncio.sleep(0.1)
        
        # Create a blog post
        post_data = {
            'title': f'Load Test Post {user_id} - {datetime.now().isoformat()}',
            'content': f'This is a load test post generated at {datetime.now()}',
            'author': f'LoadTest User {user_id}',
            'tags': ['loadtest', 'performance', 'testing'],
            'metadata': {'load_test': True, 'user_id': user_id}
        }
        
        result = await self.make_request(session, 'POST', '/api/posts/', post_data)
        self.results['/api/posts/ (POST)'].append(result['response_time'])
    
    async def trigger_celery_tasks(self, session: aiohttp.ClientSession, user_id: int):
        """Simulate triggering Celery background tasks"""
        tasks = [
            {'task_type': 'add', 'x': random.randint(1, 100), 'y': random.randint(1, 100)},
            {'task_type': 'report', 'report_type': 'daily'},
        ]
        
        for _ in range(random.randint(1, 3)):
            task_data = random.choice(tasks)
            result = await self.make_request(session, 'POST', '/api/tasks/trigger/', task_data)
            self.results['/api/tasks/trigger/'].append(result['response_time'])
            await asyncio.sleep(random.uniform(0.5, 1.0))
    
    async def mixed_workload(self, session: aiohttp.ClientSession, user_id: int):
        """Simulate a realistic mixed workload"""
        # 60% reads, 30% writes, 10% tasks
        action = random.choices(
            ['read', 'write', 'task', 'browse'],
            weights=[40, 25, 10, 25],
            k=1
        )[0]
        
        if action == 'read':
            await self.api_read_operations(session, user_id)
        elif action == 'write':
            await self.api_write_operations(session, user_id)
        elif action == 'task':
            await self.trigger_celery_tasks(session, user_id)
        else:
            await self.user_browsing_session(session, user_id)
    
    async def run_user(self, user_id: int, duration: int, workload_type: str):
        """Simulate a single user for the specified duration"""
        async with aiohttp.ClientSession() as session:
            end_time = time.time() + duration
            
            while time.time() < end_time:
                try:
                    if workload_type == 'browse':
                        await self.user_browsing_session(session, user_id)
                    elif workload_type == 'read':
                        await self.api_read_operations(session, user_id)
                    elif workload_type == 'write':
                        await self.api_write_operations(session, user_id)
                    elif workload_type == 'tasks':
                        await self.trigger_celery_tasks(session, user_id)
                    else:  # mixed
                        await self.mixed_workload(session, user_id)
                    
                    await asyncio.sleep(random.uniform(0.1, 1.0))
                except Exception as e:
                    self.errors.append(f"User {user_id}: {str(e)}")
    
    async def run_load_test(self, num_users: int, duration: int, workload_type: str = 'mixed'):
        """Run the load test with specified number of concurrent users"""
        print(f"\n{'='*70}")
        print(f"🚀 Starting Load Test")
        print(f"{'='*70}")
        print(f"  Base URL: {self.base_url}")
        print(f"  Concurrent Users: {num_users}")
        print(f"  Duration: {duration} seconds")
        print(f"  Workload Type: {workload_type}")
        print(f"  Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*70}\n")
        
        start_time = time.time()
        
        # Create tasks for all users
        tasks = [
            self.run_user(user_id, duration, workload_type)
            for user_id in range(num_users)
        ]
        
        # Run all users concurrently
        await asyncio.gather(*tasks)
        
        total_time = time.time() - start_time
        
        # Print results
        self.print_results(total_time)
    
    def print_results(self, total_time: float):
        """Print detailed load test results"""
        print(f"\n{'='*70}")
        print(f"📊 Load Test Results")
        print(f"{'='*70}\n")
        
        print(f"⏱️  Total Duration: {total_time:.2f} seconds")
        print(f"📈 Total Requests: {self.total_requests}")
        print(f"✅ Successful: {self.successful_requests} ({self.successful_requests/max(self.total_requests,1)*100:.1f}%)")
        print(f"❌ Failed: {self.failed_requests} ({self.failed_requests/max(self.total_requests,1)*100:.1f}%)")
        print(f"🔥 Throughput: {self.total_requests/total_time:.2f} requests/second")
        
        print(f"\n{'─'*70}")
        print(f"📍 Response Times by Endpoint")
        print(f"{'─'*70}\n")
        
        # Sort endpoints by average response time
        endpoint_stats = {}
        for endpoint, times in self.results.items():
            if times:
                endpoint_stats[endpoint] = {
                    'count': len(times),
                    'avg': statistics.mean(times),
                    'min': min(times),
                    'max': max(times),
                    'p50': statistics.median(times),
                    'p95': sorted(times)[int(len(times) * 0.95)] if len(times) > 1 else times[0],
                }
        
        # Print in table format
        print(f"{'Endpoint':<35} {'Count':>8} {'Avg':>8} {'Min':>8} {'Max':>8} {'P50':>8} {'P95':>8}")
        print(f"{'─'*35} {'─'*8} {'─'*8} {'─'*8} {'─'*8} {'─'*8} {'─'*8}")
        
        for endpoint in sorted(endpoint_stats.keys(), key=lambda x: endpoint_stats[x]['avg']):
            stats = endpoint_stats[endpoint]
            print(f"{endpoint:<35} {stats['count']:>8} "
                  f"{stats['avg']:>7.3f}s {stats['min']:>7.3f}s {stats['max']:>7.3f}s "
                  f"{stats['p50']:>7.3f}s {stats['p95']:>7.3f}s")
        
        if self.errors:
            print(f"\n{'─'*70}")
            print(f"⚠️  Errors (showing first 10)")
            print(f"{'─'*70}\n")
            for error in self.errors[:10]:
                print(f"  • {error}")
            if len(self.errors) > 10:
                print(f"\n  ... and {len(self.errors) - 10} more errors")
        
        print(f"\n{'='*70}")
        print(f"✅ Load Test Complete!")
        print(f"{'='*70}\n")


async def main():
    parser = argparse.ArgumentParser(
        description='Load test the Django + PyMongo + Motor + Celery application'
    )
    parser.add_argument('--users', type=int, default=20,
                       help='Number of concurrent users (default: 20)')
    parser.add_argument('--duration', type=int, default=30,
                       help='Test duration in seconds (default: 30)')
    parser.add_argument('--url', type=str, default='http://localhost:8000',
                       help='Base URL (default: http://localhost:8000)')
    parser.add_argument('--workload', type=str, default='mixed',
                       choices=['mixed', 'browse', 'read', 'write', 'tasks'],
                       help='Workload type (default: mixed)')
    parser.add_argument('--quick', action='store_true',
                       help='Quick test: 10 users for 15 seconds')
    parser.add_argument('--stress', action='store_true',
                       help='Stress test: 100 users for 60 seconds')
    
    args = parser.parse_args()
    
    if args.quick:
        args.users = 10
        args.duration = 15
    elif args.stress:
        args.users = 100
        args.duration = 60
    
    # Check if application is running
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(args.url, timeout=aiohttp.ClientTimeout(total=5)) as response:
                if response.status >= 500:
                    print(f"❌ Error: Application returned status {response.status}")
                    return
    except Exception as e:
        print(f"❌ Error: Cannot connect to {args.url}")
        print(f"   Make sure the application is running: make run")
        return
    
    # Run load test
    tester = LoadTester(args.url)
    await tester.run_load_test(args.users, args.duration, args.workload)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n⚠️  Load test interrupted by user")

