# Create your views here.
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from TatarApp.models import TatarAskModel
from TatarApp.permissions import IsVK
from TatarApp.serializers import TatarAskSerializer


class TatarGenerateTestAPIView(APIView):
    permission_classes = (IsVK,)
    renderer_classes = (JSONRenderer,)
    serializer_class = TatarAskSerializer

    def get(self, request, *args, **kwargs):
        try:
            askList = []
            askList.append(TatarAskModel.objects.all())
            serializer = self.serializer_class(instance=askList, many=True)
            # return Response({'status': True}, status=status.HTTP_200_OK)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response({'status': False}, status=status.HTTP_400_BAD_REQUEST)
