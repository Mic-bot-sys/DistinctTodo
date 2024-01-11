from django.urls import path
from . import views


# create our urls here
urlpatterns = [
    path('', views.authentication, name='authentication'),
    path('register', views.registration, name='registration'),
    path('send-mail', views.sendMail, name='sendMail'),
    path('reset-password/<str:url>/', views.reset, name='reset'),
    
    path('home/', views.home, name='home'),
    path('create', views.createTodo, name='create'),    
    path('pending-todos/', views.getPendingTodosPartial, name='pendingTodosPartial'),
    path('get/<str:id>/', views.getTodoByIdPartial, name='getTodoByIdPartial'),
    path('get/search/<str:condition>/<str:value>/', views.getTodoBySearchValue, name='getTodoBySearchValue'),
    path('completed-todos/', views.getCompletedTodos, name='completedTodos'),
    path('updated-values/', views.getUpdatedTodoValues, name='updatedTodoValues'),
    
    path('complete', views.completeTodo, name='completeTodo'),
    path('edit/<str:id>', views.editTodoById, name='editTodo'),
    path('delete/<str:id>', views.deleteTodoById, name='deleteTodo'),
    
    
    path('logout/', views.logoutAuth, name='logout'),
]