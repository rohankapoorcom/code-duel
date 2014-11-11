from duel import login_manager
from duel.models import User

@login_manager.user_loader
def load_user(id):
    """Loads the logged in user from the DB"""
    return User.query.get(int(id))

@login_manager.token_loader
def load_user_by_token(token):
    """Loads the logged in user from the token"""
    return User.query.filter_by(authentication_token=token).first_or_404()
