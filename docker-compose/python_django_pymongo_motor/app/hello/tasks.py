"""
Celery tasks for background processing
"""
from celery import shared_task
from datetime import datetime
import time
from .db import get_mongo_db


@shared_task
def add_numbers(x, y):
    """Simple task to demonstrate Celery"""
    time.sleep(2)  # Simulate some work
    return x + y


@shared_task
def process_user_data(user_id):
    """Process user data in the background"""
    time.sleep(3)  # Simulate processing
    
    db = get_mongo_db()
    result = db.users.update_one(
        {'_id': user_id},
        {'$set': {'last_processed': datetime.utcnow()}}
    )
    
    return {
        'user_id': user_id,
        'processed_at': datetime.utcnow().isoformat(),
        'modified': result.modified_count
    }


@shared_task
def generate_report(report_type='daily'):
    """Generate a report asynchronously"""
    time.sleep(5)  # Simulate report generation
    
    db = get_mongo_db()
    
    # Count users
    user_count = db.users.count_documents({})
    
    # Count blog posts
    post_count = db.blog_posts.count_documents({})
    
    # Store report in MongoDB
    report = {
        'type': report_type,
        'generated_at': datetime.utcnow(),
        'stats': {
            'total_users': user_count,
            'total_posts': post_count,
        }
    }
    
    db.reports.insert_one(report)
    
    return {
        'status': 'completed',
        'report_type': report_type,
        'stats': report['stats']
    }


@shared_task
def cleanup_old_data(days=30):
    """Clean up old data from the database"""
    from datetime import timedelta
    
    db = get_mongo_db()
    cutoff_date = datetime.utcnow() - timedelta(days=days)
    
    # Delete old blog posts
    result = db.blog_posts.delete_many({
        'created_at': {'$lt': cutoff_date}
    })
    
    return {
        'deleted_posts': result.deleted_count,
        'cutoff_date': cutoff_date.isoformat()
    }

