from app import login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin):
    """Class used to manage user authentication and sessions."""

    def set_password(self, password):
        """Method used to encrypt user's password."""

        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Method used to verify user's password."""

        return check_password_hash(self.password_hash, password)

    @login.user_loader
    def load_user(id):
        return User.query.get(int(id))