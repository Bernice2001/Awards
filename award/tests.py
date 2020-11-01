from django.test import TestCase

# Create your tests here.
class ProfileTestCase(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='testusereres', password='12345')
        
        self.profile = Profile(user=user, location='Kenya', bio='me..me', avatar='image.jpg')
                
    def test_instance(self):
        self.assertTrue(isinstance(self.profile, Profile))