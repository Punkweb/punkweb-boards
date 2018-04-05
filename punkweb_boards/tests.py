from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.test import TestCase, RequestFactory
from punkweb_boards.models import (
    BoardProfile, UserRank, Category, Subcategory, Thread
)
from punkweb_boards.views import category_detail


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


class CategoryTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.banned_user = get_user_model().objects.create_user(
            username='BannedUser',
            email='banned@punkweb.net',
            password='bannedboi',
        )
        self.banned_user.profile.is_banned = True
        self.banned_user.save()
        self.user = get_user_model().objects.create_user(
            username='TestUser', email='test@punkweb.net', password='testyboi'
        )
        self.category_1 = Category.objects.create(name='Category 1', order=1)
        self.category_2 = Category.objects.create(
            name='Category 2', order=2, auth_req=True
        )

    def test_can_view(self):
        # Anonymous user requests
        anon_request_1 = self.factory.get(self.category_1.get_absolute_url())
        anon_request_1.user = AnonymousUser()
        anon_response_1 = category_detail(anon_request_1, self.category_1.id)
        anon_request_2 = self.factory.get(self.category_2.get_absolute_url())
        anon_request_2.user = AnonymousUser()
        anon_response_2 = category_detail(anon_request_2, self.category_2.id)

        # Banned user requests
        banned_request_1 = self.factory.get(self.category_1.get_absolute_url())
        banned_request_1.user = self.banned_user
        banned_response_1 = category_detail(banned_request_1, self.category_1.id)
        banned_request_2 = self.factory.get(self.category_2.get_absolute_url())
        banned_request_2.user = self.banned_user
        banned_response_2 = category_detail(banned_request_2, self.category_2.id)

        # Authenticated user requests
        auth_request_1 = self.factory.get(self.category_1.get_absolute_url())
        auth_request_1.user = self.user
        auth_response_1 = category_detail(auth_request_1, self.category_1.id)
        auth_request_2 = self.factory.get(self.category_2.get_absolute_url())
        auth_request_2.user = self.user
        auth_response_2 = category_detail(auth_request_2, self.category_2.id)

        self.assertEqual(anon_response_1.status_code, 200)
        self.assertNotEqual(anon_response_2.status_code, 200)
        self.assertNotEqual(banned_response_1.status_code, 200)
        self.assertNotEqual(banned_response_2.status_code, 200)
        self.assertEqual(auth_response_1.status_code, 200)
        self.assertEqual(auth_response_2.status_code, 200)


class SubcategoryTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.banned_user = get_user_model().objects.create_user(
            username='BannedUser',
            email='banned@punkweb.net',
            password='bannedboi',
        )
        self.banned_user.profile.is_banned = True
        self.banned_user.save()
        self.regular_user = get_user_model().objects.create_user(
            username='TestUser', email='test@punkweb.net', password='testyboi'
        )
        self.admin_user = get_user_model().objects.create_superuser(
            username='AdminUser',
            email='admin@punkweb.net',
            password='adminboi',
        )
        self.category_1 = Category.objects.create(name='Category 1', order=1)
        self.category_2 = Category.objects.create(
            name='Category 2', order=2, auth_req=True
        )
        self.cat_1_sub_1 = Subcategory.objects.create(
            parent=self.category_1, name='Subcategory 1', order=1
        )
        self.cat_1_sub_2 = Subcategory.objects.create(
            parent=self.category_1,
            name='Subcategory 2',
            order=2,
            staff_req=True,
        )
        self.cat_1_sub_3 = Subcategory.objects.create(
            parent=self.category_1,
            name='Subcategory 3',
            order=3,
            auth_req=True,
        )
        self.cat_1_sub_4 = Subcategory.objects.create(
            parent=self.category_1,
            name='Subcategory 4',
            order=4,
            staff_req=True,
            auth_req=True,
        )
        self.cat_2_sub_1 = Subcategory.objects.create(
            parent=self.category_2, name='Subcategory 1', order=1
        )
        self.cat_2_sub_2 = Subcategory.objects.create(
            parent=self.category_2,
            name='Subcategory 2',
            order=2,
            staff_req=True,
        )
        self.cat_2_sub_3 = Subcategory.objects.create(
            parent=self.category_2,
            name='Subcategory 3',
            order=3,
            auth_req=True,
        )
        self.cat_2_sub_4 = Subcategory.objects.create(
            parent=self.category_2,
            name='Subcategory 4',
            order=4,
            staff_req=True,
            auth_req=True,
        )

    def test_can_view(self):
        # Test anonymous user
        self.assertTrue(self.cat_1_sub_1.can_view(AnonymousUser()))
        self.assertTrue(self.cat_1_sub_2.can_view(AnonymousUser()))
        self.assertFalse(self.cat_1_sub_3.can_view(AnonymousUser()))
        self.assertFalse(self.cat_1_sub_4.can_view(AnonymousUser()))
        self.assertFalse(self.cat_2_sub_1.can_view(AnonymousUser()))
        self.assertFalse(self.cat_2_sub_2.can_view(AnonymousUser()))
        self.assertFalse(self.cat_2_sub_3.can_view(AnonymousUser()))
        self.assertFalse(self.cat_2_sub_4.can_view(AnonymousUser()))

        # Test banned user
        self.assertFalse(self.cat_1_sub_1.can_view(self.banned_user))
        self.assertFalse(self.cat_1_sub_2.can_view(self.banned_user))
        self.assertFalse(self.cat_1_sub_3.can_view(self.banned_user))
        self.assertFalse(self.cat_1_sub_4.can_view(self.banned_user))
        self.assertFalse(self.cat_2_sub_1.can_view(self.banned_user))
        self.assertFalse(self.cat_2_sub_2.can_view(self.banned_user))
        self.assertFalse(self.cat_2_sub_3.can_view(self.banned_user))
        self.assertFalse(self.cat_2_sub_4.can_view(self.banned_user))

        # Test auth user
        self.assertTrue(self.cat_1_sub_1.can_view(self.regular_user))
        self.assertTrue(self.cat_1_sub_2.can_view(self.regular_user))
        self.assertTrue(self.cat_1_sub_3.can_view(self.regular_user))
        self.assertTrue(self.cat_1_sub_4.can_view(self.regular_user))
        self.assertTrue(self.cat_2_sub_1.can_view(self.regular_user))
        self.assertTrue(self.cat_2_sub_2.can_view(self.regular_user))
        self.assertTrue(self.cat_2_sub_3.can_view(self.regular_user))
        self.assertTrue(self.cat_2_sub_4.can_view(self.regular_user))

    def test_can_post(self):
        # Test anonymous user
        self.assertFalse(self.cat_1_sub_1.can_post(AnonymousUser()))
        self.assertFalse(self.cat_1_sub_2.can_post(AnonymousUser()))
        self.assertFalse(self.cat_1_sub_3.can_post(AnonymousUser()))
        self.assertFalse(self.cat_1_sub_4.can_post(AnonymousUser()))
        self.assertFalse(self.cat_2_sub_1.can_post(AnonymousUser()))
        self.assertFalse(self.cat_2_sub_2.can_post(AnonymousUser()))
        self.assertFalse(self.cat_2_sub_3.can_post(AnonymousUser()))
        self.assertFalse(self.cat_2_sub_4.can_post(AnonymousUser()))

        # Test banned user
        self.assertFalse(self.cat_1_sub_1.can_post(self.banned_user))
        self.assertFalse(self.cat_1_sub_2.can_post(self.banned_user))
        self.assertFalse(self.cat_1_sub_3.can_post(self.banned_user))
        self.assertFalse(self.cat_1_sub_4.can_post(self.banned_user))
        self.assertFalse(self.cat_2_sub_1.can_post(self.banned_user))
        self.assertFalse(self.cat_2_sub_2.can_post(self.banned_user))
        self.assertFalse(self.cat_2_sub_3.can_post(self.banned_user))
        self.assertFalse(self.cat_2_sub_4.can_post(self.banned_user))

        # Test regular user
        self.assertTrue(self.cat_1_sub_1.can_post(self.regular_user))
        self.assertFalse(self.cat_1_sub_2.can_post(self.regular_user))
        self.assertTrue(self.cat_1_sub_3.can_post(self.regular_user))
        self.assertFalse(self.cat_1_sub_4.can_post(self.regular_user))
        self.assertTrue(self.cat_2_sub_1.can_post(self.regular_user))
        self.assertFalse(self.cat_2_sub_2.can_post(self.regular_user))
        self.assertTrue(self.cat_2_sub_3.can_post(self.regular_user))
        self.assertFalse(self.cat_2_sub_4.can_post(self.regular_user))

        # Test superuser
        self.assertTrue(self.cat_1_sub_1.can_post(self.admin_user))
        self.assertTrue(self.cat_1_sub_2.can_post(self.admin_user))
        self.assertTrue(self.cat_1_sub_3.can_post(self.admin_user))
        self.assertTrue(self.cat_1_sub_4.can_post(self.admin_user))
        self.assertTrue(self.cat_2_sub_1.can_post(self.admin_user))
        self.assertTrue(self.cat_2_sub_2.can_post(self.admin_user))
        self.assertTrue(self.cat_2_sub_3.can_post(self.admin_user))
        self.assertTrue(self.cat_2_sub_4.can_post(self.admin_user))
