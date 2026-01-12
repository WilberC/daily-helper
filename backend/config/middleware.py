"""
Custom middleware for the Django application.
"""
from django.http import JsonResponse
import json


class GraphQLAuthMiddleware:
    """
    Middleware to enforce authentication on GraphQL requests.
    
    This middleware blocks all GraphQL requests from unauthenticated users,
    except for the 'login' mutation which is required for authentication.
    
    For unauthorized requests, it returns a standardized JSON response with
    an 'unauthorized' error.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Only apply to GraphQL endpoint
        if request.path.startswith('/graphql'):
            # Check if user is authenticated
            if not request.user.is_authenticated:
                # Allow login mutation to pass through
                if request.method == 'POST':
                    try:
                        body = json.loads(request.body.decode('utf-8'))
                        query = body.get('query', '')
                        operation_name = body.get('operationName', '')
                        
                        # Check if this is a login mutation
                        # We check both the query content and operation name
                        is_login = (
                            'mutation' in query.lower() and 
                            'login' in query.lower() and
                            'register' not in query.lower()  # Exclude register
                        ) or operation_name == 'Login'
                        
                        if not is_login:
                            # Return unauthorized response
                            return JsonResponse({
                                'errors': [{
                                    'message': 'Unauthorized. Please log in to access this resource.',
                                    'extensions': {
                                        'code': 'UNAUTHORIZED',
                                        'http': {
                                            'status': 401
                                        }
                                    }
                                }]
                            }, status=401)
                    except (json.JSONDecodeError, UnicodeDecodeError):
                        # If we can't parse the body, block the request
                        return JsonResponse({
                            'errors': [{
                                'message': 'Unauthorized. Please log in to access this resource.',
                                'extensions': {
                                    'code': 'UNAUTHORIZED',
                                    'http': {
                                        'status': 401
                                    }
                                }
                            }]
                        }, status=401)
                else:
                    # Block GET requests (GraphiQL interface) for unauthenticated users
                    return JsonResponse({
                        'errors': [{
                            'message': 'Unauthorized. Please log in to access this resource.',
                            'extensions': {
                                'code': 'UNAUTHORIZED',
                                'http': {
                                    'status': 401
                                }
                            }
                        }]
                    }, status=401)
        
        response = self.get_response(request)
        return response
