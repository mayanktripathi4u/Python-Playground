Install
```bash
pip install flask-sqlalchemy flask-migrate
```

Here we are creating 
* `app.py` --> for all
* `run.py` --> Instead of running `app.py` file we will run `run.py` file.
* `models.py` --> All databases related classes / tables will be define here.
* `routes.py` --> 
* 



Check if Post is in Use
`lsof -i:5000 `
Kill the process
`kill $(lsof -t -i:5000)`


When we first run it `python run.py`, it will fail as the Table does not exists.
So first we have to migrate the DB.

Navigate to Terminal, check if the files exists.
Run the command `flask db init`.

followed by `flask db migrate`
and `flask db upgrade`

Note: We do `flask db init` only once, howvere `migrate` and `upgrade` has to be done everytime we make change in the table or create new table(s).

After this we can run the flask app again and could see the error is gone and should able to see the empty array as the table is empty.





