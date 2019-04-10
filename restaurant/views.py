import collections
import json
import uuid

from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseRedirect
# Create your views here.
from django.urls import reverse
import datetime

from algorithms.create_stars_matrix import find_similar_user, find_rest
from algorithms.rating_based_algorithms import user_cf, rating_recommend
from algorithms.recommendation import rm_predict
from algorithms.text_based_algorithms import text_recommend
from .models import Business, Review
from users.models import UserReview, User
from django.db.models import Q
from django.http import JsonResponse


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
    has_review = 0
    if request.user.is_authenticated:
        if user_review_list.filter(user=request.user):
            has_review = 1
    context = {
        'business': business,
        'customer_review_list': customer_review_list,
        'user_review_list': user_review_list,
        'has_review': has_review
    }

    return render(request, 'restaurant/detail.html', context)


def review_operation(request, business_id):
    if request.method == 'DELETE':
        # delete that review
        print("get delete method: params", business_id)
        current_user = request.user
        user_review = UserReview.objects.filter(business_id=business_id, user__username=current_user.username)
        user_review.delete()
        return HttpResponse('ok')
    elif request.method == 'POST':
        print("get put method: params", business_id)
        # update the review
        rating = request.POST.get('star_rating')
        text = request.POST.get('text_review')
        username = request.POST.get('username')
        print('star:', rating, '|text', text, '|username:', username)
        user_review = UserReview.objects.get(business_id=business_id, user__username=username)
        user_review.text = text
        user_review.stars = rating
        user_review.save()
        return HttpResponseRedirect(reverse('restaurant:detail', args=(business_id,)))


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
    if request.method == 'POST':
        similarity_value = request.POST.get('similarityValue')
        method_value = request.POST.get('methodValue')
        print(similarity_value, method_value, user_name, request.user.username)

        # check the params, 0 == rating-based only
        if method_value == '0':
            top_similar_users, top_similar_restaurants = rating_recommend(username=request.user.username,
                                                                          similarity_method=similarity_value)
        elif method_value == '1':
            # 1 == bag-of-words
            top_similar_users, top_similar_restaurants = text_recommend(username=request.user.username,
                                                                        method='bag-of-words',
                                                                        similarity_method=similarity_value)
        elif method_value == '2':
            # 2 tf-idf
            top_similar_users, top_similar_restaurants = text_recommend(username=request.user.username,
                                                                        method='tfidf',
                                                                        similarity_method=similarity_value)
        elif method_value == '3':
            # 3 word2vec
            top_similar_users, top_similar_restaurants = text_recommend(username=request.user.username,
                                                                        method='word2vec',
                                                                        similarity_method=similarity_value)
        else:
            # 5 both
            top_similar_users, top_similar_restaurants = rating_recommend(username=request.user.username,
                                                                          similarity_method=similarity_value)
            top_similar_users_text, top_similar_restaurants_text = text_recommend(username=request.user.username,
                                                                                  method='bag-of-words',
                                                                                  similarity_method=similarity_value)
            top_similar_users = top_similar_users[0:7] + top_similar_users_text[0:8]
            top_similar_restaurants = top_similar_restaurants[0:3]
            top_restaurants_id = list()
            for one in top_similar_restaurants:
                top_restaurants_id.append(one[0])
            count = 0
            for one in top_similar_restaurants_text:
                if one[0] not in top_restaurants_id and count < 6:
                    top_similar_restaurants.append(one)
                    top_restaurants_id.append(one[0])
                    count = count + 1
        copy = dict()
        for one in top_similar_restaurants:
                copy[one[0]] = one[1]
        top_similar_restaurants = collections.Counter(copy).most_common(5)
        result = list()
        for one_rest in top_similar_restaurants:
            temp = dict()
            temp['id'] = one_rest[0]
            temp['name'] = Business.objects.get(business_id=one_rest[0]).name
            temp['stars'] = one_rest[1]
            result.append(temp)
        content = {
            'top_similar_users': top_similar_users,
            'top_similar_restaurants': top_similar_restaurants,
            'results': result,
            'msg': 'target user: ' + user_name + '. method: ' + method_value + '. similarity:' + similarity_value + '. algorithm: userCF'
        }
        return HttpResponse(json.dumps(content))
    else:
        user_review_list = UserReview.objects.filter(user=User.objects.get(username=user_name))
        context = {
            'user_review_list': user_review_list,
        }
        return render(request, 'restaurant/generate_rec.html', context)
