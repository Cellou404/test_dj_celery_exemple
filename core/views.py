from django.http import JsonResponse


def custom_404_view(request, exception=None):
    return JsonResponse({
        'detail': 'Ressource non trouvé',
        'status_code': 404
    }, status=404)


def custom_500_view(request):
    return JsonResponse({
        'detail': 'Une erreur est survenue veuillez réessayer ultérieurement',
        'status_code': 500
    }, status=500)
