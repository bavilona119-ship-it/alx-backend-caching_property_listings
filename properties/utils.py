from django.core.cache import cache
from .models import Property

def get_all_properties():
    properties = cache.get('all_properties')

    if properties is None:
        properties = list(Property.objects.all().values(
            "id", "title", "description", "price", "location", "created_at"
        ))
        cache.set('all_properties', properties, 3600)  # Cache for 1 hour

    return properties
from django_redis import get_redis_connection
import logging

logger = logging.getLogger(__name__)

def get_redis_cache_metrics():
    redis_conn = get_redis_connection("default")

    info = redis_conn.info()

    hits = info.get("keyspace_hits", 0)
    misses = info.get("keyspace_misses", 0)

    total = hits + misses
    hit_ratio = (hits / total) if total > 0 else 0

    metrics = {
        "hits": hits,
        "misses": misses,
        "hit_ratio": round(hit_ratio, 4)
    }

    # Log the metrics
    logger.info(f"Redis Cache Metrics: Hits={hits}, Misses={misses}, Hit Ratio={metrics['hit_ratio']}")

    return metrics
