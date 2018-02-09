import datetime
from django.db import connection


def posts_by_dow():
    QUERY = """
        SELECT
          EXTRACT(dow FROM post.created) AS chunk,
          COUNT(post.id) AS count_posts
        FROM django_boards_post as post
        GROUP BY chunk
        ORDER BY chunk
    """
    with connection.cursor() as cursor:
        cursor.execute(QUERY, {})
        return [
            {
                'chunk': chunk,
                'count_posts': count_posts
            } for chunk, count_posts in cursor
        ]

def threads_by_dow():
    QUERY = """
        SELECT
          EXTRACT(dow FROM thread.created) AS chunk,
          COUNT(thread.id) AS count_threads
        FROM django_boards_thread as thread
        GROUP BY chunk
        ORDER BY chunk
    """
    with connection.cursor() as cursor:
        cursor.execute(QUERY, {})
        return [
            {
                'chunk': chunk,
                'count_threads': count_threads
            } for chunk, count_threads in cursor
        ]

def threads_in_subcategories():
    QUERY = """
        SELECT
          subcategory.id AS chunk,
          subcategory.name AS name,
          COUNT(thread.id) AS count_threads
        FROM django_boards_subcategory as subcategory
        LEFT JOIN django_boards_thread as thread
          ON thread.category_id = subcategory.id
        GROUP BY chunk
        ORDER BY count_threads DESC
    """
    with connection.cursor() as cursor:
        cursor.execute(QUERY, {})
        return [
            {
                'chunk': chunk,
                'name': name,
                'count_threads': count_threads,
            } for chunk, name, count_threads in cursor
        ]
