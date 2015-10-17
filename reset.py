import os
import db

def clear_postgres(engine):
	engine.execute("TRUNCATE \"oldgoldmtn\";")

def clear_tmp_folder():
	for file in os.listdir("./tmp/img"):
		file_path = os.path.join("./tmp/img", file)
		os.unlink(file_path)

#clears the heroku postgres database and the tmp img folder
database = db.heroku()
clear_postgres(database.engine)
clear_tmp_folder()