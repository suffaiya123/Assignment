from .models import Users
from .data import check_password_alt


class UsersBackend(object):

    def authenticate(self, username=None, password=None):
        try:
            password_enc, user = check_password_alt(username, password)
        except Exception as e:
            return None
        if user.password == password_enc:
            return user
        else:
            return None

    @staticmethod
    def get_user(user_id):
        try:
            ret = Users.objects.get(pk=user_id)
            return ret
        except IndexError:
            return None
        except:
           pass
