import urlparse

import redis
import requests

from fncache import RedisLru

def purge_redis_cache(cache_redis_url, tags):
    cache_redis = redis.StrictRedis.from_url(cache_redis_url)
    lru_cache = RedisLru(cache_redis) 

    all_tags = set(tags)
    for tag in set(all_tags):
        print tag
        lru_cache.purge(tag)

def purge_fastly_tags(domain, api_key, service_id, tags):
    session = requests.session()
    headers = {"Fastly-Key": api_key, "Accept": "application/json"}

    all_tags = set(tags)
    purges = {}

    for tag in set(all_tags):
        # Build the URL
        url_path = "/service/%s/purge/%s" % (service_id, tag)
        url = urlparse.urljoin(domain, url_path)

        # Issue the Purge
        resp = session.post(url, headers=headers)
        resp.raise_for_status()

        # Store the Purge ID so we can track it later
        purges[tag] = resp.json()["id"]

    # for tag, purge_id in purges.iteritems():
    #     # Ensure that the purge completed successfully
    #     url = urlparse.urljoin(domain, "/purge")
    #     status = session.get(url, params={"id": purge_id})
    #     status.raise_for_status()

    #     # If the purge completely successfully remove the tag from
    #     #   our list.
    #     if status.json().get("results", {}).get("complete", None):
    #         all_tags.remove(tag)
