from django.contrib.auth import get_user_model
from django.test import TestCase
from punkweb_boards.models import (
    BoardProfile, UserRank, Category, Subcategory, Thread
)


class ProfileTestCase(TestCase):

    def setUp(self):
        self.new_user = get_user_model().objects.create_user(
            username='NewUser', email='test@punkweb.net', password='testyboi'
        )

    def test_profile_created(self):
        """
        Tests that profile is created when user is created.
        """
        self.assertTrue(self.new_user.profile)


class RankTestCase(TestCase):

    def setUp(self):
        self.category_1 = Category.objects.create(name='Category 1', order=1)
        self.subcategory_1 = Subcategory.objects.create(
            parent=self.category_1, name='Subcategory 1', order=1
        )
        self.admin_rank = UserRank.objects.create(
            title='Administrator',
            order=1,
            username_modifier='[color=green]{USER}[/color]',
        )
        self.post_count_rank_1 = UserRank.objects.create(
            title='1 Post Man',
            order=29,
            is_award=True,
            award_type='post_count',
            award_count=1,
        )
        self.post_count_rank_5 = UserRank.objects.create(
            title='5 Post Man',
            order=28,
            is_award=True,
            award_type='post_count',
            award_count=5,
        )
        self.admin_user = get_user_model().objects.create_superuser(
            username='AdminUser',
            email='admin@punkweb.net',
            password='adminboi',
        )
        self.admin_user.profile.ranks.add(self.admin_rank)
        self.admin_thread = Thread.objects.create(
            user=self.admin_user,
            category=self.subcategory_1,
            title='Test Thread',
            content='[b]test[/b]',
        )
        self.new_user = get_user_model().objects.create_user(
            username='NewUser', email='test@punkweb.net', password='testyboi'
        )
        for i in range(10):
            Thread.objects.create(
                user=self.new_user,
                category=self.subcategory_1,
                title='Test Thread {}'.format(i),
                content='[b]test[/b]',
            )

    def test_post_count_rank_awarded(self):
        """
        Tests that post count rank is awarded after creating thread.
        """
        # Test admin_user only has post_count_rank_1
        self.assertTrue(
            self.post_count_rank_1 in self.admin_user.profile.ranks.all()
            and self.post_count_rank_5 not in self.admin_user.profile.ranks.all()
        )
        # Test new_user has both ranks
        self.assertTrue(
            self.post_count_rank_1 in self.new_user.profile.ranks.all()
            and self.post_count_rank_5 in self.new_user.profile.ranks.all()
        )

    def test_rank_order(self):
        """
        Tests that when user has multiple ranks, the correct one shows as the main rank.
        """
        # Test admin_user's main rank is admin_rank
        self.assertTrue(
            self.admin_rank in self.admin_user.profile.ranks.all()
            and self.post_count_rank_1 in self.admin_user.profile.ranks.all()
        )
        self.assertTrue(self.admin_user.profile.rank == self.admin_rank)
        # Test new_user's main rank is 'post_count_rank_5'
        self.assertTrue(
            self.post_count_rank_1 in self.new_user.profile.ranks.all()
            and self.post_count_rank_5 in self.new_user.profile.ranks.all()
        )
        self.assertTrue(self.new_user.profile.rank == self.post_count_rank_5)
