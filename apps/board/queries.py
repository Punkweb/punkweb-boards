from apps.common.base import BaseQuery
from .models import Category, Subcategory, Post, Comment, Shout
from .forms import PostForm, CommentForm, ShoutForm


class CategoryQuery(BaseQuery):
    def __init__(self, category_id):
        self.category_id = category_id

    def get_name(self):
        return 'category_query'

    def get_context(self):
        parent = Category.objects.get(id=self.category_id)
        children_groups = []
        children = Subcategory.objects.filter(parent__id=parent.id).order_by('order')
        for child in children:
            child_posts = Post.objects.filter(category__id=child.id).order_by('-created')
            last_post = child_posts.first()
            children_groups.append({
                'category': child,
                'num_posts': len(child_posts),
                'last_post': last_post
            })
        return {
            'parent': parent,
            'children': children_groups
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
