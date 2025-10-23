from django.db import models
import json


class User(models.Model):
    """Simple User model to demonstrate PostgreSQL with psycopg2"""
    name = models.CharField(max_length=100)
    email = models.EmailField()
    age = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'users'
    
    def __str__(self):
        return self.name


class BlogPost(models.Model):
    """BlogPost model to demonstrate PostgreSQL document features"""
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.CharField(max_length=100)
    tags = models.TextField(blank=True, default='[]')  # Store array of tags as JSON string
    metadata = models.TextField(blank=True, default='{}')  # Store nested document as JSON string
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'blog_posts'
    
    def __str__(self):
        return self.title
    
    def get_tags(self):
        """Get tags as Python list"""
        try:
            return json.loads(self.tags) if self.tags else []
        except (json.JSONDecodeError, TypeError):
            return []
    
    def set_tags(self, tags_list):
        """Set tags from Python list"""
        self.tags = json.dumps(tags_list)
    
    def get_metadata(self):
        """Get metadata as Python dict"""
        try:
            return json.loads(self.metadata) if self.metadata else {}
        except (json.JSONDecodeError, TypeError):
            return {}
    
    def set_metadata(self, metadata_dict):
        """Set metadata from Python dict"""
        self.metadata = json.dumps(metadata_dict)
