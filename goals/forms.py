from django import forms
from .models import GoalProject

class GoalProjectForm(forms.ModelForm):
    class Meta:
        model = GoalProject
        fields = ('title', 'why_statement', 'timeframe', 'status', 'inventory_item')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '目標名稱，例如：完成 Web 系統 MVP'}),
            'why_statement': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': '清楚說明初衷：為什麼這件事值得你投入時間？'}),
            'timeframe': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'inventory_item': forms.Select(attrs={'class': 'form-select'}),
        }
