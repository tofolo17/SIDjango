from .models import Conta


class IsAuthorizedAuthBackend(object):
    def authenticate(self, request, username=None, password=None):
        try:
            account = Conta.objects.get(email=username)
            if account.check_password(password):
                return account
            return None
        except Conta.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return Conta.objects.get(pk=user_id)
        except Conta.DoesNotExist:
            return None
