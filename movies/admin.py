from django.contrib import admin
from django.utils.safestring import mark_safe

from django import forms
from .models import Category, Genre, Movie, MovieShots, Actor, Rating, RatingStar, Reviews

from ckeditor_uploader.widgets import CKEditorUploadingWidget

# Register your models here.


class MovieAdminForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget(), label='Описание')

    class Meta:
        model = Movie
        fields = '__all__'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'url')
    list_display_links = ('name', )


class ReviewInLine(admin.TabularInline):
    model = Reviews
    extra = 1
    readonly_fields = ['name', 'email']


class MovieShotsInLine(admin.TabularInline):
    model = MovieShots
    extra = 1
    readonly_fields = ('get_image',)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width = "100" height = "60">')

    get_image.short_description = "Изображение"


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'url', 'draft', 'get_image')
    list_filter = ('category', 'year')
    search_fields = ('title', 'category__name')
    readonly_fields = ('get_image',)
    inlines = [MovieShotsInLine, ReviewInLine]
    save_on_top = True
    save_as = True
    list_editable = ('draft',)
    actions = ['publish', 'unpublish']
    form = MovieAdminForm
    # fields = (('actors', 'directors', 'genres'),)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.poster.url} width = "70" height = "100">')

    get_image.short_description = "Постер"

    def unpublish(self, request, queryset):
        row_update = queryset.update(draft=True)
        if row_update == 1:
            message_bit = '1 запись была обновлена'
        else:
            message_bit = f'{row_update} записей были обновлены'
        self.message_user(request, f'{message_bit}')

    def publish(self, request, queryset):
        row_update = queryset.update(draft=False)
        if row_update == 1:
            message_bit = '1 запись была обновлена'
        else:
            message_bit = f'{row_update} записей были обновлены'
        self.message_user(request, f'{message_bit}')

    publish.short_description = 'Опубликовать'
    unpublish.short_description = 'Снять с публикации'








@admin.register(Reviews)
class ReviewsAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'parent', 'movie', 'id')
    readonly_fields = ('name', 'email')


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'url')


@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    list_display = ('name', 'age', 'get_image')
    readonly_fields = ('get_image', )

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width = "50" height = "60">')

    get_image.short_description = "Изображение"


@admin.register(MovieShots)
class MovieShotsAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'movie', 'get_image')
    readonly_fields = ('get_image',)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width = "50" height = "60">')

    get_image.short_description = "Изображение"


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('ip', 'star', 'movie')


# admin.site.register(Genre)
# admin.site.register(Movie)
# admin.site.register(MovieShots)
# admin.site.register(Actor)
# admin.site.register(Rating)
admin.site.register(RatingStar)
# admin.site.register(Reviews)

admin.site.site_title = "Django Movies"
admin.site.site_header = "Django Movies"
