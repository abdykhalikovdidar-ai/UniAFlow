from django.contrib import admin
from django.urls import path, include
from core import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # --- ВХОД И РЕГИСТРАЦИЯ ---
    path('', auth_views.LoginView.as_view(template_name='registration/login.html', redirect_authenticated_user=True), name='login'),
    path('register/', views.register, name='register'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    
    # --- ОСНОВНЫЕ СТРАНИЦЫ ---
    path('board/', views.index, name='index'),
    path('profile/', views.profile, name='profile'),
    path('stats/', views.stats, name='stats'),
    
    # --- ЗАДАНИЯ / ПРОЕКТЫ ---
    path('assignments/', views.assignments_page, name='assignments_page'),
    path('assignments/take/<int:assignment_id>/', views.take_assignment, name='take_assignment'),
    path('assignments/edit/<int:assignment_id>/', views.edit_assignment, name='edit_assignment'),
    path('assignments/delete/<int:assignment_id>/', views.delete_assignment, name='delete_assignment'),
    path('assignments/copy/<int:assignment_id>/', views.copy_assignment, name='copy_assignment'),

    # --- КАНБАН И ЗАДАЧИ ---
    path('add_task/', views.add_task, name='add_task'),
    path('edit_task/<int:task_id>/', views.edit_task, name='edit_task'),
    path('delete_task/<int:task_id>/', views.delete_task, name='delete_task'),
    path('update_status/', views.update_task_status, name='update_status'),
    
    # --- ПРОВЕРКА (УЧИТЕЛЬ) ---
    path('review_task/<int:task_id>/', views.review_task, name='review_task'),
    path('send_review/<int:task_id>/', views.send_review, name='send_review'),
    path('return_task/<int:task_id>/', views.return_task, name='return_task'),

    # --- ЖУРНАЛ ---
    path('teacher_journal/', views.teacher_journal, name='teacher_journal'),
    path('save_grade/', views.save_grade, name='save_grade'),
    path('download-transcript/', views.download_transcript, name='download_transcript'),
    
    # --- СООБЩЕНИЯ (ЧАТ) ---
    path('messages/', views.messages_page, name='messages_page'),
    path('messages/api/<int:user_id>/', views.get_messages_api, name='get_messages_api'),
    path('messages/send_api/', views.send_message_api, name='send_message_api'),
    path('messages/set_typing/', views.set_typing_status, name='set_typing_status'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)