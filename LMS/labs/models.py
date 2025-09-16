from django.db import models
from django.utils import timezone

# Create your models here.

# -----------------------------
# 1) Role
# -----------------------------
class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


# -----------------------------
# 2) User Account
# -----------------------------
class UserAccount(models.Model):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(max_length=254, unique=True)
    password_hash = models.TextField()
    full_name = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=32, blank=True, null=True)
    role = models.ForeignKey(Role, on_delete=models.RESTRICT)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username


# -----------------------------
# 3) Lab
# -----------------------------
class Lab(models.Model):
    lab_code = models.CharField(max_length=50, unique=True, blank=True, null=True)
    name = models.CharField(max_length=255)
    location = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    lab_head = models.ForeignKey(UserAccount, on_delete=models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


# -----------------------------
# 4) PC
# -----------------------------
class PC(models.Model):
    lab = models.ForeignKey(Lab, on_delete=models.CASCADE)
    asset_tag = models.CharField(max_length=100, unique=True, blank=True, null=True)
    hostname = models.CharField(max_length=150, blank=True, null=True)
    serial_number = models.CharField(max_length=150, blank=True, null=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    mac_address = models.CharField(max_length=32, blank=True, null=True)
    manufacturer = models.CharField(max_length=100, blank=True, null=True)
    model = models.CharField(max_length=100, blank=True, null=True)
    cpu = models.CharField(max_length=200, blank=True, null=True)
    cpu_cores = models.IntegerField(blank=True, null=True)
    ram_mb = models.IntegerField(blank=True, null=True)
    storage_gb = models.IntegerField(blank=True, null=True)
    os_name = models.CharField(max_length=100, blank=True, null=True)
    os_version = models.CharField(max_length=100, blank=True, null=True)
    purchased_on = models.DateField(blank=True, null=True)
    warranty_until = models.DateField(blank=True, null=True)
    is_defective = models.BooleanField(default=False)
    defective_reason = models.TextField(blank=True, null=True)
    last_checked_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.hostname or f"PC-{self.id}"


# -----------------------------
# 5) Maintenance Request
# -----------------------------
class MaintenanceRequest(models.Model):
    PRIORITY_CHOICES = [
        (1, 'High'),
        (2, 'Normal'),
        (3, 'Low'),
    ]
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('closed', 'Closed'),
    ]

    pc = models.ForeignKey(PC, on_delete=models.SET_NULL, blank=True, null=True)
    requested_by = models.ForeignKey(UserAccount, on_delete=models.SET_NULL, blank=True, null=True, related_name='requested_maintenance')
    assigned_to = models.ForeignKey(UserAccount, on_delete=models.SET_NULL, blank=True, null=True, related_name='assigned_maintenance')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    priority = models.SmallIntegerField(choices=PRIORITY_CHOICES, default=2)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='open')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    resolved_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.title


# -----------------------------
# 6) Booking
# -----------------------------
class Booking(models.Model):
    STATUS_CHOICES = [
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('pending', 'Pending'),
    ]

    pc = models.ForeignKey(PC, on_delete=models.SET_NULL, blank=True, null=True)
    lab = models.ForeignKey(Lab, on_delete=models.SET_NULL, blank=True, null=True)
    booked_by = models.ForeignKey(UserAccount, on_delete=models.SET_NULL, blank=True, null=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    purpose = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='confirmed')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(end_time__gt=models.F('start_time')), name='check_end_after_start')
        ]

    def __str__(self):
        return f"Booking {self.id}"


# -----------------------------
# 7) Class Period
# -----------------------------
class ClassPeriod(models.Model):
    lab = models.ForeignKey(Lab, on_delete=models.CASCADE)
    pc = models.ForeignKey(PC, on_delete=models.SET_NULL, blank=True, null=True)
    subject = models.CharField(max_length=255)
    instructor = models.ForeignKey(UserAccount, on_delete=models.SET_NULL, blank=True, null=True)
    day_of_week = models.PositiveSmallIntegerField()  # 0=Sunday ... 6=Saturday
    period_start = models.TimeField()
    period_end = models.TimeField()
    recurring = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('lab', 'day_of_week', 'period_start', 'period_end')
        constraints = [
            models.CheckConstraint(check=models.Q(day_of_week__gte=0, day_of_week__lte=6), name='check_day_of_week')
        ]

    def __str__(self):
        return f"{self.subject} ({self.day_of_week})"


# -----------------------------
# 8) PC Availability
# -----------------------------
class PCAvailability(models.Model):
    pc = models.ForeignKey(PC, on_delete=models.CASCADE)
    class_period = models.ForeignKey(ClassPeriod, on_delete=models.CASCADE)
    is_available = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('pc', 'class_period')

    def __str__(self):
        return f"PC {self.pc.id} - Period {self.class_period.id}"

