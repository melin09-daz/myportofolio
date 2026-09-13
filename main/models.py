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
    start_month = models.PositiveSmallIntegerField(blank=True, null=True, help_text="Bulan awal (1-12)") # Bulan awal
    end_month = models.PositiveSmallIntegerField(blank=True, null=True, help_text="Bulan akhir (1-12)") # Bulan akhir
    is_ongoing = models.BooleanField(default=True) # Condition
    
    MONTH_NAMES = {
        1: 'Januari', 2: 'Februari', 3: 'Maret', 4: 'April',
        5: 'Mei', 6: 'Juni', 7: 'Juli', 8: 'Agustus',
        9: 'September', 10: 'Oktober', 11: 'November', 12: 'Desember'
    }
    
    def __str__(self):
        return self.title
    
    def format_date(self, month, year):
        # Memformat pasangan bulan dan tahun, misal: 'Januari 2024' atau '2024'
        if month and year and month in self.MONTH_NAMES:
            return f"{self.MONTH_NAMES[month]} {year}"
        if year:
            return str(year)
        return "" 
    
    @property
    def period_display(self):
        # Menampilkan periode dengan bulan dan tahun
        start_str = self.format_date(self.start_month, self.start_year)
        end_str = self.format_date(self.end_month, self.end_year)

        if self.is_ongoing:
            if start_str:
                return f"{start_str} - Sekarang (Sedang berlangsung)"
            return "Sedang berlangsung"

        # Jika sudah selesai
        if start_str and end_str:
            if start_str == end_str:
                return f"{start_str} (Selesai)"
            return f"{start_str} - {end_str}"
        elif start_str:
            return f"{start_str} (Selesai)"
        elif end_str:
            return f"Selesai {end_str}"
        return "Selesai"

class Project(models.Model):
    PROJECT_CHOICES = [
        ('web-dev', 'Web Development'),
        ('mobile-dev', 'Mobile Development'),
        ('data-science', 'Data Science & AI'),
        ('ui-ux', 'UI/UX Design'),
        ('iot', 'Internet of Things'),
        ('other', 'Other'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=PROJECT_CHOICES, default='web-dev')
    tech_stack = models.CharField(max_length=255, blank=True, help_text="Contoh: Django, Python, PostgreSQL, Tailwind")
    repository_url = models.URLField(blank=True, null=True, help_text="Link ke GitHub/GitLab repository")
    demo_url = models.URLField(blank=True, null=True, help_text="Link ke live demo aplikasi")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
