def get_messages(request):
    """ Получить сообщения в шаблоне """
    messages = request.session.get('messages', [])
    request.session['messages'] = []
    return messages

tags = {'get_messages': get_messages}