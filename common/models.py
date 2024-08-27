import pickle

from django.conf import settings
from django.core.cache import cache
from django.db import models
from django.utils.translation import gettext_lazy as _


class BaseModel(models.Model):
    created_at = models.DateTimeField(verbose_name=_('Created at'), auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=_('Updated at'), auto_now=True)
    is_active = models.BooleanField(verbose_name=_('Active'), default=True)

    class Meta:
        abstract = True

    def __str__(self):
        raise NotImplementedError


class CachableModel(models.Model):

    def save(
            self,
            *args,
            force_insert=False,
            force_update=False,
            using=None,
            update_fields=None,
    ):
        cache.set(self.__class__.cache_key, pickle.dumps(self))
        super(CachableModel, self).save(*args, force_insert, force_update, using, update_fields)

    @staticmethod
    def cache_key() -> str:
        raise NotImplementedError

    @staticmethod
    def load():
        raise NotImplementedError

    class Meta:
        abstract = True


class SingletonBaseModel(BaseModel):
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.pk:
            if self.__class__.objects.filter(is_active=True).count() == 1:
                raise Exception(_(f'Only one active instance of {self.__class__.__name__} is allowed.'))
        super().save(*args, **kwargs)


class CommonConfigurationJsonConfig(BaseModel):
    name = models.CharField(verbose_name=_("Name"), unique=True, max_length=255)
    config = models.JSONField(verbose_name=_("Config"))

    class Meta:
        verbose_name = _("Common Json Config")
        verbose_name_plural = _("Common Json Configs")

    def __str__(self):
        return self.name


class Configuration(SingletonBaseModel, CachableModel):
    config = models.ManyToManyField(to=CommonConfigurationJsonConfig, verbose_name=_("Config"), blank=True)
    app_name = models.CharField(verbose_name=_("App Name"), max_length=255, default=settings.PROJECT_NAME)
    maintenance_mode = models.BooleanField(verbose_name=_('Maintenance mode'), default=False)

    class Meta:
        verbose_name = _("Configuration")
        verbose_name_plural = _("Configurations")

    @staticmethod
    def cache_key():
        return f'{Configuration.__name__}_CACHE'

    @staticmethod
    def load() -> 'Configuration':
        config = cache.get(Configuration.cache_key())

        if not config:
            config, c = Configuration.objects.get_or_create()
            cache.set(Configuration.cache_key(), pickle.dumps(config))
            return config

        return pickle.loads(config)

    def __str__(self):
        return self.app_name
