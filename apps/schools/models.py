import uuid

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class University(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(
        max_length=250,
        unique=True,
        help_text="The official name of the university in full",
    )
    nickname = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        unique=True,
        help_text="The short unofficial names or abbreviation the university is known as e.g. eksu, adopoly, unilag",
    )
    slug = models.SlugField(blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.school_slug = slugify(self.name)
        return super().save(*args, **kwargs)


class Faculty(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    university = models.ForeignKey(
        University, related_name="faculties", on_delete=models.CASCADE
    )
    name = models.CharField(max_length=250, help_text="The official name of the faulty")
    nickname = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="The short unofficial name of the faculty if any",
    )

    def __str__(self):
        return f"{str(self.university)} : {self.name}"

    class Meta:
        verbose_name_plural = "faculties"
        # faculties from different universities can have the same name, but we don't want
        # the same university to have multiple faculties with the same name.
        constraints = [
            models.UniqueConstraint(
                fields=["university", "name"], name="unique_faculties"
            )
        ]


class Department(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    faculty = models.ForeignKey(
        Faculty, related_name="departments", on_delete=models.CASCADE
    )
    name = models.CharField(
        max_length=250, help_text="The official name of the department"
    )
    nickname = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        unique=True,
        help_text="The short unofficial name of the department if any",
    )

    def __str__(self):
        return f"{str(self.faculty)} : {self.name}"

    class Meta:
        # departments from different universities can have the same name, but we don't want
        # the same university to have multiple departments with the same name.
        constraints = [
            models.UniqueConstraint(
                fields=["faculty", "name"], name="unique_departments"
            )
        ]


class Association(models.Model):
    id = models.UUIDField(
        _("aid"), primary_key=True, default=uuid.uuid4, editable=False
    )
    name = models.CharField(
        _("association name"),
        max_length=250,
    )
    academic_session = models.PositiveSmallIntegerField(null=True, blank=True)
    faculty = models.ForeignKey(
        Faculty,
        related_name="associations",
        on_delete=models.CASCADE,
        null=True,
        help_text="Faculty should only be provided if the association is a faculty association",
    )
    department = models.ForeignKey(
        Department,
        related_name="associations",
        on_delete=models.CASCADE,
        null=True,
        help_text="Department should only be provided if the association is a department association",
    )

    president = models.OneToOneField(
        User, related_name="president_of", on_delete=models.CASCADE
    )
    general_secretary = models.OneToOneField(
        User, related_name="general_secretary_of", on_delete=models.CASCADE
    )
    treasurer = models.OneToOneField(
        User, related_name="treasurer_of", on_delete=models.CASCADE
    )

    association_history = models.JSONField(
        default=dict,
        help_text="store information about past association and the president information",
    )

    constituency_name = models.CharField(
        _("constituency name"), max_length=128, blank=True, null=True
    )
