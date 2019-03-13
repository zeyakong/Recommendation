import uuid

from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseRedirect
# Create your views here.
from django.urls import reverse
import datetime

from .models import Business, Review
from users.models import UserReview, User
from django.db.models import Q


def search_result(request):
    keywords = request.GET.get('keywords')
    address = request.GET.get('address')
    ordered = request.GET.get('ordered')
    page = request.GET.get('page') if request.GET.get('page') else 1

    # q = Q()

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
    if ordered == 'high-rated':
        business_list = business_list.order_by('-stars')
    else:
        business_list = business_list.order_by('-review_count')
    paginator = Paginator(business_list, 15)
    business_list = paginator.page(page)

    # this code will load the first text review to the restaurant. it might slow the system.
    for var in business_list:
        first_text = ''
        list_temp = Review.objects.filter(business_id=var.business_id)
        if list_temp[0] is not None:
            first_text = list_temp[0].text
        var.attributes = first_text[0:350]

    context = {
        'business_list': business_list,
    }
    return render(request, 'restaurant/search_result.html', context)


def detail(request, business_id):
    page_num = request.GET.get('page') if request.GET.get('page') else 1
    business = get_object_or_404(Business, pk=business_id)
    customer_review_list = Review.objects.filter(business_id=business_id).order_by('-date')
    paginator = Paginator(customer_review_list, 15)
    customer_review_list = paginator.page(page_num)
    user_review_list = UserReview.objects.filter(business_id=business_id).order_by('-date')
    context = {
        'business': business,
        'customer_review_list': customer_review_list,
        'user_review_list': user_review_list
    }

    return render(request, 'restaurant/detail.html', context)


def add_review(request, business_id):
    print('business id:', business_id)
    rating = request.POST.get('star_rating')
    text = request.POST.get('text_review')
    username = request.POST.get('username')
    print('star:', rating, '|text', text, '|username:', username)
    user_review = UserReview(id=uuid.uuid4(), business=Business.objects.get(business_id=business_id),
                             user=User.objects.get(username=username), stars=rating,
                             date=datetime.date.today(), text=text)
    user_review.save()

    return HttpResponseRedirect(reverse('restaurant:detail', args=(business_id,)))


def generate_rec(request, user_name):
    user_review_list = UserReview.objects.filter(user=User.objects.get(username=user_name))
    context = {
        'user_review_list': user_review_list,
    }
    return render(request, 'restaurant/generate_rec.html', context)
