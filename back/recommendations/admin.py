from django.contrib import admin
from .models import UserLog, RecommendationCache


@admin.register(UserLog)
class UserLogAdmin(admin.ModelAdmin):
    """사용자 행동 로그 Admin"""
    list_display = ['id', 'user', 'performance', 'action_type', 'timestamp']
    list_filter = ['action_type', 'timestamp']
    search_fields = ['user__username', 'performance__prfnm']
    readonly_fields = ['timestamp']
    date_hierarchy = 'timestamp'
    ordering = ['-timestamp']

    def get_queryset(self, request):
        """성능 최적화: select_related 사용"""
        qs = super().get_queryset(request)
        return qs.select_related('user', 'performance')


@admin.register(RecommendationCache)
class RecommendationCacheAdmin(admin.ModelAdmin):
    """추천 캐시 Admin"""
    list_display = ['user', 'recommendation_count', 'updated_at']
    search_fields = ['user__username']
    readonly_fields = ['updated_at']
    ordering = ['-updated_at']

    def recommendation_count(self, obj):
        """추천 개수 표시"""
        return len(obj.top_n_list) if obj.top_n_list else 0
    recommendation_count.short_description = '추천 개수'

    def get_queryset(self, request):
        """성능 최적화: select_related 사용"""
        qs = super().get_queryset(request)
        return qs.select_related('user')
