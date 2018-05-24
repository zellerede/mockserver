# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.mixins import (
   CreateModelMixin, RetrieveModelMixin, 
   UpdateModelMixin, DestroyModelMixin,
   ListModelMixin
)
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework.decorators import list_route
from url_filter.integrations.drf import DjangoFilterBackend
from django.db.transaction import atomic

from models import MockAnswer
from serializers import MockAnswerSerializer

class ListViewSet(
      ListModelMixin,
      CreateModelMixin,
      RetrieveModelMixin,
      UpdateModelMixin,
      DestroyModelMixin,
      GenericViewSet):

    @list_route(methods=['delete', 'patch', 'post'])
    def bulk(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        if request.method == "DELETE":
            queryset.delete()
            return Response()
        if request.method == "PATCH":
            queryset.update(**request.data)
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        if request.method == "POST":
            ids = []
            with atomic():
                for item in request.data:
                    entry = queryset.create(**item)
                    ids.append(entry.pk)
            return Response(ids, status=201)

class MockAnswersView(ListViewSet):
    queryset = MockAnswer.objects.all()
    serializer_class = MockAnswerSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ("url", "req_method")

###

@api_view(["DELETE", "GET", "PATCH", "POST", "PUT"])
def mocking(request, path):
    mockAnswers = MockAnswer.objects
    answer = mockAnswers.filter(
        url=path,
        req_method=request.method
    ).order_by("id")
    if answer:
        return mock_for(request, answer[0])
    return default_response(request, path)

def mock_for(request, answer):
    answerBody = json.loads( answer.ans_body ) if answer.ans_body else None
    answer.req_body = json.dumps(request.data)
    answer.query_params = json.dumps(request.query_params)
    if answer.use_up:
        answer.use_up -= 1
    if answer.use_up is 0: 
        answer.delete()
    else:
        answer.save()
    return Response(answerBody, answer.ans_status)

def default_response(request, path):
    return Response({
        "query_params": request.query_params,
        "method": request.method,
        "data": request.data, 
        "path": path,
    }, status=404)


# -todo:
#
# variables in URL's to mock
#
# https!!!  -- with external nginx
#
# rather save a History??
# 
# credentials in headers??  -- might not be needed
#
 

