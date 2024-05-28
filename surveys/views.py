from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, LoginForm, SurveyForm
from .models import Survey, Log
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import user_passes_test

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect_based_on_role(user)
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect_based_on_role(user)
            else:
                return render(request, 'login.html', {'form': form, 'error': 'Invalid credentials'})
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def redirect_based_on_role(user):
    if user.role == 'admin':
        return redirect('create_survey')
    elif user.role == 'manager':
        return redirect('survey_list')
    elif user.role == 'internal User':
        return redirect('assigned_tasks')

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def create_survey(request):
    if request.user.role != 'admin':
        return redirect('survey_list')

    if request.method == 'POST':
        form = SurveyForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('survey_list')
    else:
        form = SurveyForm()
    return render(request, 'create_survey.html', {'form': form})

@login_required
def survey_list(request):
    surveys = Survey.objects.all()
    return render(request, 'survey_list.html', {'surveys': surveys})

@login_required
def assigned_tasks(request):
    if request.user.role != 'internal User':
        return redirect('assigned_tasks')

    surveys = Survey.objects.filter(owner=request.user)
    return render(request, 'assigned_tasks.html', {'surveys': surveys})





@login_required


def change_status(request, survey_id):
    if request.method == 'POST':
        survey = get_object_or_404(Survey, pk=survey_id)
        
        # Check if the user is a manager
        if request.user.role == 'manager':
            new_status = request.POST.get('status')
            if new_status in ['Pending', 'Ongoing', 'Completed']:
                survey.status = new_status
                survey.save()
                Log.objects.create(survey=survey, description=f"Status changed to {new_status} by {request.user.username}")
                
                return JsonResponse({'status': new_status})  # Return JSON response with updated status
            else:
                return JsonResponse({'error': 'Invalid status'}, status=400)
        else:
            return JsonResponse({'error': 'Permission denied'}, status=403)
'''return JsonResponse({'status': new_status})  # Return JSON response with updated status
            else:
                return JsonResponse({'error': 'Invalid status'}, status=400)
        else:
            return JsonResponse({'error': 'Permission denied'}, status=403)'''