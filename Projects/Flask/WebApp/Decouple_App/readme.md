1. Create a Backend Dir. for managing all backend related code such as Python; Flask; Database; Business Logic; Data Validation; etc.
   Some key notes:
   * Ensure your Flask backend allows Cross-Origin Resource Sharing (CORS) by adding the necessary headers. You can use the flask-cors extension for this purpose.

    Install flask-cors:
    `pip install flask-cors`

2. Create a Frontend Dir. for managing all frontend related code such as HTML; JavaScript; AJAX etc.
    Some key notes:
    * Modify your JavaScript code to remove no-cors mode and handle the response properly: