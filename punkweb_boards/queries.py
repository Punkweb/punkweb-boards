import datetime
from django.db import connection


def new_posts_this_week():
    QUERY = """
        SELECT
          EXTRACT(dow FROM post.created) AS chunk,
          COUNT(post.id) AS count_posts
        FROM punkweb_boards_post as post
        WHERE EXTRACT (week FROM post.created) = EXTRACT(week FROM CURRENT_DATE)
        GROUP BY chunk
        ORDER BY chunk
    """
    with connection.cursor() as cursor:
        cursor.execute(QUERY, {})
        return [
            {"chunk": chunk, "count_posts": count_posts}
            for chunk, count_posts in cursor
        ]


def new_threads_this_week():
    QUERY = """
        SELECT
          EXTRACT(dow FROM thread.created) AS chunk,
          COUNT(thread.id) AS count_threads
        FROM punkweb_boards_thread as thread
        WHERE EXTRACT (week FROM thread.created) = EXTRACT(week FROM CURRENT_DATE)
        GROUP BY chunk
        ORDER BY chunk
    """
    with connection.cursor() as cursor:
        cursor.execute(QUERY, {})
        return [
            {"chunk": chunk, "count_threads": count_threads}
            for chunk, count_threads in cursor
        ]


def new_members_this_week():
    QUERY = """
        SELECT
          EXTRACT(dow FROM member.created) AS chunk,
          COUNT(member.id) AS count_members
        FROM punkweb_boards_boardprofile AS member
        WHERE EXTRACT (week FROM member.created) = EXTRACT(week FROM CURRENT_DATE)
        GROUP BY chunk
        ORDER BY chunk
    """
    with connection.cursor() as cursor:
        cursor.execute(QUERY, {})
        return [
            {"chunk": chunk, "count_members": count_members}
            for chunk, count_members in cursor
        ]


def threads_in_subcategories():
    QUERY = """
        SELECT
          subcategory.id AS chunk,
          subcategory.name AS name,
          COUNT(thread.id) AS count_threads
        FROM punkweb_boards_subcategory as subcategory
        LEFT JOIN punkweb_boards_thread as thread
          ON thread.category_id = subcategory.id
        GROUP BY chunk
        ORDER BY count_threads DESC
    """
    with connection.cursor() as cursor:
        cursor.execute(QUERY, {})
        return [
            {"chunk": chunk, "name": name, "count_threads": count_threads}
            for chunk, name, count_threads in cursor
        ]
