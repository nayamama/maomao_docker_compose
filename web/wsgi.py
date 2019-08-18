from application import app as application

if __name__ == "__main__":
    # uwsgi expect a variable called "application" 
    application.run()
