from restaurant.models import Business

business_list = Business.objects.all()

city = list()

for one in business_list:
    if one.city not in city:
        city.append(one.city)

print(len(city))
print(city)
