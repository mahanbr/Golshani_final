from managements.models import StaticData



def data(request):
    try:
        manager_data = StaticData.objects.first()
    except:
        manager_data = {}

    return {'manager_static_data' : manager_data}