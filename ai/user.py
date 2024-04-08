"""User management module and list of users."""

import bcrypt
from ai.conversation import Base

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    user_name = Column(String(50), nullable=False)
    phone = Column(String(50), nullable=True)
    email = Column(String(50), nullable=True)
    salt = Column(String(50), nullable=True)
    password_cleartext = Column(String(50), nullable=True)
    password_hash = Column(String(50), nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    notes = Column(Text, nullable=True)
    # conversations = relationship("Conversation", back_populates="user")

    @property
    def info_dict(self):
        return {
            'id': self.id,
            'user_name': self.user_name,
            'phone': self.phone,
            'email': self.email,
            'created_at': self.created_at,
            'notes': self.notes
        }

    



class UserManagement():
    def __init__(self):
        self.session = Session()

    def create_user(self, user_name, phone=None, email=None, password_cleartext=None, notes=None):
        """Create a new user in the database."""
        # Generate salt and hash password
        salt = bcrypt.gensalt()
        password_hash = bcrypt.hashpw(password_cleartext.encode('utf-8'), salt)

        new_user = User(user_name=user_name, phone=phone, email=email, salt=salt, password_cleartext=password_cleartext, password_hash=password_hash, notes=notes)
        self.session.add(new_user)
        self.session.commit()
        return new_user

    def create_user_from_dict(self, user_dict):
        """Create a new user in the database from a dictionary."""
        return self.create_user(user_dict['user_name'], user_dict['phone'], user_dict['email'], user_dict['password_cleartext'], user_dict['notes'])

    def update_user(self, user_id, user_name=None, phone=None, email=None, password_cleartext=None, notes=None):
        """Update an existing user."""
        user = self.session.query(User).filter(User.id == user_id).first()
        if user:
            if user_name:
                user.user_name = user_name
            if phone:
                user.phone = phone
            if email:
                user.email = email
            if password_cleartext:
                # Generate new salt and hash password
                salt = bcrypt.gensalt()
                password_hash = bcrypt.hashpw(password_cleartext.encode('utf-8'), salt)
                user.salt = salt
                user.password_cleartext = password_cleartext
                user.password_hash = password_hash
            if notes:
                user.notes = notes
            self.session.commit()
        return user

    def delete_user(self, user_id):
        """Delete a user from the database."""
        user = self.session.query(User).filter(User.id == user_id).first()
        if user:
            self.session.delete(user)
            self.session.commit()

    def close_session(self):
        """Close the database session."""
        self.session.close()



if __name__ == "__main__":
    
    # create a new user
    user = User(name = "issa", password = "issapassword", phone = "1234567890", email = "issa@yangai")


    um = UserManagement()
    um.create_user(user.info_dict)

    print(f"New user created: {user.info_dict}")

    