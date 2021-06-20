from .models import Conta


class IsAuthorizedAuthBackend(object):
    """
    Anotações:
        Mensagem de erro diferenciada para account.authorized == False
    """

    def authenticate(self, request, username=None, password=None):
        try:
            account = Conta.objects.get(email=username)
            if account.check_password(password) and account.authorized:
                return account
            return None
        except Conta.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return Conta.objects.get(pk=user_id)
        except Conta.DoesNotExist:
            return None
