from django import forms
from .models import Product, ProductPhotos, BlogPost, PostResource, GaleryModel, About
from tinymce.widgets import TinyMCE

# add product form


class ProductForm(forms.ModelForm):
    old_price = forms.IntegerField(required=False,widget=forms.NumberInput(attrs={'class': 'form-control', 'id': 'inputOldPrice'}),label='Old Price (optional)')
    description = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))

    class Meta:
        model = Product
        fields = ('name','price','old_price','category','info','description')

        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control', 'id':'inputName'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'id': 'inputPrice'}),
            'category': forms.Select(attrs={'class': 'form-control', 'id': 'inputCat'}),
            'info': forms.Textarea(attrs={'class': 'form-control', 'id': 'inputInfo', 'rows':3}),
            # 'description': forms.Textarea(attrs={'class': 'form-control', 'id': 'inputDesc'}),
        }

        error_messages = {
            'name': {
                'required': 'this field is required.',
            },
            'price': {
                'required': 'this field is required.',
            },
            'category': {
                'required': 'this field is required.',
            },
            'info': {
                'required': 'this field is required.',
            },
            'description': {
                'required': 'this field is required.',
            }
        }
        

class ProductPhotosForm(forms.ModelForm):
    photo2 = forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs={'class': 'form-control'}))
    photo3 = forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs={'class': 'form-control'}))
    photo4 = forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs={'class': 'form-control'}))
    photo5 = forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs={'class': 'form-control'}))

    class Meta:
        model = ProductPhotos
        fields = ('photo1','photo2','photo3','photo4','photo5','photo6')

        widgets = {
            'photo1': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'photo6': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

        labels = {
            'photo1': "photo1 *",
            'photo6': 'photo6 *'
        }

        error_messages = {
            'photo1': {
                'required': 'this field is required.',
            },
        }


class PostResForm(forms.ModelForm):
    res_info = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))
    class Meta:
        model = PostResource
        fields = ('res_name','res_img','res_info')

        labels = {
            'res_name': 'Resource Name',
            'res_img': 'Resource Image',
            'res_info': 'Resource Information',
        }

        widgets = {
            'res_name': forms.TextInput(attrs={'class': 'form-control', 'id': 'resName','required':'false'}),
            'res_img': forms.ClearableFileInput(attrs={'class': 'form-control', 'id': 'resImg','required':'false'}),
            # 'res_info': forms.Textarea(attrs={'class': 'form-control', 'id': 'resInfo', 'rows': 3,'required':'false'}),
        }


class AddPostForm(forms.ModelForm):
    post_desc = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))
    class Meta:
        model = BlogPost
        fields = ('post_res','post_author','post_sub','post_img','post_desc')
        labels = {
            'post_res': 'Post Resource',
            'post_author': 'Post Author',
            'post_sub': 'Post Subject',
            'post_img': 'Post Image',
            'post_desc': 'Post Description',
        }

        widgets = {
            'post_res' : forms.Select(attrs={'class': 'form-control', 'id': 'postAuth'}),
            'post_author': forms.TextInput(attrs={'class': 'form-control', 'id': 'postAuth'}),
            'post_sub': forms.TextInput(attrs={'class': 'form-control', 'id': 'postSub'}),
            'post_img': forms.ClearableFileInput(attrs={'class': 'form-control', 'id': 'postImg'}),
            'post_desc': forms.Textarea(attrs={'class': 'form-control', 'id': 'postDesc', 'rows': 3}),
        }


class GalleryForm(forms.ModelForm):
    title = forms.CharField(required=False,widget=forms.TextInput(attrs={'class':'form-control'}),label='Image Title (optional)')

    class Meta:
        model = GaleryModel
        fields = '__all__'

        labels = {
            'image': 'Image',
        }

        widgets = {
            'image': forms.ClearableFileInput(attrs={'class':'form-control'}),
        }


class AboutForm(forms.ModelForm):
    info = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))
    story = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))
    class Meta:
        model = About
        fields = '__all__'

        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control'}),
            'picture': forms.ClearableFileInput(attrs={'class':'form-control'}),
            # 'info': forms.Textarea(attrs={'class':'form-control','rows':'4'}),
            # 'story': forms.Textarea(attrs={'class':'form-control'}),
        }

        labels = {
            'name':'Restaurant Name*',
            'picture':'Restaurant Photo*',
            'info':'Restaurant Information*',
            'story':'Restaurant Story*',
        }