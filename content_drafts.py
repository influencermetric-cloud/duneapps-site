"""Scheduled guides for duneapps.com (see the note above INDEX in content_posts.py).

Each draft is a dict with the same keys as a post in content_posts.POSTS, plus:
  "publish_on": "YYYY-MM-DD"  date (IST) it goes live; date_iso and updated match it
  "link_from":  [slug, ...]   live posts that should list it in their related cards
Nothing here renders before its date.
"""

DRAFTS = []
