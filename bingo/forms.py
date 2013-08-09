from django import forms
from django.utils.translation import pgettext, ugettext as _
from django.conf import settings
from django.contrib.auth.hashers import get_hasher

from models import BingoBoard, is_starttime


SALT = getattr(settings, "SALT", "hackme")
GAME_START_TIMES = getattr(settings, "GAME_START_TIMES", None)


class CreateForm(forms.Form):
    password = forms.CharField(label=_(u"Password (optional)"),
                               widget=forms.PasswordInput(),
                               required=False)

    def clean_password(self):
        hasher = get_hasher()
        hashed_password = hasher.encode(self.cleaned_data['password'],
                                        SALT)
        return hashed_password

    def clean(self):
        if not is_starttime():
            start, end = GAME_START_TIMES
            start_time_str = "{0}:{1}".format(
                str(start[0]).zfill(2),
                str(start[1]).zfill(2))
            end_time_str = "{0}:{1}".format(
                str(end[0]).zfill(2),
                str(end[1]).zfill(2))

            raise forms.ValidationError(
                _(u"Game can only be started between {0} and {1}.").format(
                    start_time_str, end_time_str))

        return super(CreateForm, self).clean()


class ReclaimForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput())

    def __init__(self, data=None, game=None):
        self.game = game
        super(ReclaimForm, self).__init__(data)

    def clean_password(self):
        hasher = get_hasher()
        hashed_password = hasher.encode(self.cleaned_data['password'],
                                        SALT)
        if not self.game or self.game.is_expired():
            raise forms.ValidationError(
                _("The game is expired, please create a new board."))
        bingo_boards = BingoBoard.objects.filter(game=self.game,
                                                 password=hashed_password)
        if bingo_boards.count() > 0:
            # if two users have the same password,
            # just return the first board.
            self.cleaned_data['bingo_board'] = bingo_boards[0]
        else:
            raise forms.ValidationError(
                _(u"No active board with this password."
                    " Try again, or create a new one."))
        return hashed_password