from django.contrib import admin


class BaseOwnerAdmin(admin.ModelAdmin):
    # 用来实现owner的自动显示; 用queryset过滤用户数据
    exclude = ('owner',)

    def get_queryset(self, request):
        queryset = super(BaseOwnerAdmin, self).get_queryset(request)
        return queryset.filter(owner=request.user)

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(BaseOwnerAdmin, self).save_model(request, obj, form, change)


