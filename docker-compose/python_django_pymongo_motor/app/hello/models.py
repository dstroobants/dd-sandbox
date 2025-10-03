"""
Helper functions for working with MongoDB collections using PyMongo and Motor.
Since we're using PyMongo/Motor directly, we don't define Django models.
Instead, we work with dictionaries and MongoDB documents.
"""
from datetime import datetime
from bson import ObjectId


def create_user_document(name, email, age):
    """Create a user document dictionary"""
    return {
        'name': name,
        'email': email,
        'age': age,
        'created_at': datetime.utcnow(),
        'updated_at': datetime.utcnow()
    }


def create_blog_post_document(title, content, author, tags=None, metadata=None):
    """Create a blog post document dictionary"""
    return {
        'title': title,
        'content': content,
        'author': author,
        'tags': tags or [],
        'metadata': metadata or {},
        'created_at': datetime.utcnow(),
        'updated_at': datetime.utcnow()
    }


def serialize_document(doc):
    """Convert MongoDB document to JSON-serializable format"""
    if doc is None:
        return None
    
    result = {}
    for key, value in doc.items():
        # Rename _id to id (Django templates can't access underscore attributes)
        new_key = 'id' if key == '_id' else key
        
        if isinstance(value, ObjectId):
            result[new_key] = str(value)
        elif isinstance(value, datetime):
            result[new_key] = value.isoformat()
        else:
            result[new_key] = value
    return result
