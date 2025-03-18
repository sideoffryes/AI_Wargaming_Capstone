import unittest
from app import app, db

class FlaskTestCase(unittest.TestCase):
    def setUp(self):
        """Set up a fresh database before each test."""
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'  # Use a separate test database
        self.client = app.test_client()
        
        with app.app_context():
            db.drop_all()  # Delete existing tables
            db.create_all()  # Recreate tables

    def tearDown(self):
        """Clean up the database after each test."""
        with app.app_context():
            db.session.remove()
            db.drop_all()  # Delete all tables after each test

    def test_index_route(self):
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

    def test_indexalt_route(self):
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

    def test_output_route(self):
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

    def test_login_route(self):
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

    def test_loginPost_DNEaccount(self):
        # Data that simulates what would be entered in the form
        form_data = {
            'username': 'DNE',
            'password': 'DNE',
        }

        # Simulate the POST request to the '/login' route with the form data
        response = self.client.post('/login', data=form_data)

        # Assert that the submission works
        self.assertEqual(response.status_code, 200)

        # Check that it stays on login page
        self.assertIn(b'<title>Login Form</title>', response.data)

        # Check that the error message exists
        self.assertIn(b'<p>ERROR: That username does not exist, please try again.</p>', response.data)

    def test_my_artifacts_logged_out(self):
        # Send a GET request to the artifacts page
        response = self.client.get('/my_artifacts')

        # Check that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Check that the title is is now Login From because user is not logged in
        self.assertIn(b'<title>Login Form</title>', response.data)

        # Check for the error message
        self.assertIn(b'NOTICE: Please login to see your generated artifacts.', response.data)

    def test_myartifacts_loggedin_noartifacts(self):
        # Data that simulates what would be entered in the form
        form_data = {
            'username': 'success',
            'ogpassword': 'success',
            'repassword': 'success'
        }

        # Simulate the POST request to the '/login' route with the form data
        response = self.client.post('/register', data=form_data)

        # Assert that the submission works
        self.assertEqual(response.status_code, 200)

        # Check that it stays on login page
        self.assertIn(b'<title>Login Form</title>', response.data)

        # Check that the error message exists
        self.assertIn(b'<p>NOTICE: Please login using previously created username and password.</p>', response.data)

        # Data that simulates what would be entered in the form
        form_data = {
            'username': 'success',
            'password': 'success',
        }

         # Simulate the POST request to the '/login' route with the form data
        response = self.client.post('/login', data=form_data)

        # Assert that the submission works
        self.assertEqual(response.status_code, 200)

        # Check that it stays on login page
        self.assertIn(b'<title>Capstone Starter</title>', response.data)

        # Check that the error message exists
        self.assertIn(b'<p>Successfully logged into: success</p>', response.data)

        # Send a GET request to the artifacts page
        response = self.client.get('/my_artifacts')

        # Check that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Check that the title is is now Login From because user is not logged in
        self.assertIn(b'<title>Capstone Starter</title>', response.data)

        # Check for the error message
        self.assertIn(b'NOTICE: There are no artifacts associated with this account.', response.data)

    def test_register_route(self):
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

    def test_registerPost_mismatchPassword(self):
        # Data that simulates what would be entered in the form
        form_data = {
            'username': 'DNE',
            'ogpassword': 'DNE',
            'repassword': 'notDNE'
        }

        # Simulate the POST request to the '/login' route with the form data
        response = self.client.post('/register', data=form_data)

        # Assert that the submission works
        self.assertEqual(response.status_code, 200)

        # Check that it stays on login page
        self.assertIn(b'<title>Account Creation</title>', response.data)

        # Check that the error message exists
        self.assertIn(b'<p>ERROR: The passwords did not match.</p>', response.data)

    def test_registerPost_successfulCreation(self):
        # Data that simulates what would be entered in the form
        form_data = {
            'username': 'success',
            'ogpassword': 'success',
            'repassword': 'success'
        }

        # Simulate the POST request to the '/login' route with the form data
        response = self.client.post('/register', data=form_data)

        # Assert that the submission works
        self.assertEqual(response.status_code, 200)

        # Check that it stays on login page
        self.assertIn(b'<title>Login Form</title>', response.data)

        # Check that the error message exists
        self.assertIn(b'<p>NOTICE: Please login using previously created username and password.</p>', response.data)

    def test_registerPost_duplicateCreation(self):
        # Data that simulates what would be entered in the form
        form_data = {
            'username': 'duplicate',
            'ogpassword': 'duplicate',
            'repassword': 'duplicate'
        }

        # Simulate the POST request to the '/login' route with the form data
        response = self.client.post('/register', data=form_data)

        # Assert that the submission works
        self.assertEqual(response.status_code, 200)

        # Check that it stays on login page
        self.assertIn(b'<title>Login Form</title>', response.data)

        # Check that the error message exists
        self.assertIn(b'<p>NOTICE: Please login using previously created username and password.</p>', response.data)

        # Simulate the POST request to the '/login' route with the form data
        response = self.client.post('/register', data=form_data)

        # Assert that the submission works
        self.assertEqual(response.status_code, 200)

        # Check that it stays on login page
        self.assertIn(b'<title>Account Creation</title>', response.data)

        # Check that the error message exists
        self.assertIn(b'<p>ERROR: This username already exists. Please use a different one.</p>', response.data)

    def test_registerloginPost_successfulCreationAndLogin(self):
        # Data that simulates what would be entered in the form
        form_data = {
            'username': 'success',
            'ogpassword': 'success',
            'repassword': 'success'
        }

        # Simulate the POST request to the '/login' route with the form data
        response = self.client.post('/register', data=form_data)

        # Assert that the submission works
        self.assertEqual(response.status_code, 200)

        # Check that it stays on login page
        self.assertIn(b'<title>Login Form</title>', response.data)

        # Check that the error message exists
        self.assertIn(b'<p>NOTICE: Please login using previously created username and password.</p>', response.data)

        # Data that simulates what would be entered in the form
        form_data = {
            'username': 'success',
            'password': 'success',
        }

         # Simulate the POST request to the '/login' route with the form data
        response = self.client.post('/login', data=form_data)

        # Assert that the submission works
        self.assertEqual(response.status_code, 200)

        # Check that it stays on login page
        self.assertIn(b'<title>Capstone Starter</title>', response.data)

        # Check that the error message exists
        self.assertIn(b'<p>Successfully logged into: success</p>', response.data)

    def test_registerloginPost_successfulCreation_badpassword(self):
        # Data that simulates what would be entered in the form
        form_data = {
            'username': 'success',
            'ogpassword': 'success',
            'repassword': 'success'
        }

        # Simulate the POST request to the '/login' route with the form data
        response = self.client.post('/register', data=form_data)

        # Assert that the submission works
        self.assertEqual(response.status_code, 200)

        # Check that it stays on login page
        self.assertIn(b'<title>Login Form</title>', response.data)

        # Check that the error message exists
        self.assertIn(b'<p>NOTICE: Please login using previously created username and password.</p>', response.data)

        # Data that simulates what would be entered in the form
        form_data = {
            'username': 'success',
            'password': 'wrong',
        }

         # Simulate the POST request to the '/login' route with the form data
        response = self.client.post('/login', data=form_data)

        # Assert that the submission works
        self.assertEqual(response.status_code, 200)

        # Check that it stays on login page
        self.assertIn(b'<title>Login Form</title>', response.data)

        # Check that the error message exists
        self.assertIn(b'<p>ERROR: Given login credentials were incorrect, please try again.</p>', response.data)     

    def test_logout_route(self):
        # Send a GET request to logout
        response = self.client.get('/logout')

        # Check that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Check that the title is present
        self.assertIn(b'<title>Capstone Starter</title>', response.data)

        # Check for the {{ errorMsg }}
        self.assertIn(b'Successfully logged out of profile', response.data)

    def test_indexPost_allparams(self):
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
        
    def test_indexPost_twoparams(self):
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

    def test_indexPost_onlyparam(self):
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

    def test_indexPost_onlytype(self):
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

    def test_indexPost_noparams(self):
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