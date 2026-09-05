from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .models import GoalProject
from .forms import GoalProjectForm
from inventory.models import MentalInventoryItem

class GoalListView(LoginRequiredMixin, View):
    def get(self, request):
        goals = GoalProject.objects.filter(user=request.user)
        focus_inventory = MentalInventoryItem.objects.filter(user=request.user, is_focus=True)
        form = GoalProjectForm()
        form.fields['inventory_item'].queryset = MentalInventoryItem.objects.filter(user=request.user, test_status='kept')

        return render(request, 'goals/goal_list.html', {
            'goals': goals,
            'focus_inventory': focus_inventory,
            'form': form
        })

    def post(self, request):
        form = GoalProjectForm(request.POST)
        if form.is_valid():
            goal = form.save(commit=False)
            goal.user = request.user
            goal.save()
            messages.success(request, f"成功建立焦點目標：{goal.title}！")
            return redirect('goals:list')

        goals = GoalProject.objects.filter(user=request.user)
        focus_inventory = MentalInventoryItem.objects.filter(user=request.user, is_focus=True)
        return render(request, 'goals/goal_list.html', {
            'goals': goals,
            'focus_inventory': focus_inventory,
            'form': form
        })
