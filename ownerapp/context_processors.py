from .models import Owner

def owner_info(request):
    owner = None
    if request.session.get('ownerid'):
        try:
            owner = Owner.objects.get(id=request.session['ownerid'])
        except Owner.DoesNotExist:
            owner = None
    return {'owner': owner}