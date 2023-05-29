
from django.contrib import admin

from todolist.goals.models.board import Board, BoardParticipant
from todolist.goals.models.category import GoalCategory
from todolist.goals.models.comment import Comment
from todolist.goals.models.goal import Goal


@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_deleted')
    readonly_fields = ('created', 'updated')

    fieldsets = (
        ('Info', {
            'fields': ('title',)
        }),
        ('Dates', {
            'fields': ('created', 'updated')
        }),
        ('Status', {
            'fields': ('is_deleted',)
        }),
    )


@admin.register(BoardParticipant)
class BoardParticipantAdmin(admin.ModelAdmin):
    list_display = ('board', 'user', 'role')
    readonly_fields = ('created', 'updated')
    list_filter = ("role",)

    fieldsets = (
        ('Info', {
            'fields': ('board', 'user')
        }),
        ('Dates', {
            'fields': ('created', 'updated')
        }),
    )


@admin.register(GoalCategory)
class GoalCategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'is_deleted')
    search_fields = ('title', 'user__username')
    readonly_fields = ('created', 'updated')

    fieldsets = (
        ('Info', {
            'fields': ('title', 'user')
        }),
        ('Dates', {
            'fields': ('created', 'updated')
        }),
        ('Status', {
            'fields': ('is_deleted',)
        }),
    )


@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'category', 'priority', 'status')
    search_fields = ('title', 'user__username', 'category__title')
    readonly_fields = ('created', 'updated', 'due_date')

    fieldsets = (
        ('Info', {
            'fields': ('title', 'user', 'category', 'priority')
        }),
        ('Dates', {
            'fields': ('created', 'updated', 'due_date')
        }),
        ('Status', {
            'fields': ('status',)
        }),
    )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('text', 'user', 'goal')
    search_fields = ('text', 'user__username', 'goal__title')
    readonly_fields = ('created', 'updated')

    fieldsets = (
        ('Info', {
            'fields': ('text', 'user', 'goal')
        }),
        ('Dates', {
            'fields': ('created', 'updated')
        }),
    )