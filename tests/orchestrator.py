from django.contrib.auth import get_user_model


def create_test_user():
    User = get_user_model()
    username = 'testuser'
    defaults = {
        'email': 'testuser@example.com',
        'first_name': 'Test',
        'last_name': 'User',
        'is_active': True
    }

    user, created = User.objects.get_or_create(username=username, defaults=defaults)

    if created:
        user.set_password('testpassword')
        user.save()

    return user

def clear_database():
    try:
        User = get_user_model()
        User.objects.all().delete()
    except Exception as e:
        print(f"Error clearing database: {e}")

if __name__ == "__main__":
    create_test_user()
    clear_database()
