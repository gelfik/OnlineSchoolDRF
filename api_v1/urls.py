from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from rest_framework_swagger.views import get_swagger_view

# from rest_framework import permissions
# from drf_yasg import openapi
# from drf_yasg.views import get_schema_view

app_name = 'api_v1'

urlpatterns = [
    path('/users', include('UserProfileApp.urls', namespace='UserProfileApp')),
    path('/main', include('MainContentApp.urls', namespace='MainContentApp')),
    path('/courses', include('CoursesApp.urls', namespace='CoursesApp')),
    path('/lessons', include('LessonApp.urls', namespace='LessonApp')),
    path('/promocode', include('PromocodeApp.urls', namespace='PromocodeApp')),
    path('/purchase', include('PurchaseApp.urls', namespace='PurchaseApp')),
    path('/progress', include('ProgressApp.urls', namespace='ProgressApp')),
    path('/apanel', include('APanelApp.urls', namespace='APanelApp')),
    path('/tatar', include('TatarApp.urls', namespace='TatarApp')),
    # path('file/', include('fileapp.urls', namespace='fileapp')),
]

# schema_view = get_schema_view(
#     openapi.Info(
#         title="izzibrain API",
#         default_version='v1',
#     ),
#     public=True,
#     permission_classes=(permissions.AllowAny,),
#     patterns=urlpatterns,
# )
#
# urlpatterns += [
#     url(r'^/doc(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
#     url(r'^/doc$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
#     url(r'^/redoc$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
#     # path('/doc', schema_view.with_ui('swagger', cache_timeout=0)),
# ]
