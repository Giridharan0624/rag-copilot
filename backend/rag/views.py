"""
Module 8 — Django API view for RAG queries.
"""

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import QueryRequestSerializer
from .pipeline import run_pipeline


class QueryView(APIView):
    """
    POST /api/query/
    Requires JWT authentication.
    Accepts: { "query": "..." }
    Returns: { "answer": "...", "sources": [...], "confidence": 0.85, "validated": true }
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
