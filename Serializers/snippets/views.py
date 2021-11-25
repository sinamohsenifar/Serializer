from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.http import Http404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User

from snippets.models import Snippet
from snippets.serializers import SnippetSerializer, SnippetModelSerializer, UserSerializer

from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import mixins
from rest_framework import generics
from rest_framework import permissions
from rest_framework import renderers
from .permissions import IsOwnerOrReadOnly


class SnippetHighlight(generics.GenericAPIView):
    queryset = Snippet.objects.all()
    renderer_classes = [renderers.StaticHTMLRenderer]

    def get(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)



@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user_list', request=request, format=format),
        'snippets': reverse('snippet_list', request=request, format=format),

        'snippet_class': reverse('snippet_class', request=request, format=format),
        
        'snippet_generic_class': reverse('snippet_genericclass', request=request, format=format),
        
        'snippet_full_generic_class': reverse('snippet_fullgenericclass', request=request, format=format),

        'users_class': reverse('user_class_list', request=request, format=format),

    })


@api_view(['GET', 'POST'])
@csrf_exempt
def user_list(request):
    """
    List all code snippets, or create a new snippet.
    """
    # FOR show all objects from database
    if request.method == 'GET':
        user = User.objects.all()
        serializer = UserSerializer(user, many=True)
        return JsonResponse(serializer.data, safe=False, status=status.HTTP_201_CREATED)
    
    # for saving an object
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({'Job Done': True}, status=status.HTTP_201_CREATED)
        return JsonResponse({'Job Done': False}, status=status.HTTP_400_BAD_REQUEST)




"""
    FUNCTION BASE VIEWS TO WORK WITH REST API   this views are very old methods
"""

@api_view(['GET', 'POST'])
@csrf_exempt
def snippet_list(request):
    """
    List all code snippets, or create a new snippet.
    """
    # FOR show all objects from database
    if request.method == 'GET':
        snippets = Snippet.objects.all()
        serializer = SnippetSerializer(snippets, many=True)
        return JsonResponse(serializer.data, safe=False, status=status.HTTP_201_CREATED)
    
    # for saving an object
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = SnippetSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({'Job Done': True}, status=status.HTTP_201_CREATED)
        return JsonResponse({'Job Done': False}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET', 'PUT', 'DELETE', 'PATCH'])
@csrf_exempt
def snippet_detail(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        snippet = Snippet.objects.get(pk=pk)
    except Snippet.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    print(snippet)
    
    if request.method == 'GET':
        print(request.method)
        serializer = SnippetSerializer(snippet)
        print(serializer.data)
        return Response({'item': serializer.data}, status=status.HTTP_201_CREATED)

    elif request.method == 'PUT':
        print(request.method)
        data = JSONParser().parse(request)
        serializer = SnippetSerializer(snippet, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'Job Done': True, 'item': serializer.data}, status=status.HTTP_201_CREATED)
        return Response({'Job Done': False}, status=status.HTTP_400_BAD_REQUEST)

    # this patch not working
    elif request.method== 'PATCH':
        data = JSONParser().parse(request)
        serializer = SnippetModelSerializer(instance=snippet, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'Job Done': True, 'item': serializer.data}, status=status.HTTP_201_CREATED)
        return Response({'Job Done': False}, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        print(request.method)
        title = snippet.title
        snippet.delete()
        return Response({'Item-Delete-Done': True, 'item title': title}, status=status.HTTP_201_CREATED)



"""
    THE BASIC CLASS BASE VIEWS TO WORK WITH REST API   we are using class base views but with basic level the classes are better than this 
"""

class SnippetListView(APIView):
    """
    List all snippets, or create a new snippet.
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get(self, request, format=None):
        snippets = Snippet.objects.all()
        serializer = SnippetSerializer(snippets, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = SnippetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'Job Done Response': True,'data_id': serializer.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class SnippetDetailView(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_object(self, pk):
        try:
            return Snippet.objects.get(pk=pk)
        except Snippet.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = SnippetSerializer(snippet)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = SnippetSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'Job Done Response': True,'data_id': serializer.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


"""
    WE ARE USING CLASS BASE VIEWS TO WORK WITH REST API   but with lesser code , we are using mixins and generic api view , we can do lesser code
"""


class SnippetListGenericView(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    """
    List all snippets, or create a new snippet.
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class SnippetDetailGenericView(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    """
    Retrieve, update or delete a snippet instance.
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


"""
    HERE WE ARE USING CLASS BASE VIEW WITH GENERIC LIST , CREATE , RETRIEVE , UPDATE AND DESTROY VIEWS WITH COMPRESSED CODING
"""

class SnippetGenericListCreateView(generics.ListCreateAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer

    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class SnippetGenericRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):

    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

'''
    here we get a list of users and the id of related snippets
'''

class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
