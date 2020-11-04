from django.urls import path

from users.views import CreateUserView, CreateTokeView, ManageUserView

app_name = "users"

urlpatterns = [
    path('create/', CreateUserView.as_view(), name='create'),
    path('token/', CreateTokeView.as_view(), name='token'),
    path('manage/', ManageUserView.as_view(), name='manage')


]