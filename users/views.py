from django.shortcuts import render
from django_filters import rest_framework as filters
from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListAPIView

from online_education.serializers import CourseSerializer
from models import Payment
# Create your views here.


class PaymentListAPIView(ListAPIView):
    serializer_class = CourseSerializer
    queryset = Payment.objects.all()
    filter_backends = (filters.DjangoFilterBackend, OrderingFilter)
    filterset_fields = ('paid_course', 'paid_lesson', 'payment_method')
    ordering_fields = ('date',)
