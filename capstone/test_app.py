import unittest
from app import app

class FlaskTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_index(self):
        # Send a GET request to the index page
        response = self.client.get('/index')
        
        # Check that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)
        
        # Check that the title is present
        self.assertIn(b'<title>Capstone Starter</title>', response.data)

        # Check that the form and input fields are present
        self.assertIn(b'<form action="/index" method="POST">', response.data)

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
        self.assertIn(b'<form action="/index" method="POST">', response.data)

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

    def test_output(self):
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

    def test_login(self):
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
        self.assertIn(b'<form action="/login" method="POST">', response.data)
        self.assertIn(b'<input type="text" id="username" name="username" required>', response.data)
        self.assertIn(b'<input type="password" id="password" name="password" required>', response.data)

        # check for create new account
        self.assertIn(b'<a href="/register" class="button">Create Account</a>', response.data)

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

    def test_register(self):
        # Send a GET request to the new account page
        response = self.client.get('/register')

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
        self.assertIn(b'<form action="/register" method="POST">', response.data)
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

    def test_indexPost(self):
        # Data that simulates what would be entered in the form
        form_data = {
            'artifact_type': '1',  # DEBUG ARTIFACT
            'model_selection': '2',  # Llama-3.2-3B-Instruct
            'artifact_parameters': 'Some additional parameters for artifact'
        }

        # Simulate the POST request to the '/index' route with the form data
        response = self.client.post('/index', data=form_data)

        # Assert that the submission works
        self.assertEqual(response.status_code, 200)

        # Check that it redirects to the output page
        self.assertIn(b'<title>AI Wargaming</title>', response.data)

        # Check that the output exists
        self.assertIn(b'<div id="ai-output">You selected: 1</div>', response.data)
        self.assertIn(b'<div id="ai-output">You gave the following prompt: Some additional parameters for artifact</div>', response.data)
        self.assertIn(b'Output: You selected the DEBUG ARTIFACT and gave this prompt: Some additional parameters for artifact Here is a bunch of random numbers:', response.data)
        
        # Data that simulates what would be entered in the form
        form_data = {
            'artifact_type': '1',  # DEBUG ARTIFACT
            'artifact_parameters': 'Some additional parameters for artifact'
        }

        # Simulate the POST request to the '/index' route with the form data
        response = self.client.post('/index', data=form_data)

        # Assert that the submission works
        self.assertEqual(response.status_code, 200)

        # Check that it redirects to the output page
        self.assertIn(b'<title>Capstone Starter</title>', response.data)

        # Check that it gives the error message
        self.assertIn(b'<p>ERROR: Please select an artifact, model type, and give a prompt.</p>', response.data)

        # Data that simulates what would be entered in the form
        form_data = {
            'artifact_parameters': 'Some additional parameters for artifact'
        }

        # Simulate the POST request to the '/index' route with the form data
        response = self.client.post('/index', data=form_data)

        # Assert that the submission works
        self.assertEqual(response.status_code, 200)

        # Check that it redirects to the output page
        self.assertIn(b'<title>Capstone Starter</title>', response.data)

        # Check that it gives the error message
        self.assertIn(b'<p>ERROR: Please select an artifact, model type, and give a prompt.</p>', response.data)

        # Data that simulates what would be entered in the form
        form_data = {
            'artifact_type': '1',  # DEBUG ARTIFACT
        }

        # Simulate the POST request to the '/index' route with the form data
        response = self.client.post('/index', data=form_data)

        # Assert that the submission works
        self.assertEqual(response.status_code, 200)

        # Check that it redirects to the output page
        self.assertIn(b'<title>Capstone Starter</title>', response.data)

        # Check that it gives the error message
        self.assertIn(b'<p>ERROR: Please select an artifact, model type, and give a prompt.</p>', response.data)

        # Data that simulates what would be entered in the form
        form_data = {
        }

        # Simulate the POST request to the '/index' route with the form data
        response = self.client.post('/index', data=form_data)

        # Assert that the submission works
        self.assertEqual(response.status_code, 200)

        # Check that it redirects to the output page
        self.assertIn(b'<title>Capstone Starter</title>', response.data)

        # Check that it gives the error message
        self.assertIn(b'<p>ERROR: Please select an artifact, model type, and give a prompt.</p>', response.data)

if __name__ == '__main__':
    unittest.main()