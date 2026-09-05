from django.urls import path
from . import views

app_name = 'inventory'

urlpatterns = [
    path('wizard/step1/', views.InventoryWizardStep1View.as_view(), name='wizard_step1'),
    path('wizard/step2/', views.InventoryWizardStep2View.as_view(), name='wizard_step2'),
    path('wizard/step3/', views.InventoryWizardStep3View.as_view(), name='wizard_step3'),
    path('', views.InventoryListView.as_view(), name='list'),
    path('api/<int:item_id>/sift/', views.InventoryAPISiftView.as_view(), name='api_sift'),
    path('api/<int:item_id>/toggle-focus/', views.InventoryAPIToggleFocusView.as_view(), name='api_toggle_focus'),
    path('api/<int:item_id>/delete/', views.InventoryAPIDeleteView.as_view(), name='api_delete'),
]
