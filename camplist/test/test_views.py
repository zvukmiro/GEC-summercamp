import datetime
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from camplist.models import CampTheme, CampWeek, CampPrice, Child

class CampThemeListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create 5 camps
        number_of_camps = 5
        for campw_id in range(1, number_of_camps+1):
            week = CampWeek.objects.create(
                week_num = campw_id,
                date_start = datetime.date(2019, 6, 25),
                date_end = datetime.date(2019, 6, 30)
            )
            price = CampPrice.objects.create(
                duration_in_days=campw_id,
                price_in_dollars=100*campw_id,
            )


        for camptheme_id in range(1, number_of_camps+1):
            CampTheme.objects.create(
                theme=f'summer {camptheme_id}',
                field_trip=f'field trip number {camptheme_id}',
                summary=f'summary {camptheme_id}',
                week_date= CampWeek.objects.get(week_num=camptheme_id),
                price=CampPrice.objects.get(duration_in_days=camptheme_id)
            )
# 3 tests for camp views info
    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/camplist/camps/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('camps'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('camps'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'camplist/camptheme_list.html')

# do not need to instatiet client=Client(), just refer to self.client, in anytest


class ChildViewsTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        User = get_user_model()

        cls.test_user1 = User.objects.create(
            username='testuser1',
            email='normal1@user.com',
            first_name='Norma1',
            last_name='Smith',
            address='Rudy Dr, San Jose, CA',
            phone='4089995959')
        cls.test_user1.set_password('1X<ISRUkw+tuK')

        cls.test_user2 = User.objects.create(
            username='testuser2',
            password='2HJ1vRV0Z&3iD',
            email='normal2@user.com',
            first_name='Norma2',
            last_name='Smith',
            address='Rudy Dr, San Jose, CA',
            phone='4089995959')


        cls.test_user1.save()
        cls.test_user2.save()

        # Create a child
        cls.test_child1 = Child.objects.create(
            first_name = 'Lea1', last_name = 'Dobro1', dob = '2001-03-29', grade_in_fall = 1,
            parent = cls.test_user1,
            )

        cls.test_child2 = Child.objects.create(
            first_name = 'Lea2', last_name = 'Dobro2', dob = '2002-03-29', grade_in_fall = 2,
            parent = cls.test_user2,
            )
        cls.test_child3 = Child.objects.create(
            first_name = 'Lea3', last_name = 'Dobro3', dob = '2003-03-29', grade_in_fall = 3,
            parent = cls.test_user1,
            )
        cls.test_child4 =Child.objects.create(
            first_name = 'Lea4', last_name = 'Dobro4', dob = '2004-03-29', grade_in_fall = 4,
            parent = cls.test_user2,
            )
        number_of_camps = 5
        for campw_id in range(1, number_of_camps+1):
            week = CampWeek.objects.create(
                week_num = campw_id,
                date_start = datetime.date(2019, 6, 25),
                date_end = datetime.date(2019, 6, 30)
            )
            price = CampPrice.objects.create(
                duration_in_days=campw_id,
                price_in_dollars=100*campw_id,
            )


        for camptheme_id in range(1, number_of_camps+1):
            CampTheme.objects.create(
                theme=f'summer {camptheme_id}',
                field_trip=f'field trip number {camptheme_id}',
                summary=f'summary {camptheme_id}',
                week_date= CampWeek.objects.get(week_num=camptheme_id),
                price=CampPrice.objects.get(duration_in_days=camptheme_id)
            )


        # Create child camps as a post-step
        camps_objects_for_child = CampTheme.objects.all()
        cls.test_child1.camps.set(camps_objects_for_child) # Direct assignment of many-to-many types not allowed.
        cls.test_child1.save()

        camps_objects_for_child2 = CampTheme.objects.filter(id=2)
        cls.test_child2.camps.set(camps_objects_for_child2)
        cls.test_child2.save()


        camps_objects_for_child3 = CampTheme.objects.filter(id=3)
        cls.test_child3.camps.set(camps_objects_for_child3)
        cls.test_child3.save()


        camps_objects_for_child4 = CampTheme.objects.filter(id=4)
        cls.test_child4.camps.set(camps_objects_for_child4)
        cls.test_child4.save()

# child view 8 tests
    def test_logged_in_view_url_exists_for_child_at_loc(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get('/camplist/child/1')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/camplist/child/3')
        self.assertEqual(response.status_code, 200)

    def test_logged_in_view_url_accessible_by_name(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        self.assertTrue(login)
        response = self.client.get(reverse('child-detail', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)


    def test_logged_in_view_uses_correct_template_detail(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')

        response = self.client.get(reverse('child-detail', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'camplist/child_detail.html')

    def test_parent_not_logged_in_view_uses_template_error(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        # testuser1 is not a parent of child 2
        response = self.client.get(reverse('child-detail', kwargs={'pk': 2}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'camplist/error.html')

    def test_logged_in_view_uses_correct_template_edit(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')

        response = self.client.get(reverse('edit-child', kwargs={'pk': 3}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'camplist/edit_child.html')

    def test_logged_in_view_uses_correct_template_delete(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')

        response = self.client.get(reverse('delete-child', kwargs={'pk': 3}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'camplist/child_confirm_delete.html')

    def test_not_logged_in_view_uses_correct_template_edit(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        # testuser1 is not a parent of the child with id 2
        response = self.client.get(reverse('edit-child', kwargs={'pk': 2}))
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, '404.html')

    def test_not_logged_in_view_uses_correct_template_delete(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        # testuser1 is not a parent of the child with id 2
        response = self.client.get(reverse('delete-child', kwargs={'pk': 2}))
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, '404.html')
