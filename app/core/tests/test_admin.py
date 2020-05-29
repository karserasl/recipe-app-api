# @Author: Administrator
# @Date:   29/05/2020 15:13


from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse


class AdminSiteTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@example.com',
            password='test123456',
        )
        # Helper function to force login the user.
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email='user@example.com',
            password='test123',
            name='Test user',
        )

    def test_users_listed(self):
        """Test that users are listed on the user page"""
        # Defined in Django admin docs. It autogenerates the url,
        # so we dont have to change it everywhere.
        url = reverse('admin:core_user_changelist')
        res = self.client.get(url)

        # Check if HTTP 200 and if the result from the url is included in.
        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    def test_user_change_page(self):
        """Test the user edit page"""
        url = reverse('admin:core_user_change', args=[self.user.id])
        # /admin/core/user/{id}/
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_user_page_create(self):
        """Create user page works"""
        url = reverse('admin:core_user_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
