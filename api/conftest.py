import pytest
from app import create_app, db
from models.UserModel import Users

@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app()
    
    # Configure as chaves secretas diretamente no app
    flask_app.config['SECRET_KEY'] = 'supersecretkey'
    flask_app.config['JWT_SECRET_KEY'] = 'supersecretkey'

    # Flask provides a way to test your application by exposing the Werkzeug test Client
    # and handling the context locals for you.
    testing_client = flask_app.test_client()


    # Establish an application context before running the tests.
    ctx = flask_app.app_context()
    ctx.push()


    yield testing_client  # this is where the testing happens!

    ctx.pop()

@pytest.fixture(scope='module')
def init_database():
    db.create_all()

    # Insert user data
    user = Users(email="test@example.com", name="Test", surname="User", cpf="123456789", roles=0)
    user.setPassword("password")
    user.save()

    yield db  # this is where the testing happens!

    db.session.remove()
    db.drop_all()
