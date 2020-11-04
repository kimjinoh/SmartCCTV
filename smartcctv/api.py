from .models import cctv
from .models import people
from .models import detect
from .models import heatmap
from rest_framework import serializers, viewsets
from rest_framework.response import Response
from django import forms

class cctvSerializer(serializers.ModelSerializer):
    class Meta:
        model = cctv
        fields = '__all__'

class peopleSerializer(serializers.ModelSerializer):
    class Meta:
        model = people
        fields='__all__'

class detectSerializer(serializers.ModelSerializer):
	class Meta:
		model = detect
		fields = '__all__'

class heatmapSerializer(serializers.ModelSerializer):
	class Meta:
		model = heatmap
		fields = '__all__'

class cctvViewSet(viewsets.ModelViewSet):
    queryset = cctv.objects.all()
    serializer_class = cctvSerializer

class peopleViewSet(viewsets.ModelViewSet):
    queryset=people.objects.all()
    serializer_class = peopleSerializer

class detectViewSet(viewsets.ModelViewSet):
	queryset=detect.objects.all()
	serializer_class = detectSerializer

class heatmapViewSet(viewsets.ModelViewSet):
	queryset=heatmap.objects.all()
	serializer_class = heatmapSerializer

class PostForm(forms.ModelForm):
    class Meta:
        model=cctv
        fields=['user','email','password']
