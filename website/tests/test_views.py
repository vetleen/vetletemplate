from django.test import TestCase
from django.test import SimpleTestCase
from django.urls import reverse

from django.test import Client
from website.forms import ChangePasswordForm, SignUpForm, LoginForm, EditAccountForm

from django.contrib.auth.models import AnonymousUser, User
from django.contrib import auth

def yellow(message):
    ''' A custom function that sets strings meant for the consoll to yellow so that they stand out'''
    return '\n' + '\033[1;33;40m ' + message + '\x1b[0m'

# Create your tests here.
class TestThatUrlsExist(TestCase):
    """
    Test that URLs yield expected response
    """
    def test_url_status(self):
        """
        TEST THAT ALL URLS LEAD SOMEWHERE
        """
        ## Set the conditions for URL-testing
        self.urls_to_test = [
            '/',
            '/sign-up/',
            '/change-password/',
            '/login/',
            '/logout/',
            '/edit-account/',
            '/dashboard/',

            ]
        self.acceptable_url_statuses = [200]

        #test that URLs exist
        for url in self.urls_to_test:
            response = self.client.get(url, follow=True)
            my_message = 'TestThatUrlsExist: the url: \'%s\' gave the wrong status code (%s).'%(url, response.status_code)
            self.assertIn(response.status_code, self.acceptable_url_statuses, yellow(my_message))

class IndexViewTest(TestCase):
    ''' TESTS THAT THE FRONT PAGE BEHAVES PROPERLY '''
    def setUp(self):
        User.objects.create_user(   'macgyver@phoenix.com',
                                    'macgyver@phoenix.com',
                                    'anguspassword'
                                    )
        User.objects.create_user(   'thornton@phoenix.com',
                                    'thornton@phoenix.com',
                                    'petepassword'
                                    )
    def test_index_can_be_loaded(self):
        response = self.client.get('/', follow=True)
        my_message = yellow('Couldn\'t find the front page at \'/\'')
        self.assertTemplateUsed(response, 'index.html', my_message)
    def test_authenticated_users_get_rd_to_dashboard(self):
        #log in
        self.credentials = {
            'username': 'macgyver@phoenix.com',
            'password': 'anguspassword'
            }
        login_response = self.client.post('/login/', self.credentials, follow=True)
        #try go to front page
        response = self.client.post('/', self.credentials, follow=True)
        #assert get dashboard
        my_message = yellow(' Active user was not correctly redirected when trying to reach front page: ')
        self.assertRedirects(response, '/dashboard/', 302, 200, msg_prefix=my_message)
        #assert correct template
        self.assertTemplateNotUsed(response, 'index.html', my_message)
        self.assertTemplateUsed(response, 'dashboard.html', my_message)

class LoginViewTest(TestCase):
    """
    TEST THE LOG IN VIEW IN EVERY WHICH WAY
    """
    def setUp(self):
        User.objects.create_user(   'lennon@thebeatles.com',
                                    'lennon@thebeatles.com',
                                    'johnpassword'
                                    )
        User.objects.create_user(   'lennon@thebeatles2.com',
                                    'lennon@thebeatles2.com',
                                    'johnpassword2'
                                    )

    ### TESTS FOR IF USER IS ALREADY LOGGED IN ###
    def test_active_users_given_correct_template_and_a_message(self):
        #correct credentials
        self.credentials = {
            'username': 'lennon@thebeatles.com',
            'password': 'johnpassword'
            }
        #Login
        response = self.client.post('/login/', self.credentials, follow=True)
        #check that it worked
        self.assertTrue(response.context['user'].is_active)
        #try go to login page again
        response = self.client.get('/login/', follow=True)
        messages = list(response.context['messages'])

        my_message = 'LoginViewTest: A logged in user was not given exactly 1 messages as expected, but %s.'%(len(messages))
        self.assertEqual(len(messages), 1, yellow(my_message))

        my_message = 'LoginViewTest: An already logged in user was correct template at /login/.'
        self.assertTemplateUsed(response, 'you_did_something.html', yellow(my_message))

    ### TESTS FOR GET ###
    def test_correct_form_and_template_is_used(self):
        ''' Test that a GET request is met with the correct form and template '''
        response = self.client.get('/login/', follow=True)
        received_form = response.context['form']
        #print(response.context)
        my_message = yellow('LoginViewTest: %s was not the expected object'% (received_form))
        self.assertEqual(received_form, LoginForm, my_message)
        my_message = yellow('LoginViewTest: An anonymous user was not shown the correct template at /login/.')
        self.assertTemplateUsed(response, 'login_form.html', my_message)

    ### TESTS FOR  POST ###
    def test_login_works(self):
        ''' Test that login works with valid credentials '''
        self.credentials = {
            'username': 'lennon@thebeatles.com',
            'password': 'johnpassword'
            }
        #user = User.objects.get(username='lennon@thebeatles.com')
        response = self.client.post('/login/', self.credentials, follow=True)
        # should be logged in now
        my_message = yellow('LoginViewTest: User was not logged in as expected')
        self.assertTrue(response.context['user'].is_active, my_message)
        my_message = yellow('LoginViewTest: The \"active\" user was not the expected user.')
        self.assertEqual(response.context['user'], User.objects.get(username='lennon@thebeatles.com'), my_message)

        messages = list(response.context['messages'])
        #my_message = 'User was not given exactly 1 messages as expected after he loged in, but %s.'%(len(messages))
        #self.assertEqual(len(messages), 4, yellow(my_message))
        my_message = yellow('LoginViewTest: User was not correctly redirected after login')
        self.assertRedirects(response, '/dashboard/', 302, 200, msg_prefix=my_message)
        #SimpleTestCase.assertContains(response, text, count=None, status_code=200, msg_prefix='', html=False)
        my_message = yellow('LoginViewTest: After login the expected "You have logged in."-text did not show')
        self.assertContains(response, 'You have logged in.', msg_prefix=my_message)

    def test_login_does_not_work_for_unathorized(self):
        ''' Test that login doesnt work with invalid credentials '''

        self.credentials = {
            'username': 'lennon@thebeatles.com', #existing
            'password': 'elvispassword' #wrong
            }
        response = self.client.post('/login/', self.credentials, follow=True)
        # should NOT be logged in now
        my_message = yellow('LoginViewTest: User was logged in mysteriously, despite submitting the wrong password')
        self.assertFalse(response.context['user'].is_active, my_message)

        #and should get the login form again:
        received_form = response.context['form']
        #print(response.context)
        my_message = yellow('LoginViewTest: %s was not an insatnce ofg LoginForm. A user giving the wrong password was supposed to get the form anew.'% (received_form))
        self.assertIsInstance(received_form, LoginForm, my_message)
        my_message = yellow('LoginViewTest: A user giving the wrong password was not shown the correct template at /login/.')
        self.assertTemplateUsed(response, 'login_form.html', my_message)

class LogoutViewTest(TestCase):
    """
    TEST THE LOGOUT VIEW IN EVERY WHICH WAY
    """
    def setUp(self):
        User.objects.create_user(   'lennon@thebeatles.com',
                                    'lennon@thebeatles.com',
                                    'johnpassword'
                                    )
        User.objects.create_user(   'lennon@thebeatles2.com',
                                    'lennon@thebeatles2.com',
                                    'johnpassword2'
                                    )
    def test_logout(self):
        #correct credentials
        self.credentials = {
            'username': 'lennon@thebeatles.com',
            'password': 'johnpassword'
            }
        #Login
        response = self.client.post('/login/', self.credentials, follow=True)
        #check that it worked
        my_message = yellow('TestLogoutView: User was supposed to be logged in' )
        self.assertTrue(response.context['user'].is_active, my_message)
        #try logout
        response = self.client.get('/logout/', follow=True)
        my_message = yellow('TestLogoutView: User was supposed to be logged out after visiting /logout/' )
        self.assertFalse(response.context['user'].is_active, my_message)
        my_message = 'TestLogoutView: After logout user was supposed to find a different template.'
        self.assertTemplateUsed(response, 'logout_complete.html', yellow(my_message))
        my_message = yellow('TestLogoutView: After logout the expected "You have logged out successfully."-text did not show')
        self.assertContains(response, 'You have logged out successfully.', msg_prefix=my_message)


class ChangePasswordViewTest(TestCase):
    """
    TEST THE CHANGE PASSWORD VIEW IN EVERY WHICH WAY
    """
    def setUp(self):
        User.objects.create_user(   'lennon@thebeatles.com',
                                    'lennon@thebeatles.com',
                                    'johnpassword'
                                    )
        User.objects.create_user(   'lennon@thebeatles2.com',
                                    'lennon@thebeatles2.com',
                                    'johnpassword2'
                                    )
    def test_that_login_is_required(self):
        #Test that login is required
        response = self.client.get('/change-password/', follow=True)
        my_message = yellow('ChangePasswordViewTest: anonymous users should be redirected when attempting to GET at this address')
        self.assertRedirects(response, '/login/?next=/change-password/', 302, 200, msg_prefix=my_message)
        response = self.client.post('/change-password/', follow=True)
        my_message = yellow('ChangePasswordViewTest: anonymous users should be redirected when attempting to POST to this address')
        self.assertRedirects(response, '/login/?next=/change-password/', 302, 200, msg_prefix=my_message)

    def test_get_requests(self):
        #correct credentials
        self.credentials = {
            'username': 'lennon@thebeatles.com',
            'password': 'johnpassword'
            }
        #Login
        response = self.client.post('/login/', self.credentials, follow=True)
        #check that it worked
        my_message = yellow('ChangePasswordViewTest: User was supposed to be logged in' )
        self.assertTrue(response.context['user'].is_active, my_message)
        #Test GET works
        response = self.client.get('/change-password/', follow=True)
        ##correct template
        my_message = 'ChangePasswordViewTest: Should use template "change_password_form.html".'
        self.assertTemplateUsed(response, 'change_password_form.html', yellow(my_message))
        ##correct form
        my_message = 'ChangePasswordViewTest: Expected ChangePasswordForm to be available in context.'
        self.assertEqual(response.context['form'], ChangePasswordForm, my_message)

    def test_post_requests(self):
        #correct credentials
        self.credentials = {
            'username': 'lennon@thebeatles.com',
            'password': 'johnpassword'
            }
        #Login
        response = self.client.post('/login/', self.credentials, follow=True)
        #check that it worked
        my_message = yellow('ChangePasswordViewTest: User was supposed to be logged in' )
        self.assertTrue(response.context['user'].is_active, my_message)
        ###Test POST works
        #wrong input in all fields
        response = self.client.post('/change-password/', {'old_password': "", 'new_password': "", 'confirm_new_password': ""}, follow=True)
        my_message = yellow('ChangePasswordViewTest: %s should be an instance of ChangePasswordForm.'%(response.context['form']))
        received_form = response.context['form']
        self.assertIsInstance(received_form, ChangePasswordForm, my_message)
        my_message = yellow('ChangePasswordViewTest: should use change_password_form-html template.')
        self.assertTemplateUsed(response, 'change_password_form.html', my_message)

        #correct input in all fields
        response = self.client.post('/change-password/', {'old_password': "johnpassword", 'new_password': "newjohnpassword", 'confirm_new_password': "newjohnpassword"}, follow=True)
        my_message = yellow('ChangePasswordViewTest: %s should not be a bound instance of ChangePasswordForm, but point directly at it.'%(response.context['form']))
        received_form = response.context['form']
        self.assertEqual(received_form, ChangePasswordForm, my_message)
        my_message = yellow('ChangePasswordViewTest: should use change_password_form-html template.')
        self.assertTemplateUsed(response, 'change_password_form.html', my_message)
        #gotta check the user is still logged in:
        self.assertTrue(response.context['user'].is_active)
        #print("checking password for user after first change (correctly done): should be F-T-F-F")
        #print(response.context['user'])
        #print(response.context['user'].check_password('johnpassword'))
        #print(response.context['user'].check_password('newjohnpassword'))
        #print(response.context['user'].check_password('randompassword'))
        #print(response.context['user'].check_password('evennewerjohnpassword'))
        #should stil use the right template
        my_message = 'ChangePasswordViewTest: Should use template "change_password_form.html".'
        self.assertTemplateUsed(response, 'change_password_form.html', yellow(my_message))
        #Are passwords correctly updated?
        my_message = yellow('ChangePasswordViewTest: password should be changed')
        self.assertFalse(response.context['user'].check_password('johnpassword'), my_message)
        self.assertTrue(response.context['user'].check_password('newjohnpassword'), my_message)

        #Are passwords incorrectly updated when you provide the wrong passowrd?
        response = self.client.post('/change-password/', {'old_password': "ggg", 'new_password': "ejpassword", 'confirm_new_password': "ejpassword"}, follow=True)
        #print("checking password for user after second change (incorrectly done): should be F-T-F-F (passw-change didnt work) OR F-F-F-T (passw-change worked)")
        #print(response.context['user'])
        #print(response.context['user'].check_password('johnpassword'))
        #print(response.context['user'].check_password('newjohnpassword'))
        #print(response.context['user'].check_password('randompassword'))
        #print(response.context['user'].check_password('ejpassword'))
        my_message = yellow('ChangePasswordViewTest: password should NOT be changed.')
        self.assertFalse(response.context['user'].check_password('ejpassword'), my_message)
        self.assertTrue(response.context['user'].check_password('newjohnpassword'), my_message)
        #should stil use the right template
        my_message = 'ChangePasswordViewTest: Should use template "change_password_form.html".'
        self.assertTemplateUsed(response, 'change_password_form.html', yellow(my_message))
