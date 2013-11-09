from django.contrib import admin
from .models import Chart, Page, PageChart


class PageChartInline(admin.TabularInline):
	model = PageChart


class ChartAdmin(admin.ModelAdmin):
	list_display = ('title',)
admin.site.register(Chart, ChartAdmin)


class PageAdmin(admin.ModelAdmin):
	prepopulated_fields = {"slug": ("title",)}
	list_display = ('title',)
	inlines = [PageChartInline]
admin.site.register(Page, PageAdmin)
