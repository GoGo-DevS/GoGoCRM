from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Sum, Count, Q
from .models import Cliente, Proyecto, Tarea, Pago, Soporte
from .forms import ClienteForm, ProyectoForm, TareaForm, PagoForm, SoporteForm


# ─── DASHBOARD ────────────────────────────────────────────────────────────────
@login_required
def dashboard(request):
    proyectos_activos = Proyecto.objects.exclude(estado__in=['entregado', 'pausado'])
    total_pipeline    = Proyecto.objects.exclude(estado='entregado').aggregate(t=Sum('monto_total'))['t'] or 0
    total_cobrado     = sum(p.total_pagado for p in Proyecto.objects.all())
    por_cobrar        = sum(
        p.saldo_pendiente for p in Proyecto.objects.exclude(estado='entregado')
        if p.saldo_pendiente > 0
    )
    tareas_urgentes = Tarea.objects.filter(
        prioridad__in=['alta', 'critica'],
        estado__in=['por_hacer', 'en_progreso']
    ).select_related('proyecto')[:8]

    pagos_pendientes = Pago.objects.filter(pagado=False).select_related('proyecto')[:6]
    tickets_abiertos = Soporte.objects.filter(estado__in=['abierto', 'en_proceso']).select_related('proyecto')[:5]

    estado_counts = {
        'prospecto':   Proyecto.objects.filter(estado='prospecto').count(),
        'negociacion': Proyecto.objects.filter(estado='negociacion').count(),
        'activo':      Proyecto.objects.filter(estado='activo').count(),
        'revision':    Proyecto.objects.filter(estado='revision').count(),
        'entregado':   Proyecto.objects.filter(estado='entregado').count(),
    }

    context = {
        'proyectos_activos': proyectos_activos,
        'total_pipeline':    total_pipeline,
        'total_cobrado':     total_cobrado,
        'por_cobrar':        por_cobrar,
        'tareas_urgentes':   tareas_urgentes,
        'pagos_pendientes':  pagos_pendientes,
        'tickets_abiertos':  tickets_abiertos,
        'estado_counts':     estado_counts,
        'total_clientes':    Cliente.objects.count(),
        'total_proyectos':   Proyecto.objects.count(),
    }
    return render(request, 'core/dashboard.html', context)


# ─── CLIENTES ─────────────────────────────────────────────────────────────────
@login_required
def clientes_list(request):
    q = request.GET.get('q', '')
    clientes = Cliente.objects.annotate(num_proyectos=Count('proyectos'))
    if q:
        clientes = clientes.filter(Q(nombre__icontains=q) | Q(empresa__icontains=q))
    return render(request, 'core/clientes_list.html', {'clientes': clientes, 'q': q})


@login_required
def cliente_create(request):
    form = ClienteForm(request.POST or None)
    if form.is_valid():
        cliente = form.save()
        messages.success(request, f'Cliente "{cliente.nombre}" creado.')
        return redirect('core:cliente_detail', pk=cliente.pk)
    return render(request, 'core/cliente_form.html', {'form': form, 'titulo': 'Nuevo cliente'})


@login_required
def cliente_detail(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    proyectos = cliente.proyectos.all()
    return render(request, 'core/cliente_detail.html', {'cliente': cliente, 'proyectos': proyectos})


@login_required
def cliente_edit(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    form = ClienteForm(request.POST or None, instance=cliente)
    if form.is_valid():
        form.save()
        messages.success(request, 'Cliente actualizado.')
        return redirect('core:cliente_detail', pk=pk)
    return render(request, 'core/cliente_form.html', {'form': form, 'titulo': f'Editar — {cliente.nombre}', 'cliente': cliente})


# ─── PROYECTOS ────────────────────────────────────────────────────────────────
@login_required
def proyectos_list(request):
    estado = request.GET.get('estado', '')
    proyectos = Proyecto.objects.select_related('cliente').all()
    if estado:
        proyectos = proyectos.filter(estado=estado)
    return render(request, 'core/proyectos_list.html', {
        'proyectos': proyectos,
        'estado_filter': estado,
        'estados': Proyecto.ESTADO_CHOICES,
    })


@login_required
def proyecto_create(request):
    form = ProyectoForm(request.POST or None)
    if form.is_valid():
        proyecto = form.save()
        # Crear pagos 50/50 automáticamente
        if proyecto.monto_total > 0:
            mitad = proyecto.monto_total / 2
            Pago.objects.create(proyecto=proyecto, tipo='adelanto', monto=mitad, metodo='transferencia')
            Pago.objects.create(proyecto=proyecto, tipo='entrega', monto=mitad, metodo='transferencia')
        messages.success(request, f'Proyecto "{proyecto.nombre}" creado con pagos 50/50 generados.')
        return redirect('core:proyecto_detail', pk=proyecto.pk)
    return render(request, 'core/proyecto_form.html', {'form': form, 'titulo': 'Nuevo proyecto'})


@login_required
def proyecto_detail(request, pk):
    proyecto = get_object_or_404(Proyecto, pk=pk)
    tareas_por_estado = {
        estado[0]: proyecto.tareas.filter(estado=estado[0])
        for estado in Tarea.ESTADO_CHOICES
    }
    tarea_form  = TareaForm(initial={'proyecto': proyecto})
    pago_form   = PagoForm()
    soporte_form = SoporteForm()
    return render(request, 'core/proyecto_detail.html', {
        'proyecto':        proyecto,
        'tareas_por_estado': tareas_por_estado,
        'estados_tarea':   Tarea.ESTADO_CHOICES,
        'tarea_form':      tarea_form,
        'pago_form':       pago_form,
        'soporte_form':    soporte_form,
        'pagos':           proyecto.pagos.all(),
        'soportes':        proyecto.soportes.all(),
    })


@login_required
def proyecto_edit(request, pk):
    proyecto = get_object_or_404(Proyecto, pk=pk)
    form = ProyectoForm(request.POST or None, instance=proyecto)
    if form.is_valid():
        form.save()
        messages.success(request, 'Proyecto actualizado.')
        return redirect('core:proyecto_detail', pk=pk)
    return render(request, 'core/proyecto_form.html', {'form': form, 'titulo': f'Editar — {proyecto.nombre}', 'proyecto': proyecto})


@login_required
def proyecto_kanban(request, pk):
    proyecto = get_object_or_404(Proyecto, pk=pk)
    columnas = [
        ('backlog',     'Backlog'),
        ('por_hacer',   'Por hacer'),
        ('en_progreso', 'En progreso'),
        ('revision',    'En revisión'),
        ('hecho',       'Hecho'),
    ]
    tareas_por_col = {c[0]: proyecto.tareas.filter(estado=c[0]) for c in columnas}
    tarea_form = TareaForm(initial={'proyecto': proyecto})
    return render(request, 'core/kanban.html', {
        'proyecto':      proyecto,
        'columnas':      columnas,
        'tareas_por_col': tareas_por_col,
        'tarea_form':    tarea_form,
    })


# ─── TAREAS ───────────────────────────────────────────────────────────────────
@login_required
def tarea_create(request):
    if request.method == 'POST':
        form = TareaForm(request.POST)
        if form.is_valid():
            tarea = form.save()
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'ok': True, 'id': tarea.pk, 'titulo': tarea.titulo, 'estado': tarea.estado, 'prioridad': tarea.prioridad})
            return redirect('core:proyecto_detail', pk=tarea.proyecto.pk)
    return JsonResponse({'ok': False}, status=400)


@login_required
def tarea_estado(request, pk):
    if request.method == 'POST':
        tarea = get_object_or_404(Tarea, pk=pk)
        nuevo_estado = request.POST.get('estado')
        if nuevo_estado in dict(Tarea.ESTADO_CHOICES):
            tarea.estado = nuevo_estado
            tarea.save()
            return JsonResponse({'ok': True, 'estado': tarea.estado, 'progreso': tarea.proyecto.progreso})
    return JsonResponse({'ok': False}, status=400)


@login_required
def tarea_delete(request, pk):
    if request.method == 'POST':
        tarea = get_object_or_404(Tarea, pk=pk)
        proyecto_pk = tarea.proyecto.pk
        tarea.delete()
        return JsonResponse({'ok': True})
    return JsonResponse({'ok': False}, status=400)


# ─── PAGOS ────────────────────────────────────────────────────────────────────
@login_required
def pagos_list(request):
    pagos_pendientes = Pago.objects.filter(pagado=False).select_related('proyecto__cliente')
    pagos_recibidos  = Pago.objects.filter(pagado=True).select_related('proyecto__cliente')
    total_pendiente  = pagos_pendientes.aggregate(t=Sum('monto'))['t'] or 0
    total_recibido   = pagos_recibidos.aggregate(t=Sum('monto'))['t'] or 0
    return render(request, 'core/pagos_list.html', {
        'pagos_pendientes': pagos_pendientes,
        'pagos_recibidos':  pagos_recibidos,
        'total_pendiente':  total_pendiente,
        'total_recibido':   total_recibido,
    })


@login_required
def pago_create(request, pk):
    proyecto = get_object_or_404(Proyecto, pk=pk)
    if request.method == 'POST':
        form = PagoForm(request.POST)
        if form.is_valid():
            pago = form.save(commit=False)
            pago.proyecto = proyecto
            pago.save()
            messages.success(request, 'Pago registrado.')
    return redirect('core:proyecto_detail', pk=pk)


@login_required
def pago_toggle(request, pk):
    if request.method == 'POST':
        pago = get_object_or_404(Pago, pk=pk)
        pago.pagado = not pago.pagado
        pago.fecha_recibido = timezone.now().date() if pago.pagado else None
        pago.save()
        return JsonResponse({
            'ok': True,
            'pagado': pago.pagado,
            'total_pagado': float(pago.proyecto.total_pagado),
            'saldo': float(pago.proyecto.saldo_pendiente),
            'porcentaje': pago.proyecto.porcentaje_cobrado,
        })
    return JsonResponse({'ok': False}, status=400)


# ─── SOPORTE ──────────────────────────────────────────────────────────────────
@login_required
def soporte_list(request):
    tickets = Soporte.objects.select_related('proyecto__cliente').all()
    estado  = request.GET.get('estado', '')
    if estado:
        tickets = tickets.filter(estado=estado)
    return render(request, 'core/soporte_list.html', {'tickets': tickets, 'estado_filter': estado})


@login_required
def soporte_create(request, pk):
    proyecto = get_object_or_404(Proyecto, pk=pk)
    if request.method == 'POST':
        form = SoporteForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.proyecto = proyecto
            ticket.save()
            messages.success(request, 'Ticket creado.')
    return redirect('core:proyecto_detail', pk=pk)


@login_required
def soporte_estado(request, pk):
    if request.method == 'POST':
        ticket = get_object_or_404(Soporte, pk=pk)
        nuevo  = request.POST.get('estado')
        if nuevo in dict(Soporte.ESTADO_CHOICES):
            ticket.estado = nuevo
            if nuevo == 'resuelto':
                ticket.resuelto_en = timezone.now()
            ticket.save()
            return JsonResponse({'ok': True})
    return JsonResponse({'ok': False}, status=400)
