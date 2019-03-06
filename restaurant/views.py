from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseRedirect
# Create your views here.
from django.urls import reverse
import datetime

from .models import Business, Review
from users.models import UserReview
from django.db.models import Q


def search_result(request):
    keywords = request.GET.get('keywords')
    address = request.GET.get('address')
    print(keywords, address)

    # q = Q()
    #
    # for var in category_list:
    #     q = Q(categories=var) | q

    if ',' in keywords:
        keywords = keywords[0:keywords.find(',')]

    if keywords == '' and address != '':
        business_list = Business.objects.filter(Q(city__iregex=address))
    elif address == '' and keywords != '':
        business_list = Business.objects.filter(
            Q(name__iregex=keywords) | Q(categories__iregex=keywords))
    else:
        business_list = Business.objects.filter(
            (Q(name__iregex=keywords) | Q(categories__iregex=keywords)) & (Q(address__iregex=address) | Q(
                city__iregex=address)))
    # business_list = business_list.order_by('-review_count')
    paginator = Paginator(business_list, 15)
    business_list = paginator.page(1)

    # this code will load the first text review to the restaurant. it might slow the system.
    for var in business_list:
        first_text = ''
        list = Review.objects.filter(business_id=var.business_id)
        if list[0] is not None:
            first_text = list[0].text
        var.attributes = first_text[0:350]

    context = {
        'business_list': business_list,
    }
    return render(request, 'restaurant/search_result.html', context)


def detail(request, business_id):
    # context = ''
    # return render(request, 'restaurant/search_result.html', context)
    business = get_object_or_404(Business, pk=business_id)
    review_list = Review.objects.filter(business_id=business_id)
    paginator = Paginator(review_list, 15)
    review_list = paginator.page(1)
    context = {
        'business': business,
        'review_list': review_list
    }

    return render(request, 'restaurant/detail.html', context)


def add_review(request, business_id):
    print('business id:', business_id)
    v1 = request.POST.get('star_rating')
    v2 = request.POST.get('text_review')
    v3 = request.POST.get('username')
    print('star:', v1, '|text', v2, '|username:', v3)
    # user_review = UserReview(business_id=business_id, user_name=v3, stars=v1, date=datetime.datetime.now(), text=v2)
    # user_review.save()

    return HttpResponseRedirect(reverse('restaurant:detail', args=(business_id,)))
