def user_profile(request):
    try:
        return {'profile': request.user}
    except Exception as e:
        return {}
