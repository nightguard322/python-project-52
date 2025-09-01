from django.test import TestCase, Client

# Create your tests here.

# class UnregisterUserTestCase(TestCase):
    
#     def SetUp(self):
#         self.user = User.objects.create_user(
#             username='Vasya',
#             first_name='Vasya',
#             last_name = 'Pupkin',
#             password='Qq12345'
#         )


#     def testUserListAccess(self):
#         response = self.client.get('/accounts')
#         self.assertEqual(response.status_code, 200)
#         self.assertContains(response, 'Vasya Pupkin')

    # def testUserNotAllowedToActions(self):
    #     response = self.client.post(
    #         '/accounts/{self.user.id}/update',
    #         {'username': 'new Vasya'},
    #         follow=True
    #     )
    #     self.assertRedirect(
    #         response,
    #         expected_url=reverse('login'),
    #         status_code=302
    #     )

