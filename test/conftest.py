import pytest
from models.users.user import User
 
 
@pytest.fixture(scope='module')
def new_user():
    user = User('patkennedy79@gmail.com', 'FlaskIsAwesome')
    return user