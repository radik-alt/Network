from django.db import models


class BookLover(models.Model):
    class Meta:
        db_table = 'BookLover'

    id_book_lover = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    middle_name = models.CharField(max_length=255, null=True)
    birthday = models.DateField(null=True)
    date_of_joining = models.DateField(null=True)
    address = models.CharField(max_length=255, null=True)
    phone = models.CharField(max_length=255, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.middle_name}"


class Book(models.Model):
    class Meta:
        db_table = "Book"

    id_book = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    publisher = models.ForeignKey("Publisher", on_delete=models.CASCADE, null=True)
    year_of_release = models.PositiveIntegerField(null=True)
    cover_photo = models.ImageField(upload_to='book_covers/', null=True)

    def __str__(self):
        return self.title


class Volume(models.Model):
    class Meta:
        db_table = "VolumeBook"

    id_volume = models.AutoField(primary_key=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='volumes')
    volume_number = models.PositiveIntegerField()
    number_of_pages = models.PositiveIntegerField()

    def __str__(self):
        return f"Volume {self.volume_number} of {self.book.title}"


class Region(models.Model):
    class Meta:
        db_table = "Region"
        unique_together = (('code', 'id'),)

    code = models.CharField(max_length=5, unique=True, verbose_name='Код области')
    name = models.CharField(max_length=100, verbose_name='Название области')

    def __str__(self):
        return f"{self.code} - {self.name}"


class Publisher(models.Model):
    class Meta:
        db_table = "Publisher"

    name = models.CharField(max_length=255, verbose_name='Название издательства')
    region = models.ForeignKey(Region, on_delete=models.CASCADE, verbose_name='Область', related_name='publishers')

    def __str__(self):
        return self.name


