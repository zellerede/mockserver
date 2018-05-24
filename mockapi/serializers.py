from rest_framework.serializers import ModelSerializer

from models import MockAnswer

class MockAnswerSerializer(ModelSerializer):
    class Meta:
        model = MockAnswer
        fields = ("id", "url", "req_method", "use_up", "query_params", "req_body", "ans_status", "ans_body")

