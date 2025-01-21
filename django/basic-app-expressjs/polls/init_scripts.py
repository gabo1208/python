import random

gopt = GameOption.objects.all()
authors = Author.objects.all()
quotes = Quote.objects.all()

for i in range(len(gopt)):
    gopt[i].author = list(
        filter(lambda q: q['id'] == quotes[i]['author_id'], authors))[0]['name']
    gopt[i].save()
    i += 1

for i in range(len(gopt)):
    correctAnswerPosition = random.randint(3)
    for j in range(4):
        if j == correctAnswerPosition:
            if j == 0:
                gopt[i].option1 = gopt[i].author
            elif j == 1:
                gopt[i].option2 = gopt[i].author
            elif j == 2:
                gopt[i].option3 = gopt[i].author
            else:
                gopt[i].option4 = gopt[i].author
            j += 1
            continue

        random_author = random.choice(authors)
        if (random_author['name'] != gopt[i].author):
            if j == 0:
                gopt[i].option1 = random_author['name']
            elif j == 1:
                gopt[i].option2 = random_author['name']
            elif j == 2:
                gopt[i].option3 = random_author['name']
            else:
                gopt[i].option4 = random_author['name']
            j += 1
    gopt[i].save()
    i += 1
