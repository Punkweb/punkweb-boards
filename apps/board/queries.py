from django.db.models import Sum
from apps.common.base import BaseQuery
from .models import Category, Subcategory, Post, Comment, Shout
from .forms import PostForm, CommentForm, ShoutForm


class CategoryQuery(BaseQuery):
    def __init__(self, category_id):
        self.category_id = category_id

    def get_name(self):
        return 'category_query'

    def get_context(self):
        category = Category.objects.get(id=self.category_id)
        sub_groups = []
        subcategories = Subcategory.objects.filter(parent__id=category.id).order_by('order')
        for sub in subcategories:
            posts = Post.objects.filter(category__id=sub.id).order_by('-created')
            num_posts = len(posts)
            last_post = posts.first()
            comments = Comment.objects.filter(post__category__id=sub.id)
            num_comments = len(comments)
            sub_groups.append({
                'category': sub,
                'num_posts': num_posts,
                'last_post': last_post,
                'num_comments': num_comments
            })
        return {
            'category': category,
            'subcategories': sub_groups
        }

class SubCategoryQuery(BaseQuery):
    def __init__(self, category_id):
        self.category_id = category_id

    def get_name(self):
        return 'subcategory_query'

    def get_context(self):
        category = Subcategory.objects.get(id=self.category_id)
        post_groups = []
        posts = Post.objects.filter(category__id=self.category_id).order_by('-created')
        for post in posts:
            comments = Comment.objects.filter(post_id=post.id).order_by('-created')
            last_comment = comments.first()
            group = {
                'post': post,
                'num_comments': len(comments),
                'last_comment': last_comment
            }
            post_groups.append(group)
        return {
            'category': category,
            'posts': post_groups
        }


class RecentPostsQuery(BaseQuery):
    def get_name(self):
        return 'recent_posts_query'

    def get_context(self):
        posts = Post.objects.all().order_by('-created')[:5]
        return {
            'recents': posts
        }


class RecentActivityQuery(BaseQuery):
    def get_name(self):
        return 'recent_activity_query'

    def get_context(self):
        posts = Post.objects.all().order_by('-modified')[:5]
        return {
            'recents': posts
        }
