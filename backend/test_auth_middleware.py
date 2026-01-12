#!/usr/bin/env python3
"""
Simple test script to verify GraphQL authentication middleware using urllib.
"""
import urllib.request
import urllib.error
import json

BASE_URL = "http://localhost:8000/graphql/"

def make_request(query, operation_name=None):
    """Make a GraphQL request."""
    data = {"query": query}
    if operation_name:
        data["operationName"] = operation_name
    
    json_data = json.dumps(data).encode('utf-8')
    
    req = urllib.request.Request(
        BASE_URL,
        data=json_data,
        headers={'Content-Type': 'application/json'}
    )
    
    try:
        with urllib.request.urlopen(req) as response:
            return response.status, json.loads(response.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read().decode('utf-8'))

print("=" * 70)
print("GraphQL Authentication Middleware Test")
print("=" * 70)
print()

# Test 1: Unauthorized query (should be blocked)
print("Test 1: Unauthorized query (should return 401)")
print("-" * 70)
query = """
query {
    me {
        id
        username
    }
}
"""
status, response = make_request(query)
print(f"Status Code: {status}")
print(f"Response: {json.dumps(response, indent=2)}")
print()

# Test 2: Unauthorized register mutation (should be blocked)
print("Test 2: Unauthorized register mutation (should return 401)")
print("-" * 70)
query = """
mutation {
    register(input: {
        username: "testuser"
        email: "test@example.com"
        password: "password123"
    }) {
        success
        message
    }
}
"""
status, response = make_request(query)
print(f"Status Code: {status}")
print(f"Response: {json.dumps(response, indent=2)}")
print()

# Test 3: Login mutation (should be allowed)
print("Test 3: Login mutation (should return 200, but may fail with wrong credentials)")
print("-" * 70)
query = """
mutation {
    login(username: "admin", password: "wrongpassword") {
        success
        message
        user {
            id
            username
        }
    }
}
"""
status, response = make_request(query)
print(f"Status Code: {status}")
print(f"Response: {json.dumps(response, indent=2)}")
print()

print("=" * 70)
print("Test Summary:")
print("- Test 1 should return 401 (Unauthorized)")
print("- Test 2 should return 401 (Unauthorized)")
print("- Test 3 should return 200 (but login may fail with invalid credentials)")
print("=" * 70)
