from django.core.paginator import Paginator, PageNotAnInteger, InvalidPage


def get_current_page(objects, amt_per_page, cur_page_no):
    paginator = Paginator(objects, amt_per_page)
    try:
        page = paginator.page(cur_page_no)
    except PageNotAnInteger:
        page = paginator.page(1)
    except InvalidPage:
        page = paginator.page(paginator.num_pages)
    return page

