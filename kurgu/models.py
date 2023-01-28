from django.db import models
from crawler.models import Agreement

# Create your models here.
class KJ(models.Model):
    company = models.ForeignKey(Agreement)
    # Muhasebe
    client = models.CharField(default='', blank=True,max_length=250,verbose_name="Röportaj veren adı soyadı")
    title = models.CharField(default='', blank=True,max_length=250,verbose_name="Ekranda gözükecek unvan")
    instagram = models.CharField(default='', blank=True,max_length=50,verbose_name="İnstagram hesabı")
    website = models.CharField(default='', blank=True,max_length=250,verbose_name="Web adresi")
    tel = models.CharField(default='', blank=True,max_length=20,verbose_name="Tel no")
    sponser = models.CharField(default='', blank=True,max_length=250,verbose_name="ُSponsorluk")
    ad_banner = models.CharField(default='', blank=True,max_length=250,verbose_name="ُAlt bant reklam")
    play_time_as_minuate = models.CharField(default='', blank=True,max_length=2,verbose_name="Yayın dakikasi")
    agreement_price = models.CharField(default='', blank=True,max_length=250,verbose_name="Sözleşme Ücreti")
    Paid_price = models.CharField(default='', blank=True,max_length=250,)
    note = models.TextField(blank=True,default='',verbose_name="Not")

    # Kurgu 
    is_played = models.BooleanField(default=False,verbose_name="Yayınlanma")
    videos = models.BooleanField(default=False,verbose_name="Görseller")
    kj_detials = models.BooleanField(default=False,verbose_name="Görseller")
    banner = models.BooleanField(default=False,verbose_name="Afiş")
    presentation = models.BooleanField(default=False,verbose_name="Sunum")
    subtitle = models.BooleanField(default=False,verbose_name="Altyazı")
    youtube = models.BooleanField(default=False,verbose_name="Youtube")
    is_sent = models.BooleanField(default=False,verbose_name="Firmaya gönderim")
    play_date = models.DateTimeField(null=True, default=None,verbose_name="Yayın tarihi")

    def __str__(self):
        return f"{self.client}-{self.title}"
    class Meta:
        verbose_name = "Kj listesi"
        verbose_name_plural = "Kj listeleri"
