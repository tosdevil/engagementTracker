from .models import Video
from django.forms import ModelForm, FileInput


class ImageForm(ModelForm):
	class Meta:
		model = Video
		fields = ['video_path']

		widgets = {
			"img": FileInput(attrs={
				'class':'video_upload',
				'id':'video_upload',
				'placeholder':'Put your image...'
			})
		}