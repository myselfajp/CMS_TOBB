from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class KJStatus(models.Model):
    name = models.CharField(max_length=25,verbose_name = "Adı")
    color = models.CharField(max_length=25,verbose_name = "Rengi(İngilizce reng)")
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "KJ kurgu Durumu"
        verbose_name_plural = "KJ kurgu Durumları"

class KJStatusAccounting(models.Model):
    name = models.CharField(max_length=25,verbose_name = "Adı")
    color = models.CharField(max_length=25,verbose_name = "Rengi(İngilizce reng)")
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "KJ muhasebe Durumu"
        verbose_name_plural = "KJ muhasebe Durumları"

class KJ(models.Model):
    company = models.CharField(default='', blank=True,max_length=250,verbose_name="Firma unvanı")
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True,verbose_name = "Kullanıcı")

    # Muhasebe
    client = models.CharField(default='', blank=True,max_length=250,verbose_name="Röportaj veren adı soyadı")
    nikname = models.CharField(default='', blank=True,max_length=250,verbose_name="Kişi unvanı")
    title = models.CharField(default='', blank=True,max_length=250,verbose_name="Ekranda gözükecek unvan")
    instagram = models.CharField(default='', blank=True,max_length=50,verbose_name="İnstagram hesabı")
    website = models.CharField(default='', blank=True,max_length=250,verbose_name="Web adresi")
    tel = models.CharField(default='', blank=True,max_length=20,verbose_name="Tel no")
    sponser = models.CharField(default='', blank=True,max_length=250,verbose_name="ُSponsorluk")
    ad_banner = models.CharField(default='', blank=True,max_length=250,verbose_name="ُAlt bant reklam")
    play_time_as_minuate = models.CharField(default='', blank=True,max_length=2,verbose_name="Yayın dakikasi")
    note = models.TextField(blank=True,default='',verbose_name="Not")

    # Kurgu 
    is_played = models.BooleanField(default=False,verbose_name="Yayınlanma")
    videos = models.BooleanField(default=False,verbose_name="Görseller")
    kj_detials = models.BooleanField(default=False,verbose_name="Görseller")
    banner = models.BooleanField(default=False,verbose_name="Afiş")
    presentation = models.TextField(default='',verbose_name="Sunum")
    subtitle = models.BooleanField(default=False,verbose_name="Altyazı")
    youtube = models.BooleanField(default=False,verbose_name="Youtube")
    is_sent = models.BooleanField(default=False,verbose_name="Firmaya gönderim")
    montaj = models.BooleanField(default=False,verbose_name="Montaj")
    status = models.ForeignKey(KJStatus,blank=True,null=True,on_delete=models.CASCADE)
    status_accounting = models.ForeignKey(KJStatusAccounting,null=True,on_delete=models.CASCADE)
    play_date = models.DateField(default=None,null=True,verbose_name="Yayın tarihi")
    record_date = models.DateTimeField(null=True,verbose_name = "Çekim tarihi")


    def __str__(self):
        return self.company
    class Meta:
        verbose_name = "Kj listesi"
        verbose_name_plural = "Kj listeleri"
