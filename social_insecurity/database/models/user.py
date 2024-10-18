from sqlalchemy import Boolean, Integer, String  # type: ignore
from sqlalchemy.orm import Mapped, mapped_column  # type: ignore

from social_insecurity.database.base import db


class User(db.Model):

    __tablename__ = "user"

    id: Mapped[str] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    active: Mapped[Boolean] = mapped_column(default=True)
    authenticated: Mapped[Boolean] = mapped_column(default=False)

    def is_active(self):
        """True, as all users are active."""
        return self.active

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.id

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False
