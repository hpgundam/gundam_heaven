from django import template

register = template.Library()

@register.filter(name='pre_page_range')
def pre_page_range(page, arg=0):
    '''
    :param page: current page
    :param arg: amount of pages in front of current page
    :return: range(start_page_no, current_page_no)
    '''
    current_page_no = page.number
    if arg == 0:
        return range(1, current_page_no)
    return range(current_page_no-arg, current_page_no)


@register.filter(name='after_page_range')
def after_page_range(page, arg=0):
    '''
    :param page: current page
    :param arg: amount of pages after current page
    :return: range(current_page_no+1, end_page_no+1)
    '''
    current_page_no = page.number
    if arg == 0:
        return range(current_page_no+1, page.paginator.num_pages+1)
    return range(current_page_no+1, current_page_no+1+arg)


@register.filter(name='liked_by')
def liked_by(article, user):
    followers = article.followers
    if followers is None or followers == '':
        return False
    return str(user.id) in followers.split(':')


