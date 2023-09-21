from django.http import HttpResponse
from django.shortcuts import redirect


def unauthenticated_user(view_func):
	def wrapper_func(request, *args, **kwargs):
		if request.user.is_authenticated:
			return redirect('list')
		else:
			return view_func(request, *args, **kwargs)

	return wrapper_func


def allowed_users(allowed_roles=[]):
	def decorator(view_func):
		def wrapper_func(request, *args, **kwargs):

			group = None
			if request.user.role:
				group = request.user.role

			if group in allowed_roles:
				return view_func(request, *args, **kwargs)
			else:
				return HttpResponse('<h3>You are not authorized to view this page</h3>')
		return wrapper_func
	return decorator


def admin_only(view_func):
	def wrapper_function(request, *args, **kwargs):
		if request.user.role == 'Admin':
			return view_func(request, *args, **kwargs)

	return wrapper_function
