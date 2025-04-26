from rest_framework import serializers
import re

class ItemSerializer(serializers.Serializer):
    shortDescription = serializers.CharField()
    price = serializers.CharField()

    def validate_shortDescription(self, value):
        if not re.match(r"^[\w\s\-]+$", value.strip()):
            raise serializers.ValidationError(
                "Short description can only have letters, numbers, spaces, and hyphens (-)."
            )
        return value.strip()

    def validate_price(self, value):
        if not re.match(r"^\d+\.\d{2}$", value):
            raise serializers.ValidationError(
                "Price must look like 12.00 or 5.99."
            )
        return value


class ReceiptSerializer(serializers.Serializer):
    retailer = serializers.CharField()
    purchaseDate = serializers.DateField()
    purchaseTime = serializers.TimeField()
    total = serializers.CharField()
    items = ItemSerializer(many=True)

    def validate_retailer(self, value):
        if not re.match(r"^[\w\s\-\&]+$", value.strip()):
            raise serializers.ValidationError(
                "Retailer name can only have letters, numbers, spaces, hyphens (-), and ampersands (&)."
            )
        return value.strip()

    def validate_total(self, value):
        if not re.match(r"^\d+\.\d{2}$", value):
            raise serializers.ValidationError(
                "Total must be like 35.35 or 100.00."
            )
        return value
