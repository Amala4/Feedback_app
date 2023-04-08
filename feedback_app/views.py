from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Message, Profile
from django.db.models import F

response_limit = 200
base_url = "www.afis.quest"



# Checks if request is ajax
def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'



def index(request):
    
    return render(request, 'index.html')



def profile(request):

    personal_count = Message.objects.filter(belongs_to=request.user, purpose="private").count()
    business_count = Message.objects.filter(belongs_to=request.user, purpose="business").count()
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
            'business': business_count,
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
    
    return render(request, 'policy.html')



def PrivateMessage(request, username):

    if request.method == 'POST':
        
        #Get the message
        message = request.POST['feedbackMessage']

        #Get the user Object
        user = get_object_or_404(User, username=username)  

        messageInstance = Message(message=message, belongs_to=user, purpose="private")
        messageInstance.save()

        Profile.objects.filter(user=user).update(total_response=F('total_response') + 1)

        messages.success(request, 'Feedback sent Succesfully! Start yours now and get feedback from people')
        return redirect('index')


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

        messageInstance = Message(message=message, belongs_to=user, purpose="business")
        messageInstance.save()
        Profile.objects.filter(user=user).update(total_response=F('total_response') + 1)


        messages.success(request, 'Feedback sent Succesfully! Start yours now and get feedback from people')
        return redirect('index')

    context = {
            'owner': username,
        }
    return render(request, 'businessMessage.html', context)



def contact(request):
    
    return render(request, 'contact.html')
