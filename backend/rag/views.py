"""
Module 8 — Django API views for RAG queries.
"""

import json
import os

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.conf import settings

from .serializers import QueryRequestSerializer
from .pipeline import run_pipeline


class QueryView(APIView):
    """
    POST /api/query/
    Requires JWT authentication.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = QueryRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        query = serializer.validated_data["query"]

        try:
            result = run_pipeline(query)
            return Response(result)
        except ValueError as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )
        except Exception as e:
            return Response(
                {"error": f"An unexpected error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class QuestionsListView(APIView):
    """
    GET /api/questions/
    Returns all FAQ questions from docs.json.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        docs_path = os.path.join(settings.DATA_DIR, "docs.json")
        try:
            with open(docs_path, "r", encoding="utf-8") as f:
                docs = json.load(f)
            questions = [d["question"] for d in docs]
            return Response({"questions": questions})
        except FileNotFoundError:
            return Response(
                {"error": "FAQ dataset not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
