# suggest-me
# A flask web app to suggest movies, books and much more.
# Live version deployed at https://suggest-me.herokuapp.com/

to run the app follow these commands after cloning the project

pip install requirements.txt
activate the environment

      cd venv/scripts
      ./activate


move into the project folder

      (venv)suggest-me> 

(enter python interpreter)

      (venv)suggest-me> python
      
If you are using postgres or other database make corresponding changes in app.py. Then run these commands for database migrations. 

      from app import db
      db.create_all()
      exit()
      
(exit interpreter)

      (venv)suggest-me> python app.py

visit the localhost server http://127.0.0.1:5000/


