from django.contrib import admin
from .models import Article, Comment, Quiz, Question, QuizResult, UserProfile
from .models import PollutionReport


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'total_favorites')
    search_fields = ('title', 'content')
    list_filter = ('created_at',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('article', 'user', 'created_at')
    search_fields = ('content', 'user__username', 'article__title')
    list_filter = ('created_at',)


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('quiz', 'question_text', 'correct_answer')
    search_fields = ('question_text',)
    list_filter = ('quiz',)


@admin.register(QuizResult)
class QuizResultAdmin(admin.ModelAdmin):
    list_display = ('user', 'quiz', 'score', 'submitted_at')
    search_fields = ('user__username', 'quiz__title')
    list_filter = ('quiz', 'submitted_at')


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'nickname', 'department')
    search_fields = ('user__username', 'nickname', 'department')

@admin.register(PollutionReport)
class PollutionReportAdmin(admin.ModelAdmin):
    # 設定在後台列表中要顯示的欄位
    list_display = ('pollution_type', 'location', 'user', 'created_at')
    # 設定可以作為篩選條件的欄位（會出現在右側）
    list_filter = ('pollution_type', 'created_at')