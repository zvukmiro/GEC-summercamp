import datetime
from django.test import TestCase
from django.contrib.auth import get_user_model

from camplist.models import Child, CampWeek, CampPrice, CampTheme

class ChildModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        p = CampPrice.objects.create(duration_in_days = '4', price_in_dollars = 100)
        w = CampWeek.objects.create(week_num = 8, date_start = datetime.date(2019, 6, 25), date_end = datetime.date(2019, 6, 30))
        camp = CampTheme.objects.create(
            theme = 'summer1', field_trip = 'PumpItUp', summary = 'description',
            week_date = w, price = p
            )
        User = get_user_model()
        user = User.objects.create_user(
            username='norma', email='normal@user.com', password='foo',
            first_name='Norma', last_name='Smith', address='Rudy Dr, San Jose, CA', phone='4089995959')

        ch = Child.objects.create(
            first_name = 'Lea', last_name = 'Dobro', dob = '2002-03-29', grade_in_fall = 1,
            parent = user,
            )

        #ch.camps.add(camp)
        camp.camper.add(ch)
        camp.save()

        # here create children and create camps, Child.objects.create(first_name='Lena')
        # then reference it by Child.objects.get(first_name='Lena')

    #def test_check_start_end(self): did not work,
    #    w = CampWeek.objects.create(week_num = 8, date_start = datetime.date(2019, 6, 30), date_end = datetime.date(2019, 6, 29))
    #    self.assertRaises(w.check_start_end, ValidationError('Invalid dates.'))
    # testing CampPrice
    def test_camp_price_days(self):
        price =  CampPrice.objects.get(id=1)
        self.assertEqual(price.duration_in_days, 4)

    def test_camp_price_dollars(self):
        price =  CampPrice.objects.get(id=1)
        self.assertEqual(price.price_in_dollars, 100)

    def test_camp_price_str(self):
        price =  CampPrice.objects.get(id=1)
        expected_object_name = f'${price.price_in_dollars} for {price.duration_in_days} days'
        self.assertEqual(expected_object_name, str(price))

    # testing CampWeek
    def test_camp_week_num(self):
        week = CampWeek.objects.get(id=1)
        self.assertEqual(week.week_num, 8)

    def test_camp_week_start(self):
        week = CampWeek.objects.get(id=1)
        self.assertNotEqual(week.date_start, datetime.date(2018, 6, 25))

    def test_camp_week_end(self):
        week = CampWeek.objects.get(id=1)
        self.assertEqual(week.date_end, datetime.date(2019, 6, 30))

    def test_camp_week_str(self):
        week =  CampWeek.objects.get(id=1)
        expected_object_name = f'week #{week.week_num} ({week.date_start}  to  {week.date_end})'
        self.assertEqual(expected_object_name, str(week))
#        return f'week #{ self.week_num } ({ self.date_start }  to  { self.date_end })'

    #testing CampTheme
    def test_camp_theme_theme(self):
        c_theme = CampTheme.objects.get(id=1)
        self.assertEqual(c_theme.theme, 'summer1')

    def test_camp_theme_field_trip(self):
        c_theme = CampTheme.objects.get(id=1)
        self.assertEqual(c_theme.field_trip, 'PumpItUp')

    def test_camp_theme_summary(self):
        c_theme = CampTheme.objects.get(id=1)
        self.assertEqual(c_theme.summary, 'description')


    def test_camp_theme_week_weeknum(self):
        week = CampWeek.objects.get(id=1)
        camp = CampTheme.objects.get(id=1)
        self.assertEqual(week.week_num, camp.week_date.week_num)

    def test_camp_theme_week_price(self):
        price = CampPrice.objects.get(id=1)
        camp = CampTheme.objects.get(id=1)
        self.assertEqual(price.price_in_dollars, camp.price.price_in_dollars)

    def test_camp_theme_week_str(self):
        price = CampPrice.objects.get(id=1)
        c_theme = CampTheme.objects.get(id=1)
        expected_string = f'{c_theme.theme} ({c_theme.week_date})'
        self.assertEqual(expected_string, str(c_theme))

    def test_camp_theme_get_absolute_url(self):
        camp = CampTheme.objects.get(id=1)        # This will also fail if the urlconf is not defined.
        self.assertEqual(camp.get_absolute_url(), '/camplist/camps/1')

    # testing Child
    def test_first_name_child(self):
        child = Child.objects.get(id=1)
        first = child.first_name
        self.assertEqual(first, 'Lea')

    def test_last_name_child(self):
        child = Child.objects.get(id=1)
        last = child.last_name
        self.assertEqual(last, 'Dobro')

    def test_date_of_birth_child(self):
        child = Child.objects.get(id=1)
        dob = child.dob
        self.assertEqual(dob, datetime.date(2002, 3, 29))


    def test_grade_in_fall_child(self):
        child = Child.objects.get(id=1)
        grade = child.grade_in_fall
        self.assertEqual(grade, '1')

    def test_camps_field_child(self):
         child = Child.objects.get(id=1)
         campN = CampTheme.objects.get(id=1)
         camps = child.display_camps()
         self.assertEqual(camps, campN.theme)

    def test_parent_child(self):
        User = get_user_model()
        child = Child.objects.get(id=1)
        parentUsername = child.parent.username
        parent = User.objects.get(id=1)
        self.assertEqual(parentUsername, parent.username)


    def test_parent_count_child(self):
        User = get_user_model()
        parent = User.objects.get(id=1)
        numberCh = parent.children.count()
        self.assertEqual(numberCh, 1)

    def test_child_name_str(self):
        child = Child.objects.get(id=1)
        expected_object_name = f'{child.first_name} {child.last_name} dob: {child.dob}'
        self.assertEqual(expected_object_name, str(child))

    def test_get_absolute_url_child(self):
        child = Child.objects.get(id=1)        # This will also fail if the urlconf is not defined.
        self.assertEqual(child.get_absolute_url(), '/camplist/child/1')
