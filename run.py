from app import create_app
from app.db.models import db




app = create_app()

with app.app_context():  # Ensure that the app context is active for database setup
    db.create_all()  # Make sure the database tables are created
   

if __name__ == "__main__":
    app.run(debug=True)
