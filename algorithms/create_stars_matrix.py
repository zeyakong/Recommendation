import random
import time

from restaurant.models import Business, Review


def create_matrix():
    reviews_list = Review.objects.all()
    for one in reviews_list:
        pass


def find_similar_user(cf_type, approach):
    time.sleep(random.randint(1,5))


def find_similar_rest():
    pass


def find_rest(user_list, rec_type):
    i = 0
    business_list = []
    for i in range(5):
        business = Business.objects.order_by('?').first()
        print(business)
        business_list.append(business)
    return business_list


if __name__ == '__main__':
    create_matrix()
