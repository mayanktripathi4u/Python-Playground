# What is a `.http `file?
A `.http` file is typically used by certain IDEs (like JetBrains' PyCharm or Visual Studio Code with the REST Client extension) to define and execute HTTP requests directly from the editor. This file format allows you to write, test, and execute HTTP requests without needing to use tools like Postman or cURL separately.

## Possible Usage of `.http`
* Testing HTTP Requests: You can define GET, POST, PUT, DELETE, etc., requests within this file, which can be run to interact with your Flask app or any other HTTP-based service.
* Local Development: You might use this file to test endpoints of your Flask application during development.

## Example Setup and Usage
If you want to use a .http file to run and test requests against your Flask app, here's an example:

1. Create __dev__.http: Create a file named __dev__.http in your project directory.

2. Write HTTP Requests: Inside this file, you can write HTTP requests as follows: [code](/Python-Playground/Projects/Flask/WebApp/MoneyControlApp/__dev__.http)
3. Run the Flask App: Start your Flask app in terminal.
   ```bash
   python3 app.py
   ```
4. Execute HTTP Requests:
   * If you're using PyCharm: You can right-click inside the `.http` file and choose `Run` to execute the request.
   * If you're using VS-Code: Install the **REST Client Extension**, then click on "Send Request" above each request in the `.http` file.
  
# Benefits of Using .http Files
* Integrated Testing: You can keep your API tests close to your code, making it easier to update them as you develop.
* Version Control: Unlike Postman collections, you can version-control these files with your codebase.

If you are not using an IDE that supports `.http` files, this approach might not be relevant for your workflow. In that case, you can continue using traditional methods like Postman or cURL for testing your Flask endpoints.

# Video Reference
[The Best way to test your REST API Code](https://www.youtube.com/watch?v=qJlTGaTIkHA)