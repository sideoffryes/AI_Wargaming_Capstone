import unittest
from app import app

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
        self.assertIn(b'<option value="1">Llama-3.2-3B-Instruct</option>', response.data)
        self.assertIn(b'<option value="2">Llama-3.1-8B-Instruct</option>', response.data)
        self.assertIn(b'<option value="3">Llama-3.3-70B-Instruct</option>', response.data)
        
        # Instead of checking for the exact textarea, check for the presence of a form field
        self.assertIn(b'<textarea class ="my_text" id="artifact_parameters" name="artifact_parameters" wrap="hard"></textarea>', response.data)
        
        # Check for the dropdown menu items
        self.assertIn(b'Generate Document', response.data)
        self.assertIn(b'Login', response.data)
        self.assertIn(b'User Profile', response.data)
        self.assertIn(b'Documentation', response.data)

        # Check for the {{ errorMsg }} being empty because there should be no error in this case
        self.assertIn(b'<p></p>', response.data)
        
if __name__ == '__main__':
    unittest.main()
