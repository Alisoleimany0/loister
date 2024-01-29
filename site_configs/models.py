from ckeditor.fields import RichTextField
from django.core.exceptions import ValidationError
from django.db import models


class ContactUs(models.Model):
    phone_number_field = models.CharField(max_length=50, blank=True, null=True)
    addresses_field = models.TextField(blank=True, null=True)
    contact_email = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = 'Contact Us'
        verbose_name_plural = 'Contact Us'

    def save(self, *args, **kwargs):
        if not self.pk and ContactUs.objects.exists():
            raise ValidationError("You can only create one instance of ContactUs")
        return super(ContactUs, self).save(*args, **kwargs)

    def __str__(self):
        return "Contact Us"


class SocialLink(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)
    link_address = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.name if self.name else "Social Link"


class SiteFace(models.Model):
    logo_image = models.ImageField(upload_to='logo/', blank=True, null=True)
    bottom_text = RichTextField(max_length=600, blank=True, null=True)

    class Meta:
        verbose_name = 'Site Face'
        verbose_name_plural = 'Site Face'

    def save(self, *args, **kwargs):
        if not self.pk and SiteFace.objects.exists():
            raise ValidationError("You can only create one instance of SiteFace")
        return super(SiteFace, self).save(*args, **kwargs)

    def __str__(self):
        return "Site Face"
