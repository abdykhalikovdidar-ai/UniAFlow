from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

# --- МОДЕЛЬ: ПРОФИЛЬ ПОЛЬЗОВАТЕЛЯ ---
class Profile(models.Model):
    ROLE_CHOICES = (('student', 'Студент'), ('teacher', 'Преподаватель'))
    GENDER_CHOICES = (('M', 'Мужской'), ('F', 'Женский'), ('O', 'Другой'))
    COURSE_CHOICES = (('1', '1 курс'), ('2', '2 курс'), ('3', '3 курс'), ('4', '4 курс'))
    LANGUAGE_CHOICES = (('RU', 'Русский'), ('KZ', 'Казахский'), ('EN', 'Английский'))
    EDU_LEVEL_CHOICES = (('BACHELOR', 'Бакалавриат'), ('MASTER', 'Магистратура'), ('PHD', 'Докторантура'))
    INSTRUCTION_LANGUAGES = (('RU', 'Русский'), ('KZ', 'Казахский'), ('EN', 'Английский'))
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student', verbose_name="Роль")
    image = models.ImageField(upload_to='avatars/', default='default.png', verbose_name="Аватар")
    bio = models.TextField(max_length=500, blank=True, verbose_name="О себе")
    
    phone_number = models.CharField(max_length=20, blank=True, null=True, verbose_name="Номер телефона")
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True, null=True, verbose_name="Пол")
    birth_date = models.DateField(null=True, blank=True, verbose_name="Дата рождения")
    
    course = models.CharField(max_length=1, choices=COURSE_CHOICES, blank=True, null=True, verbose_name="Курс")
    group_name = models.CharField(max_length=20, blank=True, null=True, verbose_name="Группа")
    language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES, default='RU', verbose_name="Язык обучения")
    academic_year = models.CharField(max_length=20, blank=True, null=True, verbose_name="Учебный год")
    study_duration = models.CharField(max_length=20, blank=True, null=True, verbose_name="Срок обучения")
    education_level = models.CharField(max_length=20, choices=EDU_LEVEL_CHOICES, default='BACHELOR', verbose_name="Уровень образования")
    
    # --- ПОЛЯ ДЛЯ УЧИТЕЛЯ ---
    department = models.CharField(max_length=150, blank=True, null=True, verbose_name="Кафедра")
    academic_degree = models.CharField(max_length=150, blank=True, null=True, verbose_name="Ученая степень")
    instruction_language = models.CharField(max_length=2, choices=INSTRUCTION_LANGUAGES, default='RU', verbose_name="Язык преподавания")
    experience = models.CharField(max_length=100, blank=True, null=True, verbose_name="Стаж работы")
    office_number = models.CharField(max_length=100, blank=True, null=True, verbose_name="Кабинет / Часы приема")
    office_hours = models.TextField(blank=True, null=True, verbose_name="Часы приема (подробно)")
    interests = models.TextField(blank=True, null=True, verbose_name="Научные интересы")

    last_seen = models.DateTimeField(null=True, blank=True, verbose_name="Был в сети")
    is_typing = models.BooleanField(default=False, verbose_name="Печатает")

    def is_online(self):
        """Проверка онлайн-статуса (активность за последние 5 минут)"""
        if self.last_seen:
            return timezone.now() - self.last_seen < timedelta(minutes=5)
        return False
    
    is_online.boolean = True
    is_online.short_description = 'В сети'

    def __str__(self):
        return f"{self.user.username} ({self.get_role_display()})"

    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"

# --- МОДЕЛЬ: ЗАДАНИЯ ОТ УЧИТЕЛЯ ---
class Assignment(models.Model):
    DIFFICULTY_CHOICES = (
        ('easy', 'Легкая'),
        ('medium', 'Средняя'),
        ('hard', 'Высокая'),
    )

    title = models.CharField(max_length=200, verbose_name="Название проекта")
    description = models.TextField(verbose_name="Описание задачи")
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='given_assignments', verbose_name="Преподаватель")
    
    target_course = models.CharField(max_length=50, blank=True, null=True, verbose_name="Для курса (номер)")
    target_group = models.CharField(max_length=50, blank=True, null=True, verbose_name="Для группы (название)")
    
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='medium', verbose_name="Сложность")
    bonus_points = models.IntegerField(default=0, verbose_name="Бонусные баллы")
    
    deadline = models.DateTimeField(verbose_name="Дедлайн")
    file = models.FileField(upload_to='assignments/', null=True, blank=True, verbose_name="Материалы")
    type = models.CharField(max_length=50, default='word', verbose_name="Формат файла")
    
    max_grade = models.IntegerField(default=100, verbose_name="Макс. балл") 
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def is_expired(self):
        return timezone.now() > self.deadline

    def __str__(self):
        return f"{self.title} | {self.target_group}"

    class Meta:
        verbose_name = "Проект/Задание"
        verbose_name_plural = "Проекты/Задания"
        ordering = ['-created_at']

# --- МОДЕЛЬ: ЗАДАЧИ СТУДЕНТА ---
class Task(models.Model):
    STATUS_CHOICES = (('todo', 'План'), ('doing', 'В работе'), ('done', 'Готово'))
    
    title = models.CharField(max_length=200, verbose_name="Название")
    description = models.TextField(blank=True, verbose_name="Описание")
    executor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks', null=True, blank=True, verbose_name="Исполнитель")
    
    assignment = models.ForeignKey(Assignment, on_delete=models.SET_NULL, null=True, blank=True, related_name='tasks')
    
    file = models.FileField(upload_to='tasks/', null=True, blank=True, verbose_name="Файл")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='todo', verbose_name="Статус")
    grade = models.IntegerField(null=True, blank=True, verbose_name="Оценка")
    is_verified = models.BooleanField(default=False, verbose_name="Проверено")
    teacher_comment = models.TextField(blank=True, null=True, verbose_name="Комментарий учителя")
    
    submitted_at = models.DateTimeField(null=True, blank=True, verbose_name="Дата сдачи")
    # Изменено: убрали auto_now_add чтобы можно было ставить оценки за любую дату в журнале
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Дата создания")

    def __str__(self):
        return self.title

    @property
    def lateness_status(self):
        if not self.assignment or not self.submitted_at:
            return None
        if self.submitted_at <= self.assignment.deadline:
            return {'text': 'В срок', 'color': '#10b981', 'is_late': False}
        diff = self.submitted_at - self.assignment.deadline
        hours = diff.total_seconds() // 3600
        status_text = "Опоздание < 1ч" if hours < 1 else f"Опоздание {int(hours)}ч"
        return {'text': status_text, 'color': '#ef4444', 'is_late': True}

    class Meta:
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"

# --- МОДЕЛЬ: СООБЩЕНИЕ (ЧАТ) ---
class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages', verbose_name="Отправитель")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages', null=True, blank=True, verbose_name="Получатель")
    text = models.TextField(verbose_name="Текст сообщения")
    is_read = models.BooleanField(default=False, verbose_name="Прочитано")
    is_to_admin = models.BooleanField(default=False, verbose_name="Для админа")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Время")

    def __str__(self):
        return f"От {self.sender.username} ({self.created_at.strftime('%d.%m %H:%M')})"

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"
        ordering = ['created_at']