from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Task
from .serializer import TaskSerializer


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all().order_by("-created")
    serializer_class = TaskSerializer

    # Example custom action: mark complete
    @action(detail=True, methods=["post"])
    def mark_complete(self, request, pk=None):
        task = self.get_object()
        task.done = True
        task.save()
        serializer = self.get_serializer(task)
        return Response(serializer.data)
