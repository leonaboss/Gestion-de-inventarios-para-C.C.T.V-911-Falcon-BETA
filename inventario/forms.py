import re
from django import forms
from django.core.exceptions import ValidationError
from .models import Producto


class ProductoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Todos los campos son obligatorios
        for field in self.fields.values():
            field.required = True
            field.error_messages['required'] = 'por favor, rellena todos los campos'

    class Meta:
        model = Producto
        fields = [
            'cantidad',
            'codigo',
            'num_de_bien',
            'descripcion',
            'cod_bien',
            'concepto',
            'valor_unitario',
        ]
        widgets = {
            'cantidad': forms.NumberInput(attrs={'class': 'form-control'}),
            'codigo': forms.TextInput(attrs={'class': 'form-control'}),
            'num_de_bien': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'cod_bien': forms.TextInput(attrs={'class': 'form-control'}),
            'concepto': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'valor_unitario': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }

    # --- Métodos de validación genéricos ---

    def _validate_text(self, text_data, field_name):
        if not text_data:
            return text_data # La validación de campo requerido se maneja en otro lugar

        # Regla 1: Expresión regular para validar caracteres permitidos.
        pattern = re.compile(r'^[a-zA-Z0-9\s\.,\-áéíóúÁÉÍÓÚñÑ]+$')
        if not pattern.match(text_data):
            raise ValidationError('Contenido no válido: Contiene caracteres no permitidos.')

        # Regla 2: Longitud mínima.
        if len(text_data.strip(' .,-_')) < 3:
            raise ValidationError('Contenido no válido (demasiado corto).')

        # Regla 3: Repetición excesiva de caracteres.
        if re.search(r'(.)\1{3,}', text_data):
            raise ValidationError('Contenido no válido (parece texto sin sentido).')

        return text_data

    def _validate_code(self, text_data, field_name):
        if not text_data:
            return text_data # La validación de campo requerido se maneja en otro lugar

        # Regla 1: Expresión regular para validar caracteres permitidos.
        pattern = re.compile(r'^[a-zA-Z0-9\s\.,\-áéíóúÁÉÍÓÚñÑ]+$')
        if not pattern.match(text_data):
            raise ValidationError(f'Contenido no válido para {field_name}: Contiene caracteres no permitidos.')

        # Regla 2: Longitud (>= 2).
        length = len(text_data.strip(' .,-_'))
        if length < 2:
            raise ValidationError(f'Contenido no válido: Debe tener 2 o más caracteres.')

        # Regla 3: Repetición excesiva de caracteres.
        if re.search(r'(.)\1{3,}', text_data):
            raise ValidationError(f'Contenido no válido para {field_name} (parece texto sin sentido).')

        return text_data

    # --- Limpieza de campos específicos ---

    def clean_descripcion(self):
        return self._validate_text(self.cleaned_data.get('descripcion'), 'Descripción')

    def clean_concepto(self):
        return self._validate_text(self.cleaned_data.get('concepto'), 'Concepto')

    def clean_codigo(self):
        return self._validate_code(self.cleaned_data.get('codigo'), 'Código')

    def clean_num_de_bien(self):
        return self._validate_code(self.cleaned_data.get('num_de_bien'), 'Número de Bien')

    def clean_cod_bien(self):
        return self._validate_code(self.cleaned_data.get('cod_bien'), 'Código del Bien')
