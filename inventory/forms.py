from django import forms
from .models import MentalInventoryItem


class MentalInventoryItemForm(forms.ModelForm):
    class Meta:
        model = MentalInventoryItem
        fields = ('inventory_type', 'content', 'category', 'is_focus')
        widgets = {
            'inventory_type': forms.Select(attrs={'class': 'form-select'}),
            'content': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '寫下這件事...'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'is_focus': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class BulkInventoryForm(forms.Form):
    doing_text = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 5,
            'placeholder': '每行一件事情，例如：\n每天寫程式\n整理專案文件\n回覆客戶郵件'
        }),
        label='1. 我正在做的事 (What I am doing)'
    )
    should_text = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 5,
            'placeholder': '每行一件事情，例如：\n應該去跑步運動\n應該整理書櫃\n應該聯絡很久沒見的朋友'
        }),
        label='2. 我應該做的事 (What I should be doing)'
    )
    want_text = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 5,
            'placeholder': '每行一件事情，例如：\n想做出一個屬於自己的 Web 系統\n想去沒有去過的街道探索\n想讀完《子彈思考整理術》'
        }),
        label='3. 我想做的事 (What I want to be doing)'
    )
