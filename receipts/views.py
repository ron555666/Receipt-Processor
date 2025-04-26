from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ReceiptSerializer
from .storage import store_points, get_points
import math
from datetime import datetime, time
import uuid


class ProcessReceiptView(APIView):
    def post(self, request):
        serializer = ReceiptSerializer(data=request.data)
        if serializer.is_valid():
            receipt_data = serializer.validated_data
            points = self._calculate_points(receipt_data)
            receipt_id = str(uuid.uuid4())
            store_points(receipt_id, points)
            return Response({"id": receipt_id}, status=status.HTTP_200_OK)
        return Response(
            {"error": "Invalid receipt data", "details": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )

    def _calculate_points(self, receipt):
        points = 0

        # Points from retailer name
        points += sum(1 for char in receipt["retailer"] if char.isalnum())

        total_amount = float(receipt["total"])

        # Points if total is a round dollar
        if total_amount == int(total_amount):
            points += 50

        # Points if total is multiple of 0.25
        if total_amount % 0.25 == 0:
            points += 25

        # Points from number of items
        points += (len(receipt["items"]) // 2) * 5

        # Points from item description
        for item in receipt["items"]:
            description = item["shortDescription"].strip()
            if len(description) % 3 == 0:
                points += math.ceil(float(item["price"]) * 0.2)

        # Points if purchase day is odd
        try:
            day = receipt["purchaseDate"].day
            if day % 2 == 1:
                points += 6
        except Exception:
            pass

        # Points if purchase time is between 14:00 and 16:00
        try:
            purchase_time = receipt["purchaseTime"]
            if time(14, 0) <= purchase_time < time(16, 0):
                points += 10
        except Exception:
            pass

        # Debug prints
        print("Retailer:", receipt["retailer"])
        print("Alphanumeric characters:", sum(1 for char in receipt["retailer"] if char.isalnum()))
        print("Total amount:", total_amount)
        print("Number of items:", len(receipt["items"]))
        print("Purchase day:", receipt["purchaseDate"].day)

        return points


class GetPointsView(APIView):
    def get(self, request, receipt_id):
        points = get_points(receipt_id)
        if points is None:
            return Response({"error": "No receipt found for that ID."}, status=404)
        return Response({"points": points})
