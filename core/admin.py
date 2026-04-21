from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.utils.html import format_html
from django.urls import reverse, path
from django.db.models import Max
from .models import Profile, Task, Message

# --- ПОЛЬЗОВАТЕЛИ ---
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False

class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)
    list_display = ('username', 'get_role', 'get_group', 'status_icon')
    def get_role(self, obj): return obj.profile.role
    def get_group(self, obj): return obj.profile.group_name
    def status_icon(self, obj):
        color = '#48bb78' if obj.profile.is_online() else '#718096'
        return format_html('<span style="color: {};">● {}</span>', color, 'Online' if obj.profile.is_online() else 'Offline')

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

# --- СООБЩЕНИЯ (ОДИН ЧЕЛОВЕК - ОДИН ДИАЛОГ) ---
@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender_name', 'text_preview', 'created_at', 'reply_link')
    
    # ЛОГИКА: Показываем только по одному последнему сообщению от каждого
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Оставляем только те сообщения, ID которых является максимальным (последним) для данного отправителя
        latest_ids = qs.values('sender').annotate(max_id=Max('id')).values_list('max_id', flat=True)
        return qs.filter(id__in=latest_ids).exclude(sender=request.user).order_by('-created_at')

    def sender_name(self, obj): return obj.sender.username
    sender_name.short_description = 'Пользователь'

    def text_preview(self, obj): return obj.text[:50] + "..."
    text_preview.short_description = 'Последнее сообщение'

    def reply_link(self, obj):
        url = reverse('admin:core_message_reply', args=[obj.pk])
        return format_html('<a class="button" href="{}" style="background:#0052cc; color:white; padding:5px 15px; border-radius:15px;">Открыть диалог</a>', url)
    reply_link.short_description = 'Чат'

    def get_urls(self):
        urls = super().get_urls()
        return [path('reply/<int:message_id>/', self.admin_site.admin_view(self.reply_view), name='core_message_reply')] + urls

    def reply_view(self, request, message_id):
        msg = get_object_or_404(Message, pk=message_id)
        target = msg.sender if msg.sender != request.user else msg.receiver
        if request.method == 'POST':
            txt = request.POST.get('reply_text')
            if txt:
                Message.objects.create(sender=request.user, receiver=target, text=txt)
                return HttpResponseRedirect(request.path)
        return render(request, 'admin/reply_form.html', {'target': target})