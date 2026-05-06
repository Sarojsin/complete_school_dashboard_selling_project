# Day 12 Production Implementation Plan
**Date**: 2026-05-17
**Focus**: Redis Caching & Performance Optimization

## Objectives
- Install and configure Redis server
- Implement caching layer for frequently accessed reference data
- Add cache invalidation on write operations
- Measure performance improvement (query time reduction)
- Document caching strategy in PERFORMANCE.md

## Tasks

### 1. Morning: Redis Setup (2 hours)
**Install Redis**:
- [ ] Docker development: `docker run -d -p 6379:6379 redis:7-alpine`
- [ ] Linux local: `apt-get install redis-server` or `dnf install redis`
- [ ] Windows: Use WSL2 Redis or Docker (recommended)
- [ ] Verify: `redis-cli ping` returns `PONG`

**Configure**:
- [ ] Add to `.env`:
  ```
  REDIS_URL=redis://localhost:6379/0
  CACHE_TTL=3600  # 1 hour default
  ```
- [ ] Create `modules/shared/redis_client.py`:
  ```python
  import redis.asyncio as redis
  import os
  
  REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
  redis_client = redis.from_url(REDIS_URL, decode_responses=True)
  
  async def get_redis():
      return redis_client
  ```
- [ ] Test connection in Python shell:
  ```python
  import asyncio
  from modules.shared.redis_client import redis_client
  async def test():
      await redis_client.ping()
  asyncio.run(test())
  ```

### 2. Caching Infrastructure (2 hours)
**Create caching utilities** (`modules/shared/cache.py`):

```python
from typing import Optional, Callable, Any
from functools import wraps
import json
from modules.shared.redis_client import redis_client

class CacheManager:
    def __init__(self, default_ttl: int = 3600):
        self.default_ttl = default_ttl
    
    async def get(self, key: str) -> Optional[Any]:
        try:
            data = await redis_client.get(key)
            return json.loads(data) if data else None
        except Exception as e:
            logger.error(f"Cache get error: {e}", key=key)
            return None
    
    async def set(self, key: str, value: Any, ttl: int = None):
        try:
            await redis_client.setex(
                key, 
                ttl or self.default_ttl,
                json.dumps(value, default=str)
            )
        except Exception as e:
            logger.error(f"Cache set error: {e}", key=key)
    
    async def delete(self, *keys: str):
        try:
            await redis_client.delete(*keys)
        except Exception as e:
            logger.error(f"Cache delete error: {e}")
    
    async def invalidate_pattern(self, pattern: str):
        """Delete all keys matching pattern (e.g., 'college_programs:*')"""
        try:
            keys = await redis_client.keys(pattern)
            if keys:
                await redis_client.delete(*keys)
        except Exception as e:
            logger.error(f"Cache invalidation error: {e}", pattern=pattern)

cache_manager = CacheManager()

def cacheable(ttl: int = None, key_prefix: str = ""):
    """Decorator for caching function results"""
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Build cache key from function name + args
            key = f"{key_prefix}:{func.__name__}:{hash(str(args) + str(kwargs))}"
            cached = await cache_manager.get(key)
            if cached is not None:
                return cached
            
            result = await func(*args, **kwargs)
            await cache_manager.set(key, result, ttl)
            return result
        return wrapper
    return decorator
```

### 3. Apply Caching to College Modules (2 hours)
**Identify cacheable data**:
- CollegeFeeStructure: rarely changes → cache 1 hour
- CollegeProgram: static reference data → cache 6 hours
- CollegeSemester: changes per academic year → cache 12 hours
- CollegeDepartment: almost never changes → cache 24 hours
- CollegeStudent profile (individual): short TTL (5 min) for personal data

**Implementation examples**:

**college_programs/repository.py**:
```python
from modules.shared.cache import cacheable

class CollegeProgramRepository:
    @cacheable(ttl=21600, key_prefix="college_programs")  # 6 hours
    async def get_all(self, db: AsyncSession, skip: int = 0, limit: int = 100):
        result = await db.execute(select(CollegeProgram).offset(skip).limit(limit))
        return result.scalars().all()
    
    @cacheable(ttl=21600, key_prefix="college_programs")
    async def get_by_id(self, db: AsyncSession, program_id: int):
        result = await db.execute(select(CollegeProgram).where(CollegeProgram.id == program_id))
        return result.scalars().first()
```

**college_account_section/repository.py** (fee structures):
```python
@cacheable(ttl=3600, key_prefix="fee_structures")
async def get_by_program_semester(self, db: AsyncSession, program_id: int, semester_id: int):
    ...
```

### 4. Cache Invalidation on Writes (1 hour)
**Update service layers** to invalidate relevant cache keys on mutations:

**college_programs/service.py** (create/update/delete):
```python
async def create_program(self, data: CreateProgramSchema):
    program = await self.repository.create(data)
    # Invalidate program cache
    await cache_manager.delete(f"college_programs:get_all")
    await cache_manager.delete(f"college_programs:get_by_id:{program.id}")
    return program

async def update_program(self, program_id: int, data: UpdateProgramSchema):
    updated = await self.repository.update(program_id, data)
    await cache_manager.delete(f"college_programs:get_all")
    await cache_manager.delete(f"college_programs:get_by_id:{program_id}")
    # Also invalidate any fee structures referencing this program
    await cache_manager.invalidate_pattern(f"fee_structures:program:{program_id}:*")
    return updated

async def delete_program(self, program_id: int):
    await self.repository.delete(program_id)
    await cache_manager.delete(f"college_programs:get_all")
    await cache_manager.delete(f"college_programs:get_by_id:{program_id}")
    await cache_manager.invalidate_pattern(f"fee_structures:program:{program_id}:*")
```

**Apply pattern to all write operations** across:
- college_programs
- college_semesters
- college_enrollments (invalidate student+semester program lists)
- college_exam_section (invalidate notice lists)
- college_account_section (fee structures + fee records)

### 5. Performance Testing (1 hour)
**Write benchmark test** (`tests/performance/test_caching.py`):

```python
import time
import pytest

@pytest.mark.asyncio
async def test_cached_query_performance():
    """Compare cached vs uncached query times"""
    from modules.shared.redis_client import redis_client
    from modules.college.college_programs.repository import CollegeProgramRepository
    
    repo = CollegeProgramRepository()
    db = ...  # fixture
    
    # First call - cache miss
    start = time.time()
    result1 = await repo.get_all(db, skip=0, limit=100)
    uncached_time = time.time() - start
    
    # Second call - cache hit
    start = time.time()
    result2 = await repo.get_all(db, skip=0, limit=100)
    cached_time = time.time() - start
    
    print(f"Uncached: {uncached_time:.3f}s, Cached: {cached_time:.3f}s")
    assert cached_time < uncached_time / 10  # 10x faster
    assert result1 == result2
```

**Manual profiling**:
- [ ] Use `python -m cProfile` on a complex endpoint (dean analytics) before/after caching
- [ ] Document improvements

### 6. Documentation & Commit (1 hour)
- [ ] Create `PERFORMANCE.md`:
  - Caching strategy: what is cached, TTL values, invalidation rules
  - Redis connection details
  - How to clear cache manually (`redis-cli FLUSHDB` or `cache_manager.invalidate_pattern()`)
  - Performance metrics (expected load times)
- [ ] Update `README.md` with Redis requirement in production
- [ ] Git commit: "feat(performance): Add Redis caching for college modules with TTL and invalidation"

## Deliverables
- ✅ Redis installed and running locally
- ✅ `modules/shared/redis_client.py` + `modules/shared/cache.py`
- ✅ Caching decorator applied to college_programs, college_semesters, college_fee_structures
- ✅ Cache invalidation on write operations (create/update/delete)
- ✅ Performance benchmark test showing >10x speedup on cached queries
- ✅ `PERFORMANCE.md` documented

## Success Criteria
- `redis-cli ping` returns PONG
- Second call to `/api/v1/college/programs` is faster (logs show cache hit)
- Write to programs clears related cache keys (verify via `redis-cli KEYS *`)
- No stale data observed (cache invalidation working)
- All tests pass with caching enabled

## Notes
- Use JSON serialization for cache values; handle datetime conversion (`default=str`)
- Short TTL for user-specific data; long TTL for static reference data
- Consider cache warming on app startup for rarely changing data (departments, programs)
- Monitor Redis memory usage: `redis-cli info memory`

## Next: Day 13
Background task processing setup with Celery + Redis (or FastAPI BackgroundTasks for simple jobs). Implement: bulk email sending, report generation, data export, periodic cleanup tasks.
