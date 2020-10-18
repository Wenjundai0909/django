from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from typeidea.custom_site import custom_site
from typeidea.base_admin import BaseOwnerAdmin
from .models import Post, Category, Tag
from .adminforms import PostAdminForm


# class PostInline(admin.TabularInline):
#     fields = ('title', 'desc')
#     extra = 1
#     model = Post


@admin.register(Category, site=custom_site)
class CategoryAdmin(BaseOwnerAdmin):
    # inlines = [PostInline, ]
    list_display = ('name', 'status', 'is_nav', 'owner', 'created_time')
    fields = ('name', 'status', 'is_nav')

    # def save_model(self, request, obj, form, change):
    #     obj.owner = request.user
    #     return super(CategoryAdmin, self).save_model(request, obj, form, change)
    #
    # # 列表页面的内容只显示当前超级用户创建的内容
    # def get_queryset(self, request):
    #     queryset = super(CategoryAdmin, self).get_queryset(request)
    #     return queryset.filter(owner=request.user)

    def post_count(self, obj):
        return obj.post_set.count()

    post_count.short_description = '文章数量'


class CategoryOwnerFilter(admin.SimpleListFilter):
    # 侧边自定义过滤器只显示当前超级用户创建的内容
    title = '分类过滤'
    parameter_name = 'owner_category'

    def lookups(self, request, model_admin):
        return Category.objects.filter(owner=request.user).values_list('id', 'name')

    def queryset(self, request, queryset):
        category_id = self.value()
        if category_id:
            return queryset.filter(category_id=self.value())
        return queryset


@admin.register(Tag, site=custom_site)
class TagAdmin(BaseOwnerAdmin):
    list_display = ('name', 'status', 'owner', 'created_time')
    fields = ('name', 'status')

    # def save_model(self, request, obj, form, change):
    #     obj.owner = request.user
    #     return super(TagAdmin, self).save_model(request, obj, form, change)
    #
    # # 列表页面的内容只显示当前超级用户创建的内容
    # def get_queryset(self, request):
    #     queryset = super(TagAdmin, self).get_queryset(request)
    #     return queryset.filter(owner=request.user)


@admin.register(Post, site=custom_site)
class PostAdmin(BaseOwnerAdmin):
    form = PostAdminForm
    list_display = [
        'title', 'category', 'status',
        'created_time', 'owner', 'operator'
    ]
    list_display_links = []

    list_filter = [CategoryOwnerFilter]
    search_fields = ['title', 'category_name']

    # fields = (
    #     ('category', 'title'),
    #     'desc',
    #     'status',
    #     'content',
    #     'tag',
    # )
    fieldsets = (
        ('文章基础信息设置', {
            'fields': (
                ('title', 'category'),
                'status',
            ),
        }),
        ('文章摘要', {
            'classes': ('collapse',),
            'fields': ('desc',),
        }),
        ('文章正文内容', {
            'fields': (
                'content',
            ),
        }),
        ('额外信息', {
            'fields': ('tag',),
        })
    )

    def operator(self, obj):
        return format_html(
            '<a href="{}">编辑</a>',
            reverse('cus_admin:blog_post_change', args=(obj.id,))
        )
    operator.short_description = '操作'

    # def save_model(self, request, obj, form, change):
    #     obj.owner = request.user
    #     return super(PostAdmin, self).save_model(request, obj, form, change)
    #
    # # 列表页面的内容只显示当前超级用户创建的内容
    # def get_queryset(self, request):
    #     queryset = super(PostAdmin, self).get_queryset(request)
    #     return queryset.filter(owner=request.user)
