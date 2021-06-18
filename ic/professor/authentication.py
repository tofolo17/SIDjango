from django.contrib.auth.models import User


class IsActiveAuthBackend(object):
    """
    Faz a autenticação somente se o usuário for ativo, e usando o email
    """

    def authenticate(self, request, username=None, password=None):
        try:
            user = User.objects.get(email=username)
            if user.check_password(password) and user.is_active:  # A segunda condição é necessária?
                return user
            return None
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
