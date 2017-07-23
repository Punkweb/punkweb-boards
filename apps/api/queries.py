import datetime
from django.db import connection


def posts_and_threads_by_day():
    QUERY = """
        SELECT
          EXTRACT(dow FROM thread.created) AS chunk,
          COUNT(thread.id) AS count_threads,
          COUNT(post.id) AS count_posts
        FROM api_thread as thread
        LEFT JOIN api_post as post
          ON post.thread_id = thread.id
        GROUP BY chunk
        ORDER BY chunk
    """
    with connection.cursor() as cursor:
        cursor.execute(QUERY, {})
        return [
            {
                'chunk': chunk,
                'count_threads': count_threads,
                'count_posts': count_posts
            } for chunk, count_threads, count_posts in cursor
        ]
