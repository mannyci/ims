from .models import Environment

def needs_env():
	return not Environment.objects.all().exists()