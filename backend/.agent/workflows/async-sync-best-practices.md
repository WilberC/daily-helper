---
description: Best practices for async/sync in Strawberry GraphQL with Django
---

# Async/Sync Best Practices for Strawberry GraphQL + Django

## The Problem

When using Strawberry GraphQL with Django, you might encounter the error:
```
You cannot call this from an async context - use a thread or sync_to_async
```

This happens when trying to access Django ORM queries from async resolvers.

## The Solution: Default to Sync

**Instead of making everything async and wrapping with `sync_to_async`, do the opposite:**

✅ **Make all resolvers synchronous by default**
❌ Don't use `async`/`await` unless you have a specific reason

### Why This Approach is Better

1. **Django ORM is synchronous** - It works best in sync contexts
2. **Simpler code** - No need for `sync_to_async` wrappers everywhere
3. **Better performance** - Avoid unnecessary async overhead
4. **Fewer bugs** - Less context switching means fewer edge cases
5. **Easier to maintain** - Straightforward, predictable code flow

## When to Use Async

Only use `async` resolvers when you have:

1. **External API calls** that support async (using `httpx`, `aiohttp`, etc.)
2. **I/O-bound operations** that can run concurrently
3. **Multiple independent operations** that can be parallelized
4. **Specific async libraries** that require async context

## Example Refactoring

### ❌ Before (Unnecessarily Async)

```python
@strawberry.field
async def all_users(self, info: Info) -> list[UserType]:
    @sync_to_async
    def check_permissions():
        user = info.context.request.user
        return user.is_authenticated and user.is_staff
    
    if not await check_permissions():
        return []
    
    @sync_to_async
    def get_users():
        return list(User.objects.filter(is_superuser=False))
    
    return await get_users()
```

### ✅ After (Clean Sync)

```python
@strawberry.field
def all_users(self, info: Info) -> list[UserType]:
    user = info.context.request.user
    if not (user.is_authenticated and user.is_staff):
        return []
    
    return list(User.objects.filter(is_superuser=False))
```

## Configuration

**CRITICAL:** You must use the **synchronous** `GraphQLView` in your URLs configuration!

### ✅ Correct Configuration (urls.py)

```python
from strawberry.django.views import GraphQLView  # NOT AsyncGraphQLView!
from .schema import schema

urlpatterns = [
    path('graphql/', csrf_exempt(GraphQLView.as_view(schema=schema))),
]
```

### ❌ Wrong Configuration

```python
from strawberry.django.views import AsyncGraphQLView  # This forces async context!
from .schema import schema

urlpatterns = [
    path('graphql/', csrf_exempt(AsyncGraphQLView.as_view(schema=schema))),
]
```

**Why this matters:** Using `AsyncGraphQLView` forces all resolvers to run in an async context, which causes the "You cannot call this from an async context" error when accessing Django ORM. Even if your resolvers are synchronous, the async view wrapper will break them.

**Rule of thumb:** 
- Use `GraphQLView` (sync) for Django projects with ORM operations
- Only use `AsyncGraphQLView` if you have truly async resolvers AND async database drivers (like `databases` or `asyncpg`)


## When You Actually Need Async

If you have a legitimate use case for async (e.g., calling external APIs), here's how:

```python
import httpx

@strawberry.field
async def fetch_external_data(self, info: Info) -> str:
    # This is a good use of async - external API call
    async with httpx.AsyncClient() as client:
        response = await client.get("https://api.example.com/data")
        return response.text
```

## Summary

- **Default to sync** for all Django ORM operations
- **Use async sparingly** only when you have true async I/O operations
- **Keep it simple** - don't add async complexity unless necessary
- **Trust Django** - it's designed to work synchronously and does it well
