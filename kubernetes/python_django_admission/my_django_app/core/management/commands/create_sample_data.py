from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import Task, Category, Profile


class Command(BaseCommand):
    help = 'Create sample data for testing'

    def handle(self, *args, **options):
        # Create superuser if it doesn't exist
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
            self.stdout.write(self.style.SUCCESS('Created superuser: admin/admin123'))

        # Create test user
        test_user, created = User.objects.get_or_create(
            username='testuser',
            defaults={
                'email': 'test@example.com',
                'first_name': 'Test',
                'last_name': 'User'
            }
        )
        if created:
            test_user.set_password('test123')
            test_user.save()
            self.stdout.write(self.style.SUCCESS('Created test user: testuser/test123'))

        # Create categories
        categories_data = [
            {'name': 'Work', 'description': 'Work-related tasks', 'color': '#007bff'},
            {'name': 'Personal', 'description': 'Personal tasks', 'color': '#28a745'},
            {'name': 'Learning', 'description': 'Learning and development', 'color': '#ffc107'},
        ]

        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults=cat_data
            )
            if created:
                self.stdout.write(f'Created category: {category.name}')

        # Create sample tasks
        tasks_data = [
            {
                'title': 'Setup Django Application',
                'description': 'Create a comprehensive Django boilerplate with task management',
                'completed': True,
                'created_by': test_user
            },
            {
                'title': 'Add REST API endpoints',
                'description': 'Implement RESTful API for tasks and categories',
                'completed': True,
                'created_by': test_user
            },
            {
                'title': 'Deploy to Kubernetes',
                'description': 'Deploy the Django application to Kubernetes cluster',
                'completed': False,
                'created_by': test_user
            },
            {
                'title': 'Add Datadog monitoring',
                'description': 'Integrate Datadog APM and logging',
                'completed': False,
                'created_by': test_user
            },
            {
                'title': 'Write documentation',
                'description': 'Create comprehensive documentation for the application',
                'completed': False,
                'created_by': test_user
            },
        ]

        for task_data in tasks_data:
            task, created = Task.objects.get_or_create(
                title=task_data['title'],
                defaults=task_data
            )
            if created:
                self.stdout.write(f'Created task: {task.title}')

        # Create profile for test user
        profile, created = Profile.objects.get_or_create(
            user=test_user,
            defaults={
                'bio': 'Test user for Django application',
                'location': 'Remote',
            }
        )
        if created:
            self.stdout.write(f'Created profile for: {test_user.username}')

        self.stdout.write(
            self.style.SUCCESS(
                '\nSample data created successfully!\n'
                'You can now:\n'
                '- Visit /admin/ and login with admin/admin123\n'
                '- Visit /tasks/ to see sample tasks\n'
                '- Visit /api/tasks/ to test the API\n'
                '- Visit /health/ for health check\n'
            )
        ) 
