from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django_jalali.db import models as jmodels

from loister import utils


class ContactUs(models.Model):
    phone_number_field = RichTextField(verbose_name='شماره های تلفن', blank=True, null=True)
    addresses_field = models.TextField(verbose_name='آدرس ها', blank=True, null=True)
    contact_email = models.CharField(verbose_name='ایمیل', max_length=100, blank=True, null=True)
    extra_info = models.TextField(verbose_name='توضیحات اضافه', null=True, blank=True)

    class Meta:
        verbose_name = 'تماس با ما'
        verbose_name_plural = '3. تماس با ما'

    def save(self, *args, **kwargs):
        if not self.pk and ContactUs.objects.exists():
            raise ValidationError("You can only create one instance of ContactUs")
        return super(ContactUs, self).save(*args, **kwargs)

    def __str__(self):
        return "تماس با ما"


class UserContactMessage(models.Model):
    name = models.CharField(verbose_name='نام', max_length=50)
    email = models.EmailField(verbose_name='ایمیل')
    message = models.TextField(verbose_name='پیام')
    time = jmodels.jDateTimeField(auto_now_add=True)

    class Meta:
        ordering = 'time',
        verbose_name = 'پیام کاربر'
        verbose_name_plural = '7. پیام های کاربران'

    def __str__(self):
        return utils.truncate_text(self.message, 50)


class AboutUs(models.Model):
    text = RichTextUploadingField(verbose_name='متن')

    class Meta:
        verbose_name = "درباره ما"
        verbose_name_plural = "2. درباره ما"

    def __str__(self):
        return "درباره ما"


class SocialLink(models.Model):
    name = models.CharField(verbose_name='اسم', max_length=50, blank=True, null=True)
    link_address = models.CharField(verbose_name='آدرس لینک', max_length=50, blank=True, null=True)
    contact_us_object = models.ForeignKey('ContactUs', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'شبکه اجتماعی'
        verbose_name_plural = 'شبکه های اجتماعی'

    def __str__(self):
        return self.name if self.name else "لینک شبکه اجتماعی"


class SiteInfo(models.Model):
    site_domain = models.CharField(max_length=50, default='127.0.0.1', verbose_name='دامنه سایت')
    logo_image = models.ImageField(verbose_name='تصویر لوگو', upload_to='logo/', blank=True, null=True)
    logo_width = models.IntegerField(verbose_name='عرض لوگو', default=60)
    logo_height = models.IntegerField(verbose_name='ارتفاع لوگو', default=60)
    show_name_next_to_logo = models.BooleanField(verbose_name='نمایش نام سایت در کنار لوگو', default=True)
    site_name = models.CharField(verbose_name='اسم سایت', max_length=50, null=True)
    introduction_text = RichTextField(verbose_name='متن معرفی', max_length=600, blank=True, null=True)
    freight_cost = models.IntegerField(verbose_name='هزینه حمل', default=0)

    class Meta:
        verbose_name = 'اطلاعات سایت'
        verbose_name_plural = '1. اطلاعات سایت'

    def save(self, *args, **kwargs):
        if not self.pk and SiteInfo.objects.exists():
            raise ValidationError("You can only create one instance of SiteInfo")
        return super(SiteInfo, self).save(*args, **kwargs)

    def __str__(self):
        return "اطلاعات سایت"


class ETrustSymbol(models.Model):
    name = models.CharField(verbose_name='نام نماد', max_length=50)
    image = models.ImageField(verbose_name='تصویر نماد', null=True)
    image_link = models.CharField(verbose_name='لینک تصویر نماد', max_length=200, null=True)
    link = models.CharField(verbose_name='لینک نماد', max_length=200)

    class Meta:
        verbose_name = 'نماد اعتماد'
        verbose_name_plural = '6. نماد های اعتماد'

    def __str__(self):
        return self.name


class Rules(models.Model):
    rules = RichTextUploadingField(verbose_name='متن', blank=True, null=True)

    class Meta:
        verbose_name = 'قوانین'
        verbose_name_plural = '5. قوانین'

    def __str__(self):
        return "قوانین"


class HomepageCoverGroup(models.Model):
    show_video = models.BooleanField(default=False, verbose_name='ویدیو')

    def save(self, *args, **kwargs):
        if not self.pk and HomepageCoverGroup.objects.exists():
            raise ValidationError("You can only create one instance of HomepageCovers")
        return super(HomepageCoverGroup, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "کاور های صفحه اصلی"
        verbose_name_plural = "4. کاور های صفحه اصلی"

    def __str__(self):
        return "کاور های صفحه اصلی"


class HomepageCover(models.Model):
    group = models.ForeignKey(
        HomepageCoverGroup,
        on_delete=models.CASCADE,
    )
    title = models.CharField(verbose_name='عنوان', blank=True, max_length=30)
    description = models.CharField(verbose_name='توضیحات', blank=True, max_length=100)
    image = models.ImageField(verbose_name='تصویر', null=True)

    def __str__(self):
        return self.title


class HomepageVideo(models.Model):
    group = models.ForeignKey(
        HomepageCoverGroup,
        on_delete=models.CASCADE,
    )
    title = models.CharField(verbose_name='عنوان', blank=True, max_length=30)
    description = models.CharField(verbose_name='توضیحات', blank=True, max_length=100)
    video = models.FileField(verbose_name='ویدیو', null=True)

    def __str__(self):
        return self.title
