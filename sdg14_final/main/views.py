import requests
from bs4 import BeautifulSoup

from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from .models import Article, Comment, Quiz, QuizResult, UserProfile

from .models import PollutionReport
from .forms import PollutionReportForm


# ================= 新增爬蟲函式 =================
def fetch_latest_oca_news():
    """即時抓取海洋委員會海洋保育署的新聞快訊"""
    url = "https://www.oca.gov.tw/ch/home.jsp?id=14&parentpath=0,2"
    news_list = []
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        # 加上 verify=False 繞過政府網站 SSL 憑證問題
        response = requests.get(url, headers=headers, timeout=5, verify=False)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 根據截圖的 HTML 結構，新聞列表放在 <div class="list"> 裡的 <li> 標籤中
            list_items = soup.select('div.list ul li')

            # 只取前 3 筆最新消息
            for item in list_items[:3]:  
                # 1. 抓取網址 (a 標籤的 href)
                a_tag = item.find('a')
                if not a_tag:
                    continue
                
                link = a_tag.get('href', '')
                if link.startswith('home.jsp') or link.startswith('?'):
                    link = f"https://www.oca.gov.tw/ch/{link}"
                elif link.startswith('/'):
                    link = f"https://www.oca.gov.tw{link}"
                
                # 2. 抓取標題 (class="titlelist")
                title_div = item.find('div', class_='titlelist')
                title = title_div.get_text(strip=True) if title_div else ''
                
                # 3. 抓取日期 (class="date")
                date_div = item.find('div', class_='date')
                date_str = date_div.get_text(strip=True) if date_div else '最新消息'
                
                # 海保署的字串通常是 "發布日期 : 115-06-11   發布單位 : 秘書室"
                # 我們用 Python 字串處理把乾淨的日期切出來
                if '發布日期' in date_str:
                    # 用 '發布單位' 切開，拿前半段，再把多餘的文字和冒號清掉
                    date_str = date_str.split('發布單位')[0].replace('發布日期', '').replace('：', '').replace(':', '').strip()
                
                if title and link:
                    news_list.append({
                        'title': title,
                        'url': link,
                        'date': date_str
                    })
                    
    except Exception as e:
        print(f"爬蟲發生錯誤: {e}")
        news_list = [
            {'title': '暫時無法取得外部新聞，請稍後再試。', 'url': '#', 'date': '系統通知'}
        ]
        
    return news_list
# ===============================================


# ======== 修改：將爬蟲資料打包進首頁 ========
def home(request):
    # 1. 呼叫即時爬蟲函式取得最新消息
    oca_news = fetch_latest_oca_news()
    
    # 2. 撈取你原本資料庫裡的海洋圖鑑文章
    articles = Article.objects.all().order_by('-created_at')[:3]
    
    # 3. 一起打包傳給前端的 home.html
    context = {
        'news_list': oca_news,
        'articles': articles,
    }
    return render(request, 'home.html', context)
# ============================================


def article_list(request):
    articles = Article.objects.all().order_by('-created_at')
    return render(request, 'article_list.html', {'articles': articles})


def article_detail(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    comments = article.comments.all().order_by('-created_at')
    is_favorite = False

    if request.user.is_authenticated:
        is_favorite = article.favorites.filter(id=request.user.id).exists()

    context = {
        'article': article,
        'comments': comments,
        'is_favorite': is_favorite,
    }
    return render(request, 'article_detail.html', context)


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user)
            login(request, user)
            messages.success(request, '註冊成功，歡迎加入海洋保育學習平台！')
            return redirect('home')
    else:
        form = UserCreationForm()

    return render(request, 'register.html', {'form': form})


@login_required
def toggle_favorite(request, article_id):
    article = get_object_or_404(Article, id=article_id)

    if article.favorites.filter(id=request.user.id).exists():
        article.favorites.remove(request.user)
    else:
        article.favorites.add(request.user)

    return redirect('article_detail', article_id=article.id)


@login_required
def add_comment(request, article_id):
    article = get_object_or_404(Article, id=article_id)

    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Comment.objects.create(
                article=article,
                user=request.user,
                content=content
            )
            messages.success(request, '留言成功！')

    return redirect('article_detail', article_id=article.id)


def quiz_list(request):
    quizzes = Quiz.objects.all()
    return render(request, 'quiz_list.html', {'quizzes': quizzes})


@login_required
def quiz_detail(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = quiz.questions.all()

    if request.method == 'POST':
        score = 0
        for question in questions:
            user_answer = request.POST.get(str(question.id))
            if user_answer == question.correct_answer:
                score += 1

        QuizResult.objects.create(
            user=request.user,
            quiz=quiz,
            score=score
        )

        return render(request, 'quiz_result.html', {
            'quiz': quiz,
            'score': score,
            'total': questions.count(),
        })

    return render(request, 'quiz_detail.html', {
        'quiz': quiz,
        'questions': questions,
    })


@login_required
def profile(request):
    favorite_articles = request.user.favorite_articles.all()
    quiz_results = QuizResult.objects.filter(user=request.user).order_by('-submitted_at')

    return render(request, 'profile.html', {
        'favorite_articles': favorite_articles,
        'quiz_results': quiz_results,
    })

@login_required # 限制登入會員才能通報
def report_pollution(request):
    if request.method == 'POST':
        # ⚠️ 注意：處理檔案上傳必須傳入 request.FILES
        form = PollutionReportForm(request.POST, request.FILES)
        if form.is_valid():
            report = form.save(commit=False)
            report.user = request.user # 綁定當前登入的會員
            report.save()
            messages.success(request, '感謝您的通報！資料已成功送出並記錄。')
            return redirect('report_list')
    else:
        form = PollutionReportForm()
    
    return render(request, 'report_form.html', {'form': form})

def report_list(request):
    # 撈取所有通報紀錄，依時間由新到舊排序
    reports = PollutionReport.objects.all().order_by('-created_at')
    return render(request, 'report_list.html', {'reports': reports})