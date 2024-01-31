from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.core.exceptions import ValidationError
from django.db import models


class ContactUs(models.Model):
    phone_number_field = models.CharField(max_length=50, blank=True, null=True)
    addresses_field = models.TextField(blank=True, null=True)
    contact_email = models.CharField(max_length=100, blank=True, null=True)
    extra_info = models.TextField(null=True, blank=True)

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
    contact_us_object = models.ForeignKey('ContactUs', on_delete=models.CASCADE)

    def __str__(self):
        return self.name if self.name else "Social Link"


# TODO change name to SiteInfo
class SiteInfo(models.Model):
    logo_image = models.ImageField(upload_to='logo/', blank=True, null=True)
    site_name = models.CharField(max_length=50, null=True)
    introduction_text = RichTextField(max_length=600, blank=True, null=True)

    class Meta:
        verbose_name = 'Site Info'
        verbose_name_plural = 'Site Info'

    def save(self, *args, **kwargs):
        if not self.pk and SiteInfo.objects.exists():
            raise ValidationError("You can only create one instance of SiteFace")
        return super(SiteInfo, self).save(*args, **kwargs)

    def __str__(self):
        return "Site Info"


class Rules(models.Model):
    rules = RichTextUploadingField(blank=True, null=True)

    class Meta:
        verbose_name = 'Rules'
        verbose_name_plural = 'Rules'

    def __str__(self):
        return "Rules"


class HomepageCoverGroup(models.Model):
    def save(self, *args, **kwargs):
        if not self.pk and HomepageCoverGroup.objects.exists():
            raise ValidationError("You can only create one instance of HomepageCovers")
        return super(HomepageCoverGroup, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Homepage Covers"
        verbose_name_plural = "Homepage Covers"

    def __str__(self):
        return "Homepage Covers"


class HomepageCover(models.Model):
    group = models.ForeignKey(
        HomepageCoverGroup,
        on_delete=models.CASCADE
    )
    title = models.CharField(blank=True, max_length=30)
    description = models.CharField(blank=True, max_length=100)
    image = models.ImageField(null=True)

    def __str__(self):
        return self.title
