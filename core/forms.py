from django import forms
from .models import Item, Message


class ItemForm(forms.ModelForm):
    images = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'multiple': True}),
        required=False,
        help_text='You can upload up to 3 images (Max 5MB each)'
    )
    image = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'multiple': False}),
        required=True,
    )

    class Meta:
        model = Item
        fields = [
            'title', 'description', 'status', 'category', 'location', 'image',
            'date_lost_found', 'time_lost_found', 'contact_info'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'e.g., Blue Backpack, iPhone 13, Student ID Card'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
                'rows': 4,
                'placeholder': 'Provide details about the item...'
            }),
            'status': forms.RadioSelect(attrs={
                'class': 'h-4 w-4 text-blue-600 focus:ring-blue-500'
            }),
            'category': forms.Select(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500'
            }),
            'location': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500'
            }),
            'date_lost_found': forms.DateInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
                'type': 'date'
            }),
            'time_lost_found': forms.TimeInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
                'type': 'time'
            }),
            'contact_info': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'How should people contact you? (Email or phone)'
            }),
        }

    def clean_images(self):
        images = self.files.getlist('images')
        if len(images) > 3:
            raise forms.ValidationError("You can upload a maximum of 3 images.")
        
        for image in images:
            if image.size > 5 * 1024 * 1024:  # 5MB
                raise forms.ValidationError("Each image must be less than 5MB.")
        
        return images

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
                'rows': 3,
                'placeholder': 'Type your message here...'
            }),
        }