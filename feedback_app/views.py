from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Message, Profile, WebStat
from django.db.models import F
from django.core.mail import send_mail
from datetime import date


response_limit = 200
base_url = "www.afsi.quest"



# Checks if request is ajax
def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'



def index(request):

    #Update statistics
    period = date.today().strftime ("%b, %Y")

    # Checks if current month/year stat has been created
    if WebStat.objects.all().filter(period=period):
        currentMonth = WebStat.objects.filter(period=period).update(homePage=F('homePage') + 1)

    else:
        currentMonth = WebStat(period=period, homePage=1)
        currentMonth.save()

    return render(request, 'index.html')



def profile(request):

    #Update statistics
    period = date.today().strftime ("%b, %Y")

    # Checks if current month/year stat has been created
    if WebStat.objects.all().filter(period=period):
        currentMonth = WebStat.objects.filter(period=period).update(profile=F('profile') + 1)

    else:
        currentMonth = WebStat(period=period, profile=1)
        currentMonth.save()

    personal_count = Message.objects.filter(belongs_to=request.user, purpose="private").count()
    personal_question = get_object_or_404(Profile, user=request.user ).personal_question
    business_count = Message.objects.filter(belongs_to=request.user, purpose="business").count()
    business_question = get_object_or_404(Profile, user=request.user ).business_question
    total= personal_count + business_count
    payment_status = get_object_or_404(Profile, user=request.user)
    username= str(request.user.username)
    personal_url = base_url+"/private/anonymous-message/"+username
    business_url = base_url+"/business/anonymous-message/"+username

    if payment_status.paid:
        responses = Message.objects.filter(belongs_to=request.user)
        user_type = "premium"
    else:
        responses = Message.objects.filter(belongs_to=request.user)[:response_limit]
        user_type = "basic"


    context = {
            'personal': personal_count,
            'personal_question': personal_question,
            'firstPartOfWordsPers': firstPartOfWords(personal_question),
            'lastTwoWordsPers': lastTwoWords(personal_question),
            'business': business_count,
            'business_question': business_question,
            'firstPartOfWordsBus': firstPartOfWords(business_question),
            'lastTwoWordsBus': lastTwoWords(business_question),
            'total': total,
            'user_type': user_type,
            'response_limit': response_limit,
            'personal_url': personal_url,
            'business_url': business_url,
            'responses': responses,
        }
    return render(request, 'profile.html', context)



def logout(request):
    auth.logout(request)
    return redirect('index')



def account(request):

    if is_ajax(request) and (request.GET.get('action')=="register"):


        #Get the form values
        username = request.GET.get('username')
        email = request.GET.get('email')
        password = request.GET.get('password')


        #Check if username already exists
        if User.objects.filter(username=username).exists():
            return JsonResponse({'registered': 'False', 'username_status': 'False', 'email_status': 'none'}, status=200)

        else:
            if User.objects.filter(email=email).exists():
                return JsonResponse({'registered': 'False', 'username_status': 'True', 'email_status': 'False'}, status=200)
            else:
                # Now the user can be created
                user = User.objects.create_user(username=username, password=password,
                email=email)
                user.save()
                newProfile = Profile(user=user, paid=False, total_response=0)
                newProfile.save()
                auth.login(request, user)
                return JsonResponse({'registered': 'True', 'username_status': 'True', 'email_status': 'True'}, status=200)


    if is_ajax(request) and (request.GET.get('action')=="login"):


        #Get the form values
        username = request.GET.get('username')
        password = request.GET.get('password')


        #Check if username already exists
        if not User.objects.filter(username=username).exists():
            return JsonResponse({'loggedin': 'False', 'username_status': 'False'}, status=200)

        else:
            try:
                # Now the user can be logged in
                user = auth.authenticate(username=username, password=password)
                auth.login(request, user)
                return JsonResponse({'loggedin': 'True', 'username_status': 'True'}, status=200)
            except:
                return JsonResponse({'loggedin': 'False', 'username_status': 'True'}, status=200)



def policy(request):

    #Update statistics
    period = date.today().strftime ("%b, %Y")

    # Checks if current month/year stat has been created
    if WebStat.objects.all().filter(period=period):
        currentMonth = WebStat.objects.filter(period=period).update(privacy_policy=F('privacy_policy') + 1)

    else:
        currentMonth = WebStat(period=period, privacy_policy=1)
        currentMonth.save()

    return render(request, 'policy.html')



def PrivateMessage(request, username):

    

    if request.method == 'POST':

        #Get the message
        message = request.POST['feedbackMessage']

        #Get the user Object
        user = get_object_or_404(User, username=username)
        email = user.email
        personal_question = get_object_or_404(Profile, user=user ).personal_question
        messageInstance = Message(message=message, belongs_to=user, purpose="private",personal_question=personal_question)
        messageInstance.save()

        Profile.objects.filter(user=user).update(total_response=F('total_response') + 1)
        
        #Update statistics
        period = date.today().strftime ("%b, %Y")

        # Checks if current month/year stat has been created
        if WebStat.objects.all().filter(period=period):
            currentMonth = WebStat.objects.filter(period=period).update(personal_message_post=F('personal_message_post') + 1)

        else:
            currentMonth = WebStat(period=period, personal_message_post=1)
            currentMonth.save()
        
        send_mail(
            'AN ANONYMOUS MESSAGE',
            'Hi there, \n\nSomeone has just sent you an anonymous message.\nKindly log in to your profile to see the response. \n\nClick on the link. https://www.afsi.quest/profile \n\nBest regards, \nAdmin',
            'admin@afsi.quest',
            [email],
            fail_silently=False
        )

        messages.success(request, 'Feedback sent Succesfully! Start yours now and get feedback from people')
        return redirect('index')

    #Update statistics
    period = date.today().strftime ("%b, %Y")

    # Checks if current month/year stat has been created
    if WebStat.objects.all().filter(period=period):
        currentMonth = WebStat.objects.filter(period=period).update(personal_message_open=F('personal_message_open') + 1)

    else:
        currentMonth = WebStat(period=period, personal_message_open=1)
        currentMonth.save()

    context = {
            'owner': username,
        }

    return render(request, 'privateMessage.html', context)



def BusinessMessage(request, username):

    
    if request.method == 'POST':

        #Get the message
        message = request.POST['feedbackMessage']

        #Get the user Object
        user = get_object_or_404(User, username=username)
        email = user.email
        business_question = get_object_or_404(Profile, user=user ).business_question
        messageInstance = Message(message=message, belongs_to=user, purpose="business", business_question=business_question)
        messageInstance.save()
        Profile.objects.filter(user=user).update(total_response=F('total_response') + 1)


        #Update statistics
        period = date.today().strftime ("%b, %Y")

        # Checks if current month/year stat has been created
        if WebStat.objects.all().filter(period=period):
            currentMonth = WebStat.objects.filter(period=period).update(business_message_post=F('business_message_post') + 1)

        else:
            currentMonth = WebStat(period=period, business_message_post=1)
            currentMonth.save()


        send_mail(
            'An ANONYMOUS MESSAGE',
            'Hi there, \n\nSomeone has just sent you an anonymous message.\nKindly log in to your profile to see the response. \n\nClick on the link. https://www.afsi.quest/profile \n\nBest regards, \nAdmin',
            'admin@afsi.quest',
            [email],
            fail_silently=False
        )

        messages.success(request, 'Feedback sent Succesfully! Start yours now and get feedback from people')
        return redirect('index')


    #Update statistics
    period = date.today().strftime ("%b, %Y")

    # Checks if current month/year stat has been created
    if WebStat.objects.all().filter(period=period):
        currentMonth = WebStat.objects.filter(period=period).update(business_message_open=F('business_message_open') + 1)

    else:
        currentMonth = WebStat(period=period, business_message_open=1)
        currentMonth.save()
        
    context = {
            'owner': username,
        }
    return render(request, 'businessMessage.html', context)



def contact(request):

    #Update statistics
    period = date.today().strftime ("%b, %Y")

    # Checks if current month/year stat has been created
    if WebStat.objects.all().filter(period=period):
        currentMonth = WebStat.objects.filter(period=period).update(contact_admin=F('contact_admin') + 1)

    else:
        currentMonth = WebStat(period=period, contact_admin=1)
        currentMonth.save()

    return render(request, 'contact.html')




def savequestion(request):

    if is_ajax(request) and (request.GET.get('type')=="personal"):


        #Get the form values
        persQuestion = request.GET.get('persQuestion')

        Profile.objects.filter(user=request.user).update(personal_question=persQuestion)

        #Update statistics
        period = date.today().strftime ("%b, %Y")

        # Checks if current month/year stat has been created
        if WebStat.objects.all().filter(period=period):
            currentMonth = WebStat.objects.filter(period=period).update(personal_quest_edit=F('personal_quest_edit') + 1)

        else:
            currentMonth = WebStat(period=period, personal_quest_edit=1)
            currentMonth.save()
        return JsonResponse({'saved': 'True', }, status=200)


    if is_ajax(request) and (request.GET.get('type')=="business"):


        #Get the form values
        busQuestion = request.GET.get('busQuestion')

        Profile.objects.filter(user=request.user).update(business_question=busQuestion)

        #Update statistics
        period = date.today().strftime ("%b, %Y")

        # Checks if current month/year stat has been created
        if WebStat.objects.all().filter(period=period):
            currentMonth = WebStat.objects.filter(period=period).update(business_quest_edit=F('business_quest_edit') + 1)

        else:
            currentMonth = WebStat(period=period, business_quest_edit=1)
            currentMonth.save()

        return JsonResponse({'saved': 'True', }, status=200)






def lastTwoWords(string):

    # split by space and converting
    # string to list and
    lis = list(string.split(" "))

    # length of list
    length = len(lis)

    # returning last element in list
    last = lis[length-1]
    sec2last = lis[length-2]
    last2sentence = sec2last+" "+last

    return last2sentence


def firstPartOfWords(string):

    # split by space and converting
    # string to list and
    lis = list(string.split(" "))


    # Remove the last 2 elements from a list (list slicing)
    new_list = lis[:len(lis) - 2]
    final_string = ' '.join(new_list)

    return final_string

