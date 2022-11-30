from django import forms

from .models import Frase, Idioma

class FraseForm(forms.ModelForm):
    idioma = forms.ModelChoiceField(
        queryset=Idioma.objects.order_by('nombre')
    )
    class Meta:
        model=Frase
        fields = ['idioma','autor', 'frase']
        labels = {
            'idioma':"Idioma", 
            "autor":"Autor",
            "frase": "Frase"
        }
        widget={'frase': forms.TextInput}

    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class':'form-control'
            })