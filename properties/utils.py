from django.core.cache import cache
from .models import Property
from django_redis import get_redis_connection
import logging

logger = logging.getLogger(__name__)

def get_all_properties():
    # Check cache for properties
    properties = cache.get('all_properties')
    if properties is None:
        # Fetch from database if not in cache
        properties = Property.objects.all()
        # Store in cache for 1 hour (3600 seconds)
        cache.set('all_properties', properties, 3600)
    return properties

def get_redis_cache_metrics():
    try:
        # Connect to Redis
        redis = get_redis_connection('default')
        # Get Redis INFO
        info = redis.info()
        hits = info.get('keyspace_hits', 0)
        misses = info.get('keyspace_misses', 0)
        total_requests = hits + misses
        hit_ratio = (hits / total_requests * 100) if total_requests > 0 else 0
        # Log metrics
        logger.info(f"Cache Hits: {hits}, Misses: {misses}, Hit Ratio: {hit_ratio:.2f}%")
        return {
            'hits': hits,
            'misses': misses,
            'hit_ratio': hit_ratio
        }
    except Exception as e:
        logger.error(f"Error retrieving cache metrics: {e}")
        return {'hits': 0, 'misses': 0, 'hit_ratio': 0}
