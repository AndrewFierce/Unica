from django.db import models
from datetime import date
from django.contrib.auth.models import User
from django.urls import reverse #Used to generate URLs by reversing the URL patterns

class Post(models.Model):
    """
    Model representing a Post.
    """
    title = models.CharField(max_length=200, help_text="Введите заголовок статьи")
    summary = models.TextField(help_text="Введите описание статьи")
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(upload_to='posts/%Y/%m/%d', height_field=None, width_field=None, max_length=100)
    modified_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    # ManyToManyField used because genre can contain many books. Books can cover many genres.
    # Genre class has already been defined so we can specify the object above.
    def __str__(self):
        """
        String for representing the Model object.
        """
        return self.title
    
    def get_absolute_url(self):
        """
        Returns the url to access a particular book instance.
        """
        return reverse('post-detail', args=[str(self.id)])
    
    class Meta:
    	ordering = ["title", "-modified_at"]

class Courses(models.Model):
    """
    Model representing a Post.
    """
    typeCourse = (
        ('a', 'BUSINESS'),
        ('b', 'MARKETING'),
        ('c', 'DESIGN'),
        ('d', 'DATABASE'),
        ('e', 'PROGRAM'),
    )
    course = models.CharField(max_length=1, choices=typeCourse, blank=True, default='b', help_text='Выберите тип курса')
    title = models.CharField(max_length=200, help_text="Введите название курса")
    priсe = models.FloatField(max_length=10, help_text="Введите цену курса")
    image = models.ImageField(upload_to='courses/%Y/%m/%d', height_field=None, width_field=None, max_length=100)
    modified_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        String for representing the Model object.
        """
        return self.title
    
    def get_absolute_url(self):
        """
        Returns the url to access a particular book instance.
        """
        return reverse('course-detail', args=[str(self.id)])
    
    class Meta:
        ordering = ["title", "-priсe"]

class Subscribers(models.Model):
    """
    Model representing a Post.
    """
    email = models.EmailField(max_length=254, blank=True, default="")
    courses = models.ManyToManyField(Courses, help_text="Выберете курс", default=None)
    confirmation = models.BooleanField(default=False)
    randomkey = models.CharField(max_length=100, help_text="Рандомный ключ")
    def __str__(self):
        """
        String for representing the Model object.
        """
        return self.email
    
    class Meta:
        ordering = ["email"]

    def display_courses(self):
        """
        Creates a string for the Genre. This is required to display genre in Admin.
        """
        return ', '.join([ str(courses.get_course_display() +" " + courses.title) for courses in self.courses.all()[:3] ])

    display_courses.id = 'Courses'