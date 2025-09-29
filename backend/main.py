from app import create_app
from flask_migrate import upgrade

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        # Create tables if they don't exist
        from app import db

        db.create_all()

    app.run(debug=True, host='0.0.0.0', port=5000)