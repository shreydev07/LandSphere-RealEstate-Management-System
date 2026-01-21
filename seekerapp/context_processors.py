from adminapp.models import Seeker

def seeker_info(request):
    seeker = None
    if request.session.get('seekerid'):
        try:
            seeker = Seeker.objects.get(id=request.session['seekerid'])
        except Seeker.DoesNotExist:
            seeker = None
    return {'seeker': seeker}