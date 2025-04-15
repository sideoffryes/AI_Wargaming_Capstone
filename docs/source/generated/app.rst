Webserver API Documentation
===========================

Describes the API endpoints for the Flask web server

.. http:get:: /

   Handles GET requsts to the root path and serves the main HTML home page containing the document generation form.

   :undocumented:

.. http:get:: /index

   Handles GET requsts to the /index path and serves the main HTML home page containing the document generation form.

   :undocumented:

.. http:post:: /index

   **Description:** Handles the submission of the artifact generation form. Based on the form data, it either returns an error message or triggers the artifact generation process and redirects to the output page.

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
   