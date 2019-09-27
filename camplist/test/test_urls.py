from django.test import SimpleTestCase

from django.urls import reverse, resolve
from camplist import views

class TestUrls(SimpleTestCase):

    def test_camp_list_url_resolves(self):
        url = reverse('camps')
        self.assertEquals(resolve(url).func.view_class, views.CampThemeListView)

    def test_camp_detail_url_resolves(self):
        url = reverse('camp-detail', args=['2'])
        self.assertEquals(resolve(url).func.view_class, views.CampThemeDetailView)

    def test_parent_detail_url_resolves(self):
        url = reverse('parent-detail', args=['2'])
        self.assertEquals(resolve(url).func.view_class, views.ParentDetailView)

    def test_detail_url_resolves(self):
        url = reverse('child-detail', args=['4'])
        self.assertEquals(resolve(url).func, views.child_detail)

    def test_add_url_resolves(self):
        url = reverse('add-child')
        self.assertEquals(resolve(url).func.view_class, views.ChildCreate )

    def test_edit_url_resolves(self):
        url = reverse('edit-child', args=['4'])
        self.assertEquals(resolve(url).func.view_class, views.ChildUpdate )

    def test_delete_url_resolves(self):
        url = reverse('delete-child', args=['4'])
        self.assertEquals(resolve(url).func.view_class, views.ChildDelete )
