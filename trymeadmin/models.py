from django.db import models



class Category(models.Model):
    name = models.CharField(max_length=250)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "categories"
    
class Test(models.Model):
    title = models.CharField(max_length=250)
    description = models.TextField()
    subject = models.CharField(max_length=250)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title
    
class Question(models.Model):
    text = models.CharField(max_length=250)
    points = models.PositiveIntegerField()
    test = models.ForeignKey(Test)
    
    def __str__(self):
        return self.text
    

class Answer(models.Model):
    text = models.CharField(max_length=250)
    is_correct = models.BooleanField(default=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.text
    