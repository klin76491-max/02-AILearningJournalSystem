from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .models import AISummaryReport
from .services import ReportService

class ReportListView(LoginRequiredMixin, ListView):
    model = AISummaryReport
    template_name = 'reports/report_list.html'
    context_object_name = 'reports'
    paginate_by = 10

    def get_queryset(self):
        return AISummaryReport.objects.filter(user=self.request.user).order_by('-end_date')

class ReportDetailView(LoginRequiredMixin, DetailView):
    model = AISummaryReport
    template_name = 'reports/report_detail.html'
    context_object_name = 'report'

    def get_queryset(self):
        return AISummaryReport.objects.filter(user=self.request.user)

class GenerateWeeklyReportView(LoginRequiredMixin, View):
    def post(self, request):
        report = ReportService.generate_weekly_report(request.user)
        messages.success(request, f"成功生成 {report.title}！")
        return redirect('reports:detail', pk=report.pk)
