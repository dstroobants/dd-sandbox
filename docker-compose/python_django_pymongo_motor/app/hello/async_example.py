"""
EXAMPLE: How to use Motor in a true async Django view

To use this approach, you would need:
1. Django 3.1+ with ASGI support
2. An ASGI server like uvicorn or daphne
3. Change view definitions from 'def' to 'async def'

This file is for reference only - not used in the current sync Django setup.
"""

from django.shortcuts import render
from .db import get_motor_db
from .models import create_user_document, serialize_document


async def async_mongodb_demo(request):
    """
    TRUE async Django view using Motor
    
    To use this:
    1. Update myproject/settings.py: Add 'daphne' to INSTALLED_APPS
    2. Update docker-compose.yaml: Use daphne or uvicorn instead of gunicorn
    3. Replace the sync view with this async version in urls.py
    """
    db = get_motor_db()
    
    try:
        # These operations are truly non-blocking with Motor
        user_count = await db.users.count_documents({})
        
        if user_count == 0:
            sample_users = [
                create_user_document('Async User 1', 'async1@example.com', 25),
                create_user_document('Async User 2', 'async2@example.com', 30),
            ]
            await db.users.insert_many(sample_users)
        
        # Fetch data asynchronously (non-blocking)
        users_cursor = db.users.find().limit(50)
        users = await users_cursor.to_list(length=50)
        
        posts_cursor = db.blog_posts.find().limit(50)
        posts = await posts_cursor.to_list(length=50)
        
        # Multiple async operations can run concurrently
        import asyncio
        user_count, post_count = await asyncio.gather(
            db.users.count_documents({}),
            db.blog_posts.count_documents({})
        )
        
        context = {
            'title': 'True Async Motor Demo',
            'users': [serialize_document(u) for u in users],
            'posts': [serialize_document(p) for p in posts],
            'user_count': user_count,
            'post_count': post_count,
            'connection_status': 'Connected to MongoDB (Motor - True Async)',
        }
        
        return render(request, 'hello/mongodb_async.html', context)
        
    except Exception as e:
        import traceback
        context = {
            'title': 'Motor Async Demo',
            'error': f'Database connection error: {str(e)}',
            'error_details': traceback.format_exc(),
            'connection_status': 'Failed to connect to MongoDB'
        }
        return render(request, 'hello/mongodb_async.html', context)


# Example of multiple concurrent queries with Motor
async def concurrent_queries_example():
    """
    Example showing Motor's power: running multiple queries concurrently
    """
    import asyncio
    db = get_motor_db()
    
    # All these queries run concurrently (not sequentially)
    results = await asyncio.gather(
        db.users.count_documents({}),
        db.blog_posts.count_documents({}),
        db.users.find().limit(10).to_list(length=10),
        db.blog_posts.find().limit(10).to_list(length=10),
    )
    
    user_count, post_count, recent_users, recent_posts = results
    
    return {
        'user_count': user_count,
        'post_count': post_count,
        'recent_users': recent_users,
        'recent_posts': recent_posts
    }


# To switch to async Django:
# 1. Install: pip install daphne uvicorn
# 2. Update docker CMD in startup.sh:
#    exec ddtrace-run daphne -b 0.0.0.0 -p 8000 myproject.asgi:application
# 3. Or use uvicorn:
#    exec ddtrace-run uvicorn myproject.asgi:application --host 0.0.0.0 --port 8000

