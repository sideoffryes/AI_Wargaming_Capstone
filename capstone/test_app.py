import unittest
from app import app
import json
import requests

class FlaskTestCase(unittest.TestCase):
    
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_index_page(self):
        # Send a GET request to the index page
        response = self.client.get('/index')
        
        # Check that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)
        
        # Check that the title is present
        self.assertIn(b'<title>Capstone Starter</title>', response.data)

        # Check that the form and input fields are present
        self.assertIn(b'<form action="/handle_indexPost" method="POST">', response.data)

        self.assertIn(b'<label for="artifact_type">Artifact Options:</label>', response.data)
        self.assertIn(b'<select id="artifact_type" name="artifact_type">', response.data)
        self.assertIn(b'<option value="1">DEBUG ARTIFACT</option>', response.data)
        self.assertIn(b'<option value="2">NAVADMIN</option>', response.data)
        self.assertIn(b'<option value="3">MARADMIN</option>', response.data)
        self.assertIn(b'<option value="4">OPORD</option>', response.data)

        self.assertIn(b'<label for="model_selection">LLM Model Options:</label>', response.data)
        self.assertIn(b'<option value="1">Llama-3.2-1B-Instruct</option>', response.data)
        self.assertIn(b'<option value="2">Llama-3.2-3B-Instruct</option>', response.data)
        self.assertIn(b'<option value="3">Llama-3.1-8B-Instruct</option>', response.data)
        self.assertIn(b'<option value="4">Llama-3.3-70B-Instruct</option>', response.data)
        
        # Instead of checking for the exact textarea, check for the presence of a form field
        self.assertIn(b'<textarea class ="my_text" id="artifact_parameters" name="artifact_parameters" wrap="hard"></textarea>', response.data)
        
        # Check for the dropdown menu items
        self.assertIn(b'Generate Document', response.data)
        self.assertIn(b'Login', response.data)
        self.assertIn(b'User Profile', response.data)
        self.assertIn(b'Documentation', response.data)

        # Check for the {{ errorMsg }} being empty because there should be no error in this case
        self.assertIn(b'<p></p>', response.data)

        # Send a GET request to the index page again and test all again
        response = self.client.get('/')
        
        # Check that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)
        
        # Check that the title is present
        self.assertIn(b'<title>Capstone Starter</title>', response.data)

        # Check that the form and input fields are present
        self.assertIn(b'<form action="/handle_indexPost" method="POST">', response.data)

        self.assertIn(b'<label for="artifact_type">Artifact Options:</label>', response.data)
        self.assertIn(b'<select id="artifact_type" name="artifact_type">', response.data)
        self.assertIn(b'<option value="1">DEBUG ARTIFACT</option>', response.data)
        self.assertIn(b'<option value="2">NAVADMIN</option>', response.data)
        self.assertIn(b'<option value="3">MARADMIN</option>', response.data)
        self.assertIn(b'<option value="4">OPORD</option>', response.data)

        self.assertIn(b'<label for="model_selection">LLM Model Options:</label>', response.data)
        self.assertIn(b'<option value="1">Llama-3.2-1B-Instruct</option>', response.data)
        self.assertIn(b'<option value="2">Llama-3.2-3B-Instruct</option>', response.data)
        self.assertIn(b'<option value="3">Llama-3.1-8B-Instruct</option>', response.data)
        self.assertIn(b'<option value="4">Llama-3.3-70B-Instruct</option>', response.data)
        
        # Instead of checking for the exact textarea, check for the presence of a form field
        self.assertIn(b'<textarea class ="my_text" id="artifact_parameters" name="artifact_parameters" wrap="hard"></textarea>', response.data)
        
        # Check for the dropdown menu items
        self.assertIn(b'Generate Document', response.data)
        self.assertIn(b'Login', response.data)
        self.assertIn(b'User Profile', response.data)
        self.assertIn(b'Documentation', response.data)

        # Check for the {{ errorMsg }} being empty because there should be no error in this case
        self.assertIn(b'<p></p>', response.data)

    def test_output_page(self):
        # Send a GET request to the output page
        response = self.client.get('/output')

        # Check that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Check that the title is present
        self.assertIn(b'<title>AI Wargaming</title>', response.data)

        # Check for the dropdown menu items
        self.assertIn(b'Generate Document', response.data)
        self.assertIn(b'Login', response.data)
        self.assertIn(b'User Profile', response.data)
        self.assertIn(b'Documentation', response.data)

        # Check for output
        self.assertIn(b'<div id="ai-output">You selected: </div>', response.data)
        self.assertIn(b'<div id="ai-output">You gave the following prompt: </div>', response.data)
        self.assertIn(b'<div id="ai-output">Output: </div>', response.data)

    def test_login_page(self):
        # Send a GET request to the output page
        response = self.client.get('/login')

        # Check that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Check that the title is present
        self.assertIn(b'<title>Login Form</title>', response.data)

        # Check for the dropdown menu items
        self.assertIn(b'Generate Document', response.data)
        self.assertIn(b'Login', response.data)
        self.assertIn(b'User Profile', response.data)
        self.assertIn(b'Documentation', response.data)

        # Check for form
        self.assertIn(b'<form action="/handle_loginPost" method="POST">', response.data)
        self.assertIn(b'<input type="text" id="username" name="username" required>', response.data)
        self.assertIn(b'<input type="password" id="password" name="password" required>', response.data)

        # check for create new account
        self.assertIn(b'<a href="/new_account" class="button">Create Account</a>', response.data)

        # Check for the {{ errorMsg }} being empty because there should be no error in this case
        self.assertIn(b'<p></p>', response.data)

    def test_my_artifacts_logged_out(self):
        # Send a GET request to the artifacts page
        response = self.client.get('/my_artifacts')

        # Check that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Check that the title is is now Login From because user is not logged in
        self.assertIn(b'<title>Login Form</title>', response.data)

        # Check for the error message
        self.assertIn(b'NOTICE: Please login to see your generated artifacts.', response.data)

    def test_new_account(self):
        # Send a GET request to the new account page
        response = self.client.get('/new_account')

        # Check that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Check that the title is present
        self.assertIn(b'<title>Account Creation</title>', response.data)

        # Check for the dropdown menu items
        self.assertIn(b'Generate Document', response.data)
        self.assertIn(b'Login', response.data)
        self.assertIn(b'User Profile', response.data)
        self.assertIn(b'Documentation', response.data)

        # Check for form
        self.assertIn(b'<form action="/handle_registerPost" method="POST">', response.data)
        self.assertIn(b'<input type="text" id="username" name="username" required>', response.data)
        self.assertIn(b'<input type="password" id="ogpassword" name="ogpassword" required>', response.data)
        self.assertIn(b'<input type="password" id="repassword" name="repassword" required>', response.data)

        # Check for the {{ errorMsg }} being empty because there should be no error in this case
        self.assertIn(b'<p></p>', response.data)

    def test_logout(self):
        # Send a GET request to logout
        response = self.client.get('/logout')

        # Check that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Check that the title is present
        self.assertIn(b'<title>Capstone Starter</title>', response.data)

        # Check for the {{ errorMsg }}
        self.assertIn(b'Successfully logged out of profile', response.data)

    def test_handle_indexPost(self):
        # Data that simulates what would be entered in the form
        form_data = {
            'artifact_type': '1',  # DEBUG ARTIFACT
            'model_selection': '2',  # Llama-3.1-8B-Instruct
            'artifact_parameters': 'Some additional parameters for artifact'
        }

        # Simulate the POST request to the '/index' route with the form data
        response = self.client.post('/index', data=form_data)

        # Assert that the response is a redirect (302) after form submission
        self.assertEqual(response.status_code, 302)  # HTTP 302 for redirect

        # Optionally, you can check that the redirect is happening to the correct page (e.g., '/index')
        self.assertRedirects(response, '/index')

        # Optionally, you can assert that the data is being processed correctly
        # For example, check the content of the redirected page or other actions

        # Verify the data was processed by checking for specific changes, such as:
        # - Creation of a new object
        # - A specific error message or message indicating successful submission
        
if __name__ == '__main__':
    unittest.main()