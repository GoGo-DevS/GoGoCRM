from django import forms
from .models import Cliente, Proyecto, Tarea, Pago, Soporte


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'empresa', 'email', 'telefono', 'instagram', 'notas']
        widgets = {
            'nombre':    forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre completo'}),
            'empresa':   forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Empresa o negocio'}),
            'email':     forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'correo@ejemplo.cl'}),
            'telefono':  forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+56 9 XXXX XXXX'}),
            'instagram': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '@usuario'}),
            'notas':     forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Notas del cliente...'}),
        }


class ProyectoForm(forms.ModelForm):
    class Meta:
        model = Proyecto
        fields = ['cliente', 'nombre', 'tipo', 'estado', 'descripcion',
                  'dominio', 'stack', 'monto_total', 'fecha_inicio', 'fecha_entrega', 'notas']
        widgets = {
            'cliente':       forms.Select(attrs={'class': 'form-select'}),
            'nombre':        forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del proyecto'}),
            'tipo':          forms.Select(attrs={'class': 'form-select'}),
            'estado':        forms.Select(attrs={'class': 'form-select'}),
            'descripcion':   forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'dominio':       forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ejemplo.cl'}),
            'stack':         forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Django · Bootstrap 5 · Render'}),
            'monto_total':   forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '200000'}),
            'fecha_inicio':  forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'fecha_entrega': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'notas':         forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class TareaForm(forms.ModelForm):
    class Meta:
        model = Tarea
        fields = ['proyecto', 'titulo', 'descripcion', 'estado', 'prioridad']
        widgets = {
            'proyecto':    forms.HiddenInput(),
            'titulo':      forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Título de la tarea'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'estado':      forms.Select(attrs={'class': 'form-select'}),
            'prioridad':   forms.Select(attrs={'class': 'form-select'}),
        }


class PagoForm(forms.ModelForm):
    class Meta:
        model = Pago
        fields = ['tipo', 'monto', 'metodo', 'pagado', 'fecha_esperada', 'fecha_recibido', 'notas']
        widgets = {
            'tipo':           forms.Select(attrs={'class': 'form-select'}),
            'monto':          forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '100000'}),
            'metodo':         forms.Select(attrs={'class': 'form-select'}),
            'pagado':         forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'fecha_esperada': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'fecha_recibido': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'notas':          forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }


class SoporteForm(forms.ModelForm):
    class Meta:
        model = Soporte
        fields = ['tipo', 'titulo', 'descripcion', 'prioridad']
        widgets = {
            'tipo':        forms.Select(attrs={'class': 'form-select'}),
            'titulo':      forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Describe el problema o consulta'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'prioridad':   forms.Select(attrs={'class': 'form-select'}),
        }
