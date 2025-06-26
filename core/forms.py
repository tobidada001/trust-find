from django import forms
from .models import Item, Message


class ItemForm(forms.ModelForm):
    images = forms.FileField(
        widget=forms.FileInput(),
        required=False,
        help_text='You can upload up to 3 images (Max 5MB each)'
    )
    

    class Meta:
        model = Item
        fields = [
            'title', 'description', 'status', 'category', 'location', 'image',
            'date_lost_found', 'time_lost_found', 'contact_info', 'whatsapp_contact', 
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
            'status': forms.Select(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500'
                
            }),
            'category': forms.Select(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500'
            }),
            'location': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500'
            }),
            'date_lost_found': forms.DateInput(attrs={
                'class': 'w-full px-3 py-2 my-5 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
                'type': 'date'
            }),
            'time_lost_found': forms.TimeInput(attrs={
                'class': 'w-full px-3 py-2 my-5 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
                'type': 'time'
            }),
            'contact_info': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Email/phone number for people to contact you? (Optional)'
            }),
            'whatsapp_contact': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'WhatsApp number (if you prefer WhatsApp)'
            }),
            'image' : forms.FileInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',})
      
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