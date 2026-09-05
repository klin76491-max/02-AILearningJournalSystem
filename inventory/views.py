import json
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .models import MentalInventoryItem
from .forms import BulkInventoryForm, MentalInventoryItemForm
from .services import MentalInventoryService


class InventoryWizardStep1View(LoginRequiredMixin, View):
    def get(self, request):
        form = BulkInventoryForm()
        return render(request, 'inventory/wizard_step1.html', {'form': form})

    def post(self, request):
        form = BulkInventoryForm(request.POST)
        if form.is_valid():
            count = MentalInventoryService.save_bulk_inventory(
                user=request.user,
                doing_text=form.cleaned_data['doing_text'],
                should_text=form.cleaned_data['should_text'],
                want_text=form.cleaned_data['want_text']
            )
            messages.success(request, f"成功寫下 {count} 個盤點項目！現在進入步驟 2 進行篩選測試。")
            return redirect('inventory:wizard_step2')
        return render(request, 'inventory/wizard_step1.html', {'form': form})


class InventoryWizardStep2View(LoginRequiredMixin, View):
    def get(self, request):
        summary = MentalInventoryService.get_inventory_summary(request.user)
        return render(request, 'inventory/wizard_step2.html', {'summary': summary})


class InventoryWizardStep3View(LoginRequiredMixin, View):
    def get(self, request):
        summary = MentalInventoryService.get_inventory_summary(request.user)
        return render(request, 'inventory/wizard_step3.html', {'summary': summary})

    def post(self, request):
        messages.success(request, "🎉 恭喜完成人生思想盤點！已解鎖今日子彈工作區，隨時可返回此處調整。")
        return redirect('journal:today')


class InventoryListView(LoginRequiredMixin, View):
    def get(self, request):
        summary = MentalInventoryService.get_inventory_summary(request.user)
        form = MentalInventoryItemForm()
        return render(request, 'inventory/list.html', {'summary': summary, 'form': form})

    def post(self, request):
        form = MentalInventoryItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.user = request.user
            item.save()
            messages.success(request, f"成功新增項目：{item.content}")
            return redirect('inventory:list')
        summary = MentalInventoryService.get_inventory_summary(request.user)
        return render(request, 'inventory/list.html', {'summary': summary, 'form': form})


class InventoryAPISiftView(LoginRequiredMixin, View):
    def post(self, request, item_id):
        try:
            data = json.loads(request.body.decode('utf-8'))
        except Exception:
            data = request.POST

        test_status = data.get('test_status', 'kept')
        category = data.get('category', 'none')

        success = MentalInventoryService.sift_item(request.user, item_id, test_status, category)
        if success:
            return JsonResponse({'success': True, 'item_id': item_id, 'test_status': test_status})
        return JsonResponse({'success': False, 'error': '操作失敗或項目不存在。'}, status=404)


class InventoryAPIToggleFocusView(LoginRequiredMixin, View):
    def post(self, request, item_id):
        success = MentalInventoryService.toggle_focus(request.user, item_id)
        if success:
            item = MentalInventoryItem.objects.get(id=item_id)
            return JsonResponse({'success': True, 'item_id': item_id, 'is_focus': item.is_focus})
        return JsonResponse({'success': False, 'error': '操作失敗。'}, status=404)


class InventoryAPIDeleteView(LoginRequiredMixin, View):
    def post(self, request, item_id):
        try:
            item = MentalInventoryItem.objects.get(id=item_id, user=request.user)
            item.delete()
            return JsonResponse({'success': True, 'item_id': item_id})
        except MentalInventoryItem.DoesNotExist:
            return JsonResponse({'success': False, 'error': '項目不存在。'}, status=404)
