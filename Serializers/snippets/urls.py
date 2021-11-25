from django.urls import path
from .views import (snippet_detail, snippet_list, 
                    SnippetListView, SnippetDetailView, 
                    SnippetListGenericView, SnippetDetailGenericView, 
                    SnippetGenericListCreateView, SnippetGenericRetrieveUpdateDestroyView,
                    UserList, UserDetail)

urlpatterns = [
    #FUNCTION BASE VIEWS
    path('snippets_func/', snippet_list),
    path('snippets_func/<int:pk>/', snippet_detail),
    #CLASS BASE VIEWS
    path('snippets_class/', SnippetListView.as_view()),
    path('snippets_class/<int:pk>', SnippetDetailView.as_view()),
    #BASE GENERIC CLASS VIEWS
    path('snippets_genericclass/', SnippetListGenericView.as_view()),
    path('snippets_genericclass/<int:pk>', SnippetDetailGenericView.as_view()),
    #GENERIC CLASS VIEWS
    path('snippets_fullgenericclass/', SnippetGenericListCreateView.as_view()),
    path('snippets_fullgenericclass/<int:pk>', SnippetGenericRetrieveUpdateDestroyView.as_view()),

    #USER VIEWS
    path('users/', UserList.as_view()),
    path('users/<int:pk>/', UserDetail.as_view()),
]
