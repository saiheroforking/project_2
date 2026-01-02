from rest_framework import serializers
from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    # Extra control if you want to customize individual fields
    priority = serializers.ChoiceField(
        choices=["low", "medium", "high"],
        default="low"
    )

    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "description",
            "done",
            "priority",
            "created",
        ]
        read_only_fields = ["id", "created"]

    # ---------------------------
    # FIELD-LEVEL VALIDATION
    # ---------------------------
    def validate_title(self, value):
        value = value.strip()

        if len(value) < 3:
            raise serializers.ValidationError(
                "Title must be at least 3 characters."
            )

        return value

    # ---------------------------
    # OBJECT-LEVEL VALIDATION
    # ---------------------------
    def validate(self, attrs):
        """
        Rules:

        - high priority requires description
        - cannot mark task done without description
        """

        priority = attrs.get("priority", getattr(self.instance, "priority", "low"))
        done = attrs.get("done", getattr(self.instance, "done", False))
        description = attrs.get(
            "description",
            getattr(self.instance, "description", "")
        )

        # high priority must explain WHY
        if priority == "high" and not description:
            raise serializers.ValidationError(
                {"description": "High priority tasks must include a description."}
            )

        # done must not be empty task
        if done and not description:
            raise serializers.ValidationError(
                {"description": "Completed tasks must include a description."}
            )

        return attrs

    # ---------------------------
    # CREATE
    # ---------------------------
    def create(self, validated_data):
        # normalize title consistently
        validated_data["title"] = validated_data["title"].strip().title()
        return Task.objects.create(**validated_data)

    # ---------------------------
    # UPDATE
    # ---------------------------
    def update(self, instance, validated_data):
        title = validated_data.get("title")
        if title:
            validated_data["title"] = title.strip().title()

        return super().update(instance, validated_data)
