from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    @property
    def name(self):
        return f"{self.first_name} {self.last_name}"

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}({self.username})>"

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
