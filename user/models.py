import datetime

from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from common.models import BaseModel
from user.utils import generate_unique_string


# Create your models here.
class Player(BaseModel):
    class AgeRangeChoices(models.TextChoices):
        ABOVE_AGE = 'above_age', _("Above age")
        UNDER_AGE = 'under_age', _("Under age")
        NOT_ASSIGNED = 'na', _("Not assigned")

    profile_name = models.CharField(verbose_name="Profile name", null=True, blank=True, max_length=90)
    teki_id = models.CharField(verbose_name=_("Teki id"), max_length=10, blank=True)
    user = models.OneToOneField(to=User, related_name='player', on_delete=models.CASCADE, verbose_name=_("User"))
    birth_date = models.DateField(verbose_name=_("Birth date"), null=True, blank=True)

    def __str__(self):
        return self.teki_id

    def save(
            self,
            *args,
            force_insert=False,
            force_update=False,
            using=None,
            update_fields=None,
    ):
        if not self.teki_id:
            self.teki_id = generate_unique_string(prefix='teki', length=10, all_digit=False)

        super(Player, self).save(*args, force_insert, force_update, using, update_fields)

    @property
    def age_range(self) -> str:
        if not self.age_range:
            return Player.AgeRangeChoices.NOT_ASSIGNED

        age = (timezone.now() - self.birth_date).days // 365

        return Player.AgeRangeChoices.ABOVE_AGE if age >= 18 else Player.AgeRangeChoices.UNDER_AGE

