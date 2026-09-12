import uuid
from django.db import models

class Experience(models.Model):
    EXPERIENCE_CHOICES = [
        ('internship', 'Internship'),
        ('research', 'Research'),
        ('volunteer', 'Volunteer'),
        ('part-time', 'Part-Time'),
        ('full-time', 'Full-Time'),
        ('freelance', 'Freelance'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=EXPERIENCE_CHOICES, default='full-time')
    thumbnail = models.URLField(blank=True, null=True)
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(blank=True, null=True)
    logo = models.CharField(max_length=255, blank=True, default='') # Kasih logo
    start_year = models.PositiveIntegerField(blank=True, null=True) # Tahun awal mulai
    end_year = models.PositiveIntegerField(blank=True, null=True) # Tahun akhir
    is_ongoing = models.BooleanField(default=True) # Condition
    
    def __str__(self):
        return self.title
    
    @property
    def period_display(self):
        # 'Sedang berlangsung' jika aktif, atau tahun awal - akhir jika sudah lewat.
        if self.is_ongoing:
            if self.start_year:
                return f"{self.start_year} - Sekarang (Sedang berlangsung)"
            return "Sedang berlangsung"
        
        # Jika sudah selesai/lewat
        if self.start_year and self.end_year:
            if self.start_year == self.end_year:
                return f"{self.start_year} (Selesai)"
            return f"{self.start_year} - {self.end_year} (Selesai)"
        elif self.start_year:
            return f"{self.start_year} (Selesai)"
        elif self.end_year:
            return f"Selesai {self.end_year}"
        return "Selesai"
    
    
    
