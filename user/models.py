import uuid

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _

from user.manager import UserManager

"""
User choice selection fields below
"""

USER_PERMISSION_STATUS = (
    ("FPR", "FACULTY PRESIDENT"),
    ("DPR", "DEPARTMENT PRESIDENT"),
    ("GAD", "GENERAL ADMIN"),
)


USER_ACADEMIC_LEVEL = (
    (1, "100Level"),
    (2, "200Level"),
    (3, "300Level"),
    (4, "400Level"),
    (5, "500Level"),
    (6, "600Level"),
    (7, "700Level"),
)


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(
        _("uid"), primary_key=True, default=uuid.uuid4, editable=False
    )

    # USER BASIC INFORMATION
    first_name = models.CharField(
        _("first name"), max_length=200, blank=False, null=False
    )
    middle_name = models.CharField(_("middle name"), max_length=200)
    last_name = models.CharField(
        _("last name"), max_length=200, blank=False, null=False
    )
    email = models.EmailField(
        _("email address"), max_length=200, blank=False, null=False, unique=True
    )
    phone_number = models.CharField(
        _("phone number"), max_length=15, blank=False, null=False, unique=True
    )
    password = models.CharField(_("password"), max_length=128, blank=False, null=False)

    # USER ACADEMIC INFORMATION
    matric_no = models.CharField(_("matric no"), max_length=9, blank=True, null=True)
    level = models.PositiveSmallIntegerField(_("level"), choices=USER_ACADEMIC_LEVEL)

    # USER PERMISSION AND STATUS AND ROLE
    staff_role = models.CharField(
        _("user role"),
        max_length=100,
        choices=USER_PERMISSION_STATUS,
        blank=True,
        null=True,
    )
    is_admin = models.BooleanField(_("admin"), default=False)
    is_verified = models.BooleanField(_("verified"), default=False)
    is_active = models.BooleanField(_("active"), default=False)
    is_superuser = models.BooleanField(_("superuser"), default=False)

    # USER ACCOUNT LOGIN AND CREATION DATE
    last_login = models.DateTimeField(_("last login"), blank=True, null=True)
    created_at = models.DateTimeField(
        _("created date"),
        auto_now_add=True,
    )
    last_modified = models.DateTimeField(_("updated date"), auto_now=True)

    objects = UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
        "first_name",
        "last_name",
    ]

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def __str__(self):
        return self.first_name

    def has_perm(self, perm, obj=None):
        # Deos the user has specific permission, yes!
        return True

    def has_module_perms(self, app_label):
        # Does the user have permissions to view app 'app_label'
        return True

    @property
    def is_staff(self):
        return self.is_admin


UNIVERSITY_CHOICES = (
    ("eksu", "Ekiti State University"),
    ("fuoye", "Federal University of Oye Ekiti"),
    ("futa", "Federal University of Technology Akure"),
    ("adopoly", "Federal Polytechnic Ado Ekiti"),
    ("lasu", "Lagos State University"),
    ("unilag", "University of Lagos"),
)

FACULTY_ASSOCIATION_CHOICES = [
    ("sossa", "Social Sciences Student Association"),
    ("nabams", "National Association of Biochemistry Students"),
    ("nuesa", "National Union of Engineering Students Association"),
]

DEPARTMENT_ASSOCIATION_CHOICES = [
    ("naps1", "National Association of Psychology Students"),
    ("naps2", "National Association of Political Students"),
]


class Department(models.Model):
    id = models.UUIDField(
        _("did"), primary_key=True, default=uuid.uuid4, editable=False
    )
    name = models.CharField(
        _("department association"),
        max_length=200,
        blank=True,
        null=True,
        choices=DEPARTMENT_ASSOCIATION_CHOICES,
    )

    president = models.ForeignKey(
        User, related_name=_("dept_president"), on_delete=models.CASCADE
    )
    general_secretary = models.OneToOneField(
        User, related_name=_("dept_gen_sec"), on_delete=models.CASCADE
    )
    treasurer = models.OneToOneField(
        User, related_name=_("dept_treasurer"), on_delete=models.CASCADE
    )

    constituency_name = models.CharField(
        _("constituency name"), max_length=128, blank=True, null=True
    )

    def __str__(self):
        return self.name


class Faculty(models.Model):
    id = models.UUIDField(
        _("fid"), primary_key=True, default=uuid.uuid4, editable=False
    )
    name = models.CharField(
        _("faculty association"),
        max_length=200,
        blank=True,
        null=True,
        choices=FACULTY_ASSOCIATION_CHOICES,
    )

    president = models.ForeignKey(
        User, related_name=_("president"), on_delete=models.CASCADE
    )
    general_secretary = models.OneToOneField(
        User, related_name=_("general_secretary"), on_delete=models.CASCADE
    )
    treasurer = models.OneToOneField(
        User, related_name=_("treasurer"), on_delete=models.CASCADE
    )

    departments = models.ManyToManyField(Department, related_name=_("department"))

    constituency_name = models.CharField(
        _("constituency name"), max_length=128, blank=True, null=True
    )

    def __str__(self):
        return self.name


class Association(models.Model):
    id = models.UUIDField(
        _("aid"), primary_key=True, default=uuid.uuid4, editable=False
    )
    faculty_association = models.CharField(
        _("association name"),
        max_length=250,
        blank=True,
        null=True,
    )
    department_association = models.CharField(
        _("department association"), max_length=250, blank=True, null=True
    )


class SchoolSession(models.Model):
    id = models.UUIDField(
        _("sid"), primary_key=True, default=uuid.uuid4, editable=False
    )
    school_calender = models.DateField(_("school session"), auto_now_add=True)

    current_association = models.ForeignKey(
        Association,
        related_name="associations",
        on_delete=models.DO_NOTHING,
        help_text="current university session associations",
    )

    association_lead = models.ForeignKey(User, on_delete=models.CASCADE)

    past_association = models.JSONField(
        default=dict,
        help_text="store information about past association and the president information",
    )


class University(models.Model):
    id = models.UUIDField(
        _("uid"), primary_key=True, default=uuid.uuid4, editable=False
    )
    name = models.CharField(
        _("university name"),
        max_length=250,
        blank=True,
        null=True,
        choices=UNIVERSITY_CHOICES,
    )
    school_slug = models.SlugField(
        _("school abbrevation"),
        max_length=10,
        blank=True,
        null=True,
        help_text="short name abbrevation of the school,  e.g EKSU represents Ekiti State University.",
    )
    faculty = models.ManyToManyField(Faculty, related_name=_("faculty"))

    school_session = models.ForeignKey(
        SchoolSession, related_name="session", on_delete=models.DO_NOTHING
    )
