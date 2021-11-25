from django.urls import path
from .views import (api_root, SnippetHighlight, 
                    snippet_detail, snippet_list,user_list, 
                    SnippetListView, SnippetDetailView, 
                    SnippetListGenericView, SnippetDetailGenericView, 
                    SnippetGenericListCreateView, SnippetGenericRetrieveUpdateDestroyView,
                    UserList, UserDetail)

urlpatterns = [
    #api_root
    path('', api_root),
    #FUNCTION BASE VIEWS
    path('user_func/', user_list, name='user_list'),
    path('snippets_func/', snippet_list, name='snippet_list'),
    path('snippets_func/<int:pk>/', snippet_detail, name='snippet_detail'),
    #CLASS BASE VIEWS
    path('snippets_class/', SnippetListView.as_view(), name='snippet_class'),
    path('snippets_class/<int:pk>', SnippetDetailView.as_view(), name='snippet_class_detail'),
    #BASE GENERIC CLASS VIEWS
    path('snippets_genericclass/', SnippetListGenericView.as_view(), name='snippet_genericclass'),
    path('snippets_genericclass/<int:pk>', SnippetDetailGenericView.as_view(), name='snippet_genericclass_detail'),
    #GENERIC CLASS VIEWS
    path('snippets_fullgenericclass/', SnippetGenericListCreateView.as_view(), name='snippet_fullgenericclass'),
    path('snippets_fullgenericclass/<int:pk>', SnippetGenericRetrieveUpdateDestroyView.as_view(), name='snippet_fullgenericclass_detail'),

    #USER VIEWS
    path('users/', UserList.as_view(), name='user_class_list'),
    path('users/<int:pk>/', UserDetail.as_view(), name='user_class_detail'),

    #highlight
    path('snippets/<int:pk>/highlight/', SnippetHighlight.as_view(), name='snippet_hilight'),
]
