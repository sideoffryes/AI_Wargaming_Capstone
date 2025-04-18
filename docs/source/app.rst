Web Server API Documentation
============================

Describes the API endpoints for the Flask web server

User Endpoints
--------------

/userprofile
^^^^^^^^^^^^

.. http:get:: /userprofile

   Displays the user profile page.

   This endpoint renders the user profile page, allowing logged-in users to view their username and change their password. If the user is not logged in (no `user_id` in the session), it displays a default view indicating they are not logged in. See :func:`~app.userprofile`.

   **Session Requirements:**

   * Requires the `user_id` to be present in the session to identify the logged-in user.

   **Response Body:**

   * **Content-Type:** ``text/html``
   * Renders the `userprofile.html` template. The template will receive the following context variables:
      * ``username``: The username of the logged-in user, or "Not logged in" if no user is logged in.
      * ``errorMsg``: An empty string by default for GET requests. May contain an error message after a failed POST request.
      * ``successMsg``: An empty string by default for GET requests. May contain a success message after a successful POST request.

   **Example Response (User logged in):**

   .. code-block:: html

      <!DOCTYPE html>
      <html>
      <head>
          <title>User Profile</title>
      </head>
      <body>
          <h1>User Profile</h1>
          <p>Username: testuser</p>
          <form method="POST" action="/userprofile">
              <label for="curpwd">Current Password:</label><br>
              <input type="password" id="curpwd" name="curpwd"><br>
              <label for="newpwd">New Password:</label><br>
              <input type="password" id="newpwd" name="newpwd"><br>
              <label for="conpwd">Confirm New Password:</label><br>
              <input type="password" id="conpwd" name="conpwd"><br><br>
              <input type="submit" value="Change Password">
          </form>
          </body>
      </html>

   **Example Response (User not logged in):**

   .. code-block:: html

      <!DOCTYPE html>
      <html>
      <head>
          <title>User Profile</title>
      </head>
      <body>
          <h1>User Profile</h1>
          <p>Username: Not logged in</p>
          <p></p>
          <p></p>
          <form method="POST" action="/userprofile">
              <label for="curpwd">Current Password:</label><br>
              <input type="password" id="curpwd" name="curpwd"><br>
              <label for="newpwd">New Password:</label><br>
              <input type="password" id="newpwd" name="newpwd"><br>
              <label for="conpwd">Confirm New Password:</label><br>
              <input type="password" id="conpwd" name="conpwd"><br><br>
              <input type="submit" value="Change Password">
          </form>
          </body>
      </html>

.. http:post:: /userprofile

   Handles user password change requests.

   This endpoint processes the form submission from the user profile page to change the user's password. It requires the user to be logged in (a valid `user_id` in the session) and validates the provided current password against the stored hash before updating the password.

   **Session Requirements:**

   * Requires the `user_id` to be present in the session to identify the logged-in user.

   **Request Body:**

   * **Content-Type:** ``application/x-www-form-urlencoded``
   * The request body should contain the following form parameters:
      * ``curpwd``: The user's current password.
      * ``newpwd``: The desired new password.
      * ``conpwd``: Confirmation of the new password.

   **Response Codes:**

   * **200 OK (on successful password change):**
      * **Response Body:**
         * **Content-Type:** ``text/html``
         * Renders the `userprofile.html` template with the logged-in ``username`` and a ``successMsg`` indicating that the password was successfully changed. The ``errorMsg`` will be an empty string.
   * **200 OK (on errors):**
      * **Response Body:**
         * **Content-Type:** ``text/html``
         * Renders the `userprofile.html` template with the logged-in ``username`` and an ``errorMsg`` explaining the issue. The ``successMsg`` will be an empty string. Possible error messages include:
            * "ERROR: Please fill out all fields." (if any of the password fields are missing)
            * "ERROR: Current password is incorrect." (if the provided current password does not match)
            * "ERROR: New passwords do not match." (if the new password and confirmation do not match)

   **Example Request (using curl):**

   .. code-block:: bash

      curl -X POST -d "curpwd=oldpassword&newpwd=newsecurepassword&conpwd=newsecurepassword" http://yourdomain.com/userprofile -c cookies.txt -b cookies.txt

      # Note: You might need to handle session cookies appropriately for a real-world scenario.

   **Example Successful Response:**

   .. code-block:: html

      <!DOCTYPE html>
      <html>
      <head>
          <title>User Profile</title>
      </head>
      <body>
          <h1>User Profile</h1>
          <p>Username: testuser</p>
          <p style="color: green;">Password successfully changed.</p>
          <form method="POST" action="/userprofile">
              <label for="curpwd">Current Password:</label><br>
              <input type="password" id="curpwd" name="curpwd"><br>
              <label for="newpwd">New Password:</label><br>
              <input type="password" id="newpwd" name="newpwd"><br>
              <label for="conpwd">Confirm New Password:</label><br>
              <input type="password" id="conpwd" name="conpwd"><br><br>
              <input type="submit" value="Change Password">
          </form>
          </body>
      </html>

   **Example Error Response (Incorrect current password):**

   .. code-block:: html

      <!DOCTYPE html>
      <html>
      <head>
          <title>User Profile</title>
      </head>
      <body>
          <h1>User Profile</h1>
          <p>Username: testuser</p>
          <p style="color: red;">ERROR: Current password is incorrect.</p>
          <form method="POST" action="/userprofile">
              <label for="curpwd">Current Password:</label><br>
              <input type="password" id="curpwd" name="curpwd"><br>
              <label for="newpwd">New Password:</label><br>
              <input type="password" id="newpwd" name="newpwd"><br>
              <label for="conpwd">Confirm New Password:</label><br>
              <input type="password" id="conpwd" name="conpwd"><br><br>
              <input type="submit" value="Change Password">
          </form>
          </body>
      </html>.. http:post:: /userprofile

   Handles user password change requests.

   This endpoint processes the form submission from the user profile page to change the user's password. It requires the user to be logged in (a valid `user_id` in the session) and validates the provided current password against the stored hash before updating the password.

   **Session Requirements:**

   * Requires the `user_id` to be present in the session to identify the logged-in user.

   **Request Body:**

   * **Content-Type:** ``application/x-www-form-urlencoded``
   * The request body should contain the following form parameters:
      * ``curpwd``: The user's current password.
      * ``newpwd``: The desired new password.
      * ``conpwd``: Confirmation of the new password.

   **Response Codes:**

   * **200 OK (on successful password change):**
      * **Response Body:**
         * **Content-Type:** ``text/html``
         * Renders the `userprofile.html` template with the logged-in ``username`` and a ``successMsg`` indicating that the password was successfully changed. The ``errorMsg`` will be an empty string.
   * **200 OK (on errors):**
      * **Response Body:**
         * **Content-Type:** ``text/html``
         * Renders the `userprofile.html` template with the logged-in ``username`` and an ``errorMsg`` explaining the issue. The ``successMsg`` will be an empty string. Possible error messages include:
            * "ERROR: Please fill out all fields." (if any of the password fields are missing)
            * "ERROR: Current password is incorrect." (if the provided current password does not match)
            * "ERROR: New passwords do not match." (if the new password and confirmation do not match)

   **Example Request (using curl):**

   .. code-block:: bash

      curl -X POST -d "curpwd=oldpassword&newpwd=newsecurepassword&conpwd=newsecurepassword" http://yourdomain.com/userprofile -c cookies.txt -b cookies.txt

      # Note: You might need to handle session cookies appropriately for a real-world scenario.

   **Example Successful Response:**

   .. code-block:: html

      <!DOCTYPE html>
      <html>
      <head>
          <title>User Profile</title>
      </head>
      <body>
          <h1>User Profile</h1>
          <p>Username: testuser</p>
          <p style="color: green;">Password successfully changed.</p>
          <form method="POST" action="/userprofile">
              <label for="curpwd">Current Password:</label><br>
              <input type="password" id="curpwd" name="curpwd"><br>
              <label for="newpwd">New Password:</label><br>
              <input type="password" id="newpwd" name="newpwd"><br>
              <label for="conpwd">Confirm New Password:</label><br>
              <input type="password" id="conpwd" name="conpwd"><br><br>
              <input type="submit" value="Change Password">
          </form>
          </body>
      </html>

   **Example Error Response (Incorrect current password):**

   .. code-block:: html

      <!DOCTYPE html>
      <html>
      <head>
          <title>User Profile</title>
      </head>
      <body>
          <h1>User Profile</h1>
          <p>Username: testuser</p>
          <p style="color: red;">ERROR: Current password is incorrect.</p>
          <form method="POST" action="/userprofile">
              <label for="curpwd">Current Password:</label><br>
              <input type="password" id="curpwd" name="curpwd"><br>
              <label for="newpwd">New Password:</label><br>
              <input type="password" id="newpwd" name="newpwd"><br>
              <label for="conpwd">Confirm New Password:</label><br>
              <input type="password" id="conpwd" name="conpwd"><br><br>
              <input type="submit" value="Change Password">
          </form>
          </body>
      </html>

Authentication Endpoints
------------------------

/login
^^^^^^

.. http:get:: /login

   Displays the login form.

   This endpoint is responsible for rendering the HTML form that allows users to log in to the web application. No data is submitted or processed when this endpoint is accessed via a GET request. See :func:`~app.login`.

   **Response Body:**

   * **Content-Type:** ``text/html``
   * The response body will contain the HTML content of the `login.html` template, which includes the login form with fields for username and password.

   **Example Response:**

   .. code-block:: html

      <!DOCTYPE html>
      <html>
      <head>
          <title>Login</title>
      </head>
      <body>
          <h1>Login</h1>
          <form method="POST" action="/login">
              <label for="username">Username:</label><br>
              <input type="text" id="username" name="username"><br>
              <label for="password">Password:</label><br>
              <input type="password" id="password" name="password"><br><br>
              <input type="submit" value="Login">
          </form>
          </body>
      </html>

.. http:post:: /login

   Handles user login submissions.

   This endpoint processes the login form submitted by users. It expects a POST request with username and password data. It authenticates the user against stored credentials and either logs them in or displays an error message. See :func:`~app.login`.

   **Request Body:**

   * **Content-Type:** ``application/x-www-form-urlencoded``
   * The request body should contain the following form parameters:
      * ``username``: The username provided by the user.
      * ``password``: The password provided by the user.

   **Response Codes:**

   * **200 OK (on successful login):**
      * **Response Body:**
         * **Content-Type:** ``text/html``
         * Renders the `index.html` template with a success message indicating the logged-in username.
   * **200 OK (on failed login or non-existent user):**
      * **Response Body:**
         * **Content-Type:** ``text/html``
         * Renders the `login.html` template with an `errorMsg` parameter containing an error message (e.g., "ERROR: That username does not exist, please try again." or "ERROR: Given login credentials were incorrect, please try again.").

   **Example Request (using curl):**

   .. code-block:: bash

      curl -X POST -d "username=testuser&password=securepassword" http://yourdomain.com/login

   **Example Successful Response (renders index.html):**

   .. code-block:: html

      <!DOCTYPE html>
      <html>
      <head>
          <title>Home</title>
      </head>
      <body>
          <p>Successfully logged into: testuser</p>
          </body>
      </html>

   **Example Error Response (renders login.html with error):**

   .. code-block:: html

      <!DOCTYPE html>
      <html>
      <head>
          <title>Login</title>
      </head>
      <body>
          <h1>Login</h1>
          <p style="color: red;">ERROR: Given login credentials were incorrect, please try again.</p>
          <form method="POST" action="/login">
              <label for="username">Username:</label><br>
              <input type="text" id="username" name="username"><br>
              <label for="password">Password:</label><br>
              <input type="password" id="password" name="password"><br><br>
              <input type="submit" value="Login">
          </form>
          </body>
      </html>

/register
^^^^^^^^^

.. http:get:: /register

   Displays the user registration form.

   This endpoint renders the HTML form that allows new users to create an account on the web application. No data is submitted or processed when this endpoint is accessed via a GET request. See :func:`~app.register`.

   **Response Body:**

   * **Content-Type:** ``text/html``
   * The response body will contain the HTML content of the `new_account.html` template, which includes the registration form with fields for username, password, and password confirmation.

   **Example Response:**

   .. code-block:: html

      <!DOCTYPE html>
      <html>
      <head>
          <title>Register</title>
      </head>
      <body>
          <h1>Create New Account</h1>
          <form method="POST" action="/register">
              <label for="username">Username:</label><br>
              <input type="text" id="username" name="username"><br>
              <label for="ogpassword">Password:</label><br>
              <input type="password" id="ogpassword" name="ogpassword"><br>
              <label for="repassword">Confirm Password:</label><br>
              <input type="password" id="repassword" name="repassword"><br><br>
              <input type="submit" value="Register">
          </form>
          </body>
      </html>

.. http:post:: /register

   Handles user registration submissions.

   This endpoint processes the registration form submitted by new users. It expects a POST request with username, password, and password confirmation data. It validates the input, checks for existing usernames, hashes the password, and creates a new user account in the database.

   **Request Body:**

   * **Content-Type:** ``application/x-www-form-urlencoded``
   * The request body should contain the following form parameters:
      * ``username``: The desired username for the new account.
      * ``ogpassword``: The desired password for the new account.
      * ``repassword``: Confirmation of the desired password.

   **Response Codes:**

   * **200 OK (on successful registration):**
      * **Response Body:**
         * **Content-Type:** ``text/html``
         * Renders the `login.html` template with a success message (`errorMsg`) instructing the user to log in.
   * **200 OK (on errors):**
      * **Response Body:**
         * **Content-Type:** ``text/html``
         * Renders the `new_account.html` template with an `errorMsg` explaining the issue. Possible error messages include:
            * "ERROR: This username already exists. Please use a different one."
            * "ERROR: The passwords did not match."

   **Example Request (using curl):**

   .. code-block:: bash

      curl -X POST -d "username=newuser&ogpassword=secure123&repassword=secure123" http://yourdomain.com/register

   **Example Successful Response (renders login.html):**

   .. code-block:: html

      <!DOCTYPE html>
      <html>
      <head>
          <title>Login</title>
      </head>
      <body>
          <h1>Login</h1>
          <p style="color: green;">NOTICE: Please login using previously created username and password.</p>
          <form method="POST" action="/login">
              <label for="username">Username:</label><br>
              <input type="text" id="username" name="username"><br>
              <label for="password">Password:</label><br>
              <input type="password" id="password" name="password"><br><br>
              <input type="submit" value="Login">
          </form>
          </body>
      </html>

   **Example Error Response (Username already exists):**

   .. code-block:: html

      <!DOCTYPE html>
      <html>
      <head>
          <title>Register</title>
      </head>
      <body>
          <h1>Create New Account</h1>
          <p style="color: red;">ERROR: This username already exists. Please use a different one.</p>
          <form method="POST" action="/register">
              <label for="username">Username:</label><br>
              <input type="text" id="username" name="username"><br>
              <label for="ogpassword">Password:</label><br>
              <input type="password" id="ogpassword" name="ogpassword"><br>
              <label for="repassword">Confirm Password:</label><br>
              <input type="password" id="repassword" name="repassword"><br><br>
              <input type="submit" value="Register">
          </form>
          </body>
      </html>

   **Example Error Response (Passwords do not match):**

   .. code-block:: html

      <!DOCTYPE html>
      <html>
      <head>
          <title>Register</title>
      </head>
      <body>
          <h1>Create New Account</h1>
          <p style="color: red;">ERROR: The passwords did not match.</p>
          <form method="POST" action="/register">
              <label for="username">Username:</label><br>
              <input type="text" id="username" name="username"><br>
              <label for="ogpassword">Password:</label><br>
              <input type="password" id="ogpassword" name="ogpassword"><br>
              <label for="repassword">Confirm Password:</label><br>
              <input type="password" id="repassword" name="repassword"><br><br>
              <input type="submit" value="Register">
          </form>
          </body>
      </html>

/logout
^^^^^^^

.. http:get:: /logout

   Logs the user out.

   This endpoint handles user logout functionality. When accessed via a GET request, it removes the `user_id` from the session, effectively logging the user out of their profile. It then redirects the user to the main index page with a success message. See :func:`~app.logout`.

   **Session Modification:**

   * Clears the `user_id` key from the user's session.

   **Response Body:**

   * **Content-Type:** ``text/html``
   * Renders the `index.html` template with an `errorMsg` parameter indicating successful logout.

   **Example Response:**

   .. code-block:: html

      <!DOCTYPE html>
      <html>
      <head>
          <title>Home</title>
      </head>
      <body>
          <p>Successfully logged out of profile</p>
          </body>
      </html>

Artifact Endpoints
------------------

/
^

.. http:get:: /

   Handles GET requsts to the root path and serves the main HTML home page containing the document generation form. See :func:`~app.index`.

/index
^^^^^^

.. http:get:: /index

   Handles GET requsts to the /index path and serves the main HTML home page containing the document generation form. See :func:`~app.index`.

.. http:post:: /index

   **Description:** Handles the submission of the artifact generation form. Based on the form data, it either returns an error message or triggers the artifact generation process and redirects to the output page. See :func:`~app.index`.

   **Request Body (Form Data):**

   The request body is sent as `application/x-www-form-urlencoded` and contains the following fields:

   * `artifact_type` (integer, required): An integer representing the type of artifact to generate.
   * `model_selection` (integer, required): An integer representing the chosen language model.
   * `artifact_parameters` (string, required if `artifact_type` is not 4): Free-form text providing parameters for the artifact generation.
   * `opord_orientation` (string, required if `artifact_type` is 4): Orientation field for OPORD generation.
   * `opord_situation` (string, required if `artifact_type` is 4): Situation field for OPORD generation.
   * `opord_mission` (string, required if `artifact_type` is 4): Mission field for OPORD generation.
   * `opord_execution` (string, required if `artifact_type` is 4): Execution field for OPORD generation.
   * `opord_admin` (string, required if `artifact_type` is 4): Administration field for OPORD generation.
   * `opord_logistics` (string, required if `artifact_type` is 4): Logistics field for OPORD generation.
   * `opord_command` (string, required if `artifact_type` is 4): Command and Signal field for OPORD generation.

   **Request Body Example (Generic Artifact):**

   .. code-block:: http

      POST /index HTTP/1.1
      Content-Type: application/x-www-form-urlencoded

      artifact_type=2&model_selection=1&artifact_parameters=Provide%20a%20brief%20summary%20of%20the%20topic.

   **Request Body Example (OPORD Artifact):**

   .. code-block:: http

      POST /index HTTP/1.1
      Content-Type: application/x-www-form-urlencoded

      artifact_type=4&model_selection=2&opord_orientation=Terrain%20and%20Weather...&opord_situation=Enemy%20forces...&opord_mission=Conduct%20an%20attack...&opord_execution=Phase%201...&opord_admin=Supply%20point...&opord_logistics=Transportation...&opord_command=Commander's%20intent...

   **Response (Redirect - 302 Found):**

   On successful form submission and artifact generation, the server typically redirects the user to the `/output` route (not documented here) to display the generated artifact.

   :statuscode 302: Found
      :description: Redirects to the `/output` page upon successful artifact generation.

   **Response (Error - 200 OK with HTML):**

   If the `artifact_type` or `model_selection` are missing in the form data, the server returns the `index.html` template with an error message.

   :statuscode 200: OK
      :contenttype text/html:
      :example:

        .. code-block:: html

           <!DOCTYPE html>
           <html>
           <head>
               <title>Artifact Generator</title>
           </head>
           <body>
               <h1>Generate Artifact</h1>
               <p style="color: red;">ERROR: Please select an artifact, model type, and give a prompt.</p>
               </body>
           </html>

/output
^^^^^^^

.. http:get:: /output

   Renders the output.html template.

   This endpoint is responsible for displaying the main output of the web application. It fetches no external data but directly renders the content defined in the `output.html` template. See :func:`~app.home`.

   **Response Body:**

   * **Content-Type:** ``text/html``
   * The response body will contain the HTML content of the `output.html` template. This template likely includes the structure, styling, and dynamic content to be displayed to the user.

   **Example Response:**

   .. code-block:: html

      <!DOCTYPE html>
      <html>
      <head>
          <title>Output</title>
      </head>
      <body>
          <h1>Here is the output!</h1>
          </body>
      </html>


/my_artifacts
^^^^^^^^^^^^^

.. http:get:: /my_artifacts

   Displays the logged-in user's generated artifacts.

   This endpoint retrieves and displays a list of artifacts that have been generated by the currently logged-in user. It requires the user to be authenticated (i.e., having a `user_id` in the session). See :func:`~app.my_artifacts`.

   **Session Requirements:**

   * Requires the `user_id` to be present in the session to identify the logged-in user.

   **Response Codes:**

   * **200 OK (User has artifacts):**
      * **Response Body:**
         * **Content-Type:** ``text/html``
         * Renders the `my_artifacts.html` template, passing a list of the user's generated artifacts as the ``artifacts`` context variable. The structure and content of these artifacts will depend on your application's data model.
   * **200 OK (User has no artifacts):**
      * **Response Body:**
         * **Content-Type:** ``text/html``
         * Renders the `index.html` template with an `errorMsg` indicating that there are no artifacts associated with the user's account.
   * **200 OK (User not logged in):**
      * **Response Body:**
         * **Content-Type:** ``text/html``
         * Renders the `login.html` template with an `errorMsg` prompting the user to log in.

   **Example Response (User logged in with artifacts - simplified example):**

   .. code-block:: html

      <!DOCTYPE html>
      <html>
      <head>
          <title>My Artifacts</title>
      </head>
      <body>
          <h1>My Generated Artifacts</h1>
          <ul>
              <li>Artifact 1: ... (details of artifact 1) ...</li>
              <li>Artifact 2: ... (details of artifact 2) ...</li>
              </ul>
          </body>
      </html>

   **Example Response (User logged in, no artifacts):**

   .. code-block:: html

      <!DOCTYPE html>
      <html>
      <head>
          <title>Home</title>
      </head>
      <body>
          <p>NOTICE: There are no artifacts associated with this account.</p>
          </body>
      </html>

   **Example Response (User not logged in):**

   .. code-block:: html

      <!DOCTYPE html>
      <html>
      <head>
          <title>Login</title>
      </head>
      <body>
          <h1>Login</h1>
          <p style="color: green;">NOTICE: Please login to see your generated artifacts.</p>
          <form method="POST" action="/login">
              <label for="username">Username:</label><br>
              <input type="text" id="username" name="username"><br>
              <label for="password">Password:</label><br>
              <input type="password" id="password" name="password"><br><br>
              <input type="submit" value="Login">
          </form>
          </body>
      </html>

Documentation Endpoint
-----------------------

/docs/(path:filename)
^^^^^^^^^^^^^^^^^^^^^

.. http:get:: /docs/(path:filename)

   Serves static documentation files.

   This endpoint serves static files from the Sphinx-generated documentation build directory (`../docs/build/html`). The `filename` part of the URL path is dynamically used to locate and serve the requested file. See :func:`~app.docs`.

   **Path Parameters:**

   * **filename:** The path to the requested static file within the `../docs/build/html` directory. This can include subdirectories (e.g., `_static/style.css` or `index.html`).

   **Response Body:**

   * **Content-Type:** The Content-Type of the response will depend on the type of file being served (e.g., `text/html`, `text/css`, `image/png`, `application/javascript`).
   * The response body will contain the content of the requested static file.

   **Example Request:**

   * ``GET /docs/index.html``: Retrieves the main index page of the documentation.
   * ``GET /docs/_static/style.css``: Retrieves the stylesheet for the documentation.
   * ``GET /docs/api.html``: Retrieves the API documentation page.

   **Example Successful Response (for /docs/index.html):**

   .. code-block:: html

      <!DOCTYPE html>
      <html>
      <head>
          <title>Your Project Documentation</title>
          <link rel="stylesheet" href="_static/style.css" type="text/css" />
      </head>
      <body>
          <div class="document">
            <div class="documentwrapper">
              <div class="bodywrapper">
                <div class="body" role="main">
                  <h1>Welcome to Your Project's Documentation!</h1>
                  <div class="toctree-wrapper compound">
                    <ul>
                      <li class="toctree-l1"><a class="reference internal" href="api.html">API Reference</a></li>
                    </ul>
                  </div>
                </div>
              </div>
            </div>
            <div class="clearer"></div>
          </div>
      </body>
      </html>

   **Note:** The actual response body will vary greatly depending on the specific `filename` requested. This example shows a typical Sphinx-generated `index.html` file.
