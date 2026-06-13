from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=50, blank=True)
    department = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.user.username


class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='articles/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    favorites = models.ManyToManyField(User, blank=True, related_name='favorite_articles')

    def __str__(self):
        return self.title

    def total_favorites(self):
        return self.favorites.count()


class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.article.title}'


class Quiz(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    question_text = models.CharField(max_length=255)
    option_a = models.CharField(max_length=200)
    option_b = models.CharField(max_length=200)
    option_c = models.CharField(max_length=200)
    option_d = models.CharField(max_length=200)
    correct_answer = models.CharField(
        max_length=1,
        choices=[
            ('A', 'A'),
            ('B', 'B'),
            ('C', 'C'),
            ('D', 'D'),
        ]
    )

    def __str__(self):
        return self.question_text


class QuizResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.IntegerField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.quiz.title} - {self.score}'
    
class PollutionReport(models.Model):
    POLLUTION_CHOICES = [
        ('plastic', '塑膠與一般垃圾'),
        ('oil', '油污污染'),
        ('chemical', '工業或化學廢水'),
        ('other', '其他民生污染'),
    ]
    
    # 關聯到會員，並設定如果會員被刪除，通報紀錄依然保留（設為匿名或 null）
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='reports')
    pollution_type = models.CharField(max_length=20, choices=POLLUTION_CHOICES, verbose_name="污染類型")
    location = models.CharField(max_length=250, verbose_name="通報地點")
    description = models.TextField(verbose_name="詳細描述")
    # 圖片會自動上傳到 media/pollution_pics/ 資料夾下
    image = models.ImageField(upload_to='pollution_pics/', verbose_name="現場照片")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="通報時間")

    def __str__(self):
        return f"{self.get_pollution_type_display()} - {self.location}"