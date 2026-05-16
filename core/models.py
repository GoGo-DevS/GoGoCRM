from django.db import models
from django.utils import timezone


class Cliente(models.Model):
    nombre = models.CharField(max_length=200)
    empresa = models.CharField(max_length=200, blank=True)
    email = models.EmailField(blank=True)
    telefono = models.CharField(max_length=30, blank=True)
    instagram = models.CharField(max_length=100, blank=True)
    notas = models.TextField(blank=True)
    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-creado']
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'

    def __str__(self):
        return f"{self.nombre} — {self.empresa}" if self.empresa else self.nombre

    @property
    def proyectos_activos(self):
        return self.proyectos.exclude(estado='entregado').count()


class Proyecto(models.Model):
    ESTADO_CHOICES = [
        ('prospecto',  'Prospecto'),
        ('negociacion','Negociación'),
        ('activo',     'Activo'),
        ('revision',   'En revisión'),
        ('entregado',  'Entregado'),
        ('pausado',    'Pausado'),
    ]
    TIPO_CHOICES = [
        ('web_base',       'Web base / Landing'),
        ('web_profesional','Web profesional'),
        ('sistema',        'Sistema / Automatización'),
        ('branding',       'Branding'),
        ('seo',            'SEO'),
        ('otro',           'Otro'),
    ]

    cliente        = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='proyectos')
    nombre         = models.CharField(max_length=200)
    tipo           = models.CharField(max_length=30, choices=TIPO_CHOICES, default='web_profesional')
    estado         = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='prospecto')
    descripcion    = models.TextField(blank=True)
    dominio        = models.CharField(max_length=100, blank=True)
    stack          = models.CharField(max_length=200, blank=True, help_text='Ej: Django · Bootstrap 5 · Render')
    monto_total    = models.DecimalField(max_digits=12, decimal_places=0, default=0)
    fecha_inicio   = models.DateField(null=True, blank=True)
    fecha_entrega  = models.DateField(null=True, blank=True)
    notas          = models.TextField(blank=True)
    creado         = models.DateTimeField(auto_now_add=True)
    actualizado    = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-creado']
        verbose_name = 'Proyecto'
        verbose_name_plural = 'Proyectos'

    def __str__(self):
        return f"{self.nombre} ({self.cliente.nombre})"

    @property
    def total_pagado(self):
        return sum(p.monto for p in self.pagos.filter(pagado=True))

    @property
    def saldo_pendiente(self):
        return self.monto_total - self.total_pagado

    @property
    def porcentaje_cobrado(self):
        if self.monto_total == 0:
            return 0
        return int((self.total_pagado / self.monto_total) * 100)

    @property
    def tareas_completadas(self):
        return self.tareas.filter(estado='hecho').count()

    @property
    def tareas_total(self):
        return self.tareas.count()

    @property
    def progreso(self):
        if self.tareas_total == 0:
            return 0
        return int((self.tareas_completadas / self.tareas_total) * 100)


class Tarea(models.Model):
    ESTADO_CHOICES = [
        ('backlog',     'Backlog'),
        ('por_hacer',   'Por hacer'),
        ('en_progreso', 'En progreso'),
        ('revision',    'En revisión'),
        ('hecho',       'Hecho'),
    ]
    PRIORIDAD_CHOICES = [
        ('baja',   'Baja'),
        ('media',  'Media'),
        ('alta',   'Alta'),
        ('critica','Crítica'),
    ]

    proyecto   = models.ForeignKey(Proyecto, on_delete=models.CASCADE, related_name='tareas')
    titulo     = models.CharField(max_length=300)
    descripcion= models.TextField(blank=True)
    estado     = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='por_hacer')
    prioridad  = models.CharField(max_length=10, choices=PRIORIDAD_CHOICES, default='media')
    orden      = models.PositiveIntegerField(default=0)
    creado     = models.DateTimeField(auto_now_add=True)
    actualizado= models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['orden', '-prioridad', 'creado']
        verbose_name = 'Tarea'
        verbose_name_plural = 'Tareas'

    def __str__(self):
        return self.titulo


class Pago(models.Model):
    TIPO_CHOICES = [
        ('adelanto',  'Adelanto 50%'),
        ('entrega',   'Contra entrega 50%'),
        ('parcial',   'Pago parcial'),
        ('total',     'Pago total'),
        ('mensual',   'Mensualidad'),
    ]
    METODO_CHOICES = [
        ('transferencia', 'Transferencia'),
        ('efectivo',      'Efectivo'),
        ('webpay',        'Webpay'),
        ('otro',          'Otro'),
    ]

    proyecto  = models.ForeignKey(Proyecto, on_delete=models.CASCADE, related_name='pagos')
    tipo      = models.CharField(max_length=20, choices=TIPO_CHOICES)
    monto     = models.DecimalField(max_digits=12, decimal_places=0)
    metodo    = models.CharField(max_length=20, choices=METODO_CHOICES, default='transferencia')
    pagado    = models.BooleanField(default=False)
    fecha_esperada = models.DateField(null=True, blank=True)
    fecha_recibido = models.DateField(null=True, blank=True)
    notas     = models.TextField(blank=True)
    creado    = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['fecha_esperada']
        verbose_name = 'Pago'
        verbose_name_plural = 'Pagos'

    def __str__(self):
        return f"{self.proyecto.nombre} — ${self.monto:,.0f} ({self.get_tipo_display()})"


class Soporte(models.Model):
    TIPO_CHOICES = [
        ('bug',          'Bug / Error'),
        ('consulta',     'Consulta'),
        ('capacitacion', 'Capacitación'),
        ('cambio',       'Cambio de alcance'),
        ('mantencion',   'Mantención'),
    ]
    ESTADO_CHOICES = [
        ('abierto',    'Abierto'),
        ('en_proceso', 'En proceso'),
        ('resuelto',   'Resuelto'),
    ]
    PRIORIDAD_CHOICES = [
        ('baja',  'Baja'),
        ('media', 'Media'),
        ('alta',  'Alta'),
    ]

    proyecto  = models.ForeignKey(Proyecto, on_delete=models.CASCADE, related_name='soportes')
    tipo      = models.CharField(max_length=20, choices=TIPO_CHOICES)
    titulo    = models.CharField(max_length=300)
    descripcion = models.TextField(blank=True)
    estado    = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='abierto')
    prioridad = models.CharField(max_length=10, choices=PRIORIDAD_CHOICES, default='media')
    resolucion= models.TextField(blank=True)
    creado    = models.DateTimeField(auto_now_add=True)
    resuelto_en = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-creado']
        verbose_name = 'Ticket de soporte'
        verbose_name_plural = 'Tickets de soporte'

    def __str__(self):
        return f"[{self.get_tipo_display()}] {self.titulo}"
