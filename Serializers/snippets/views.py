from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer
from rest_framework.views import APIView


@csrf_exempt
def snippet_list(request):
    """
    List all code snippets, or create a new snippet.
    """
    # FOR show all objects from database
    if request.method == 'GET':
        snippets = Snippet.objects.all()
        serializer = SnippetSerializer(snippets, many=True)
        return JsonResponse(serializer.data, safe=False)
    
    # for saving an object
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = SnippetSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({'Job Done': True, 'status': 201})
        return JsonResponse({'Job Done': False, 'status': 400})


@csrf_exempt
def snippet_detail(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        snippet = Snippet.objects.get(pk=pk)
    except Snippet.DoesNotExist:
        return HttpResponse(status=404)
    print(snippet)
    
    if request.method == 'DELETE':
        print(request.method)
        snippet.delete()
        return HttpResponse(status=204)

    elif request.method == 'GET':
        print(request.method)
        serializer = SnippetSerializer(snippet)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        print(request.method)
        data = JSONParser().parse(request)
        serializer = SnippetSerializer(snippet, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({'Job Done': True, 'status': 201})
        return JsonResponse({'Job Done': False, 'status': 400})

    

@csrf_exempt
class SnippetListView(APIView):
    pass
