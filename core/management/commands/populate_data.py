from django.core.management.base import BaseCommand
from core.models import Cliente, Proyecto, Tarea, Pago


DATA = [
    {
        "cliente": {
            "nombre": "Sergio Arancibia",
            "empresa": "Luxury Studios CDValles",
            "instagram": "@luxurystudios.cl",
            "notas": "Dueño del salón. Ciudad de los Valles. Abriendo nueva sucursal. Usa AgendaPro para reservas y divide boletas 50/50 con estilistas.",
        },
        "proyectos": [
            {
                "nombre": "Salón Amanda",
                "tipo": "web_profesional",
                "estado": "activo",
                "descripcion": "Web premium para salón de belleza femenino. Nueva sucursal. Diseño premium con reservas integradas vía AgendaPro y catálogo de productos con derivación a WhatsApp.",
                "dominio": "pendiente confirmar (salonamanda.cl o salonamandaspa.cl)",
                "stack": "Django · Bootstrap 5 · AgendaPro · Render · Cloudflare",
                "monto_total": 200000,
                "notas": "Cliente confirmó con $200.000 opción 1. Catálogo productos → WhatsApp sin Webpay. Inauguración nueva sucursal como fecha límite aprox 2 semanas. Pestañas: Inicio · Reservar · Profesionales · Servicios · Productos · Galería · Nosotros. Cliente confirmó por WhatsApp. Diego arranca desarrollo de inmediato sin esperar adelanto. Fecha límite real 25 de mayo.",
                "tareas": [
                    ("Recibir adelanto $100.000", "por_hacer", "critica"),
                    ("Desarrollar antes del 25 de mayo — Diego viaja a RD", "por_hacer", "critica"),
                    ("Confirmar nombre definitivo del dominio", "por_hacer", "alta"),
                    ("Registrar dominio en NIC Chile", "por_hacer", "alta"),
                    ("Crear diseño mockup premium del salón", "por_hacer", "media"),
                    ("Desarrollar estructura base Django", "por_hacer", "media"),
                    ("Integrar botón AgendaPro para reservas", "por_hacer", "media"),
                    ("Desarrollar catálogo productos con link WhatsApp", "por_hacer", "media"),
                    ("Configurar SEO on-page básico", "por_hacer", "baja"),
                    ("Deploy en Render + Cloudflare", "por_hacer", "media"),
                    ("Reunión presencial realizada y propuesta enviada", "hecho", "baja"),
                ],
                "pagos": [
                    ("adelanto", 100000, False),
                    ("entrega", 100000, False),
                ],
            }
        ],
    },
    {
        "cliente": {
            "nombre": "Felipe Dinamarca Abarca",
            "empresa": "MAX SERVICES SPA",
            "notas": "Empresa de climatización HVAC fundada en 2011. RUT 76.174.166-7. Prima de Diego trabaja en la empresa y fue contacto clave. Cliente real y pagado.",
        },
        "proyectos": [
            {
                "nombre": "Max Services SPA — Sitio Corporativo",
                "tipo": "web_profesional",
                "estado": "activo",
                "descripcion": "Sitio corporativo para empresa HVAC. Climatización, ventilación, extracción, presurización y mantenciones para retail, salud, oficinas, edificios e inmobiliarias. Rediseño visual completo en progreso.",
                "dominio": "maxservices.cl (si está disponible) o pendiente",
                "stack": "Django · Bootstrap 5 · Render · Cloudflare · NIC Chile",
                "monto_total": 0,
                "notas": "Rediseño industrial dark premium entregado en home.html. Formulario de contacto con SMTP Google Workspace funcionando y configurado. Placeholders listos para fotos reales del fotógrafo. Proyecto entregado originalmente, actualmente en fase de rediseño visual v2.",
                "tareas": [
                    ("Corregir footer include en home.html", "por_hacer", "critica"),
                    ("Recibir DNS de Valeriano para apuntar dominio a maxservicesspa.onrender.com", "por_hacer", "critica"),
                    ("Recuperar 2 imágenes de clientes borradas al hacer logos clickeables", "por_hacer", "alta"),
                    ("Agregar imagen Solar y Palau en sección proveedores", "por_hacer", "alta"),
                    ("Fotografías profesionales con amigo fotógrafo — edificios y obras esta semana", "en_progreso", "alta"),
                    ("Recibir fotos del fotógrafo para reemplazar placeholders", "por_hacer", "alta"),
                    ("Reemplazar imágenes IA por fotos reales", "por_hacer", "alta"),
                    ("Revisar SEO on-page completo", "por_hacer", "media"),
                    ("Rediseño visual home.html v2 entregado", "hecho", "media"),
                    ("Formulario contacto SMTP configurado y funcionando", "hecho", "media"),
                    ("Deploy original en Render funcionando", "hecho", "baja"),
                ],
                "pagos": [],
            }
        ],
    },
    {
        "cliente": {
            "nombre": "Sindicato AZA",
            "empresa": "Sindicato AZA",
            "notas": "Sindicato institucional. 6 personas deciden en conjunto. 4 ya dijeron que sí. Esperando los otros 2. Probabilidad 99% de cierre.",
        },
        "proyectos": [
            {
                "nombre": "Sindicato AZA — Plataforma Institucional",
                "tipo": "sistema",
                "estado": "activo",
                "descripcion": "Plataforma web institucional autogestionable para sindicato. Comunicados, documentos descargables, beneficios, capacitaciones y panel de administración. Producto reutilizable como base para futuros sindicatos e instituciones.",
                "dominio": "pendiente",
                "stack": "Django MVT · Bootstrap 5 · Render · Cloudflare",
                "monto_total": 850000,
                "notas": "Son 6 personas que deciden juntos. 4 ya aprobaron. Esperando 2 restantes. 99% seguro. Propuesta enviada el 23-04-2026. Producto escalable y reutilizable para otras instituciones. Diego arranca desarrollo sin esperar confirmación final.",
                "tareas": [
                    ("Arrancar desarrollo esta semana sin esperar confirmación final", "por_hacer", "critica"),
                    ("Confirmar aprobación de los 2 restantes", "por_hacer", "critica"),
                    ("Recibir adelanto $425.000", "por_hacer", "alta"),
                    ("Definir interlocutor único del cliente", "por_hacer", "alta"),
                    ("Iniciar desarrollo estructura base Django", "backlog", "media"),
                    ("Desarrollar módulo comunicados", "backlog", "media"),
                    ("Desarrollar módulo documentos PDF descargables", "backlog", "media"),
                    ("Desarrollar módulo beneficios", "backlog", "media"),
                    ("Desarrollar panel administración autogestionable", "backlog", "media"),
                    ("Propuesta enviada y presentada", "hecho", "baja"),
                ],
                "pagos": [
                    ("adelanto", 425000, False),
                    ("entrega", 425000, False),
                ],
            }
        ],
    },
    {
        "cliente": {
            "nombre": "Travesía Logística",
            "empresa": "Travesía Logística",
            "notas": "Empresa logística y de transporte con camiones. Cliente real. Proyecto entregado y desplegado. Caso fuerte de portafolio para GoGoDevS.",
        },
        "proyectos": [
            {
                "nombre": "Travesía Logística — Sitio Corporativo",
                "tipo": "web_profesional",
                "estado": "entregado",
                "descripcion": "Sitio corporativo para empresa logística y de camiones. Imagen profesional, presencia corporativa, branding y confianza. Caso de portafolio real para GoGoDevS.",
                "dominio": "travesialogistica.cl",
                "stack": "Django · Python · Render · Cloudflare · NIC Chile",
                "monto_total": 0,
                "notas": "Proyecto entregado y desplegado en producción. Cliente configuró su propia cuenta Render con tarjeta propia. Usado como caso de estudio en marketing y reels de GoGoDevS. Deploy exitoso con dominio propio. Cliente tiene Zoho Mail configurado en su PC. Render y dominio a nombre del cliente. Proyecto 100% cerrado.",
                "tareas": [
                    ("Deploy en producción completado", "hecho", "media"),
                    ("Cliente configuró Render con tarjeta propia", "hecho", "baja"),
                    ("Crear reels y contenido para Instagram de GoGoDevS", "por_hacer", "media"),
                    ("Agregar como caso de éxito en gogodevs.cl", "por_hacer", "media"),
                    ("Verificar fecha de vencimiento del dominio — Diego lo tiene registrado, renovación anual", "por_hacer", "media"),
                ],
                "pagos": [],
            }
        ],
    },
    {
        "cliente": {
            "nombre": "Yayito",
            "empresa": "La Dolce Mammina",
            "notas": "Banquetería y catering para eventos. Sofía (la Sofi) participa en decisiones estéticas, fotos y catálogo. Relación cercana y de confianza. Comunicación vía WhatsApp.",
        },
        "proyectos": [
            {
                "nombre": "La Dolce Mammina — Landing Web",
                "tipo": "web_base",
                "estado": "revision",
                "descripcion": "Landing page premium para banquetería y catering. Servicios: matrimonios, coffee break, garzones, bartender, vajilla, tablas de charcutería, decoración de eventos. Diseño premium artesanal orientado a conversión y cotizaciones.",
                "dominio": "ladolcemammina.cl (pendiente registrar)",
                "stack": "Django · Bootstrap · Python · HTML · CSS · JS vanilla",
                "monto_total": 200000,
                "notas": "Proyecto pagado completamente. Sofía pide ajustes estéticos y más fotos reales de eventos. Pendiente definir dominio, incorporar fotografías finales y cerrar detalles visuales antes del deploy oficial. Se ofreció mantención mensual $15.000 CLP pendiente confirmar. Uno de los primeros casos formales de GoGoDevS — importante para portafolio y reels. Sofía quiere cambio de paleta completa a rosado petal #F9E6EA y valentine #FF85A2. El negocio creció de tablas de charcutería a banquetería completa. Diego le pidió que mande TODO el contenido de una sola vez antes de hacer cambios. Cuando mande todo se cobra nuevamente por los cambios. Primera web de GoGoDevS, cobrada a $100.000.",
                "tareas": [
                    ("Esperar que Sofía mande TODO el contenido nuevo de una vez", "por_hacer", "alta"),
                    ("Cotizar cobro por rediseño y nuevo contenido", "por_hacer", "media"),
                    ("Incorporar fotografías reales de eventos (Sofía)", "por_hacer", "alta"),
                    ("Cerrar ajustes estéticos del catálogo", "por_hacer", "alta"),
                    ("Actualizar paleta a petal #F9E6EA y valentine #FF85A2", "backlog", "alta"),
                    ("Actualizar catálogo completo de banquetería (ya no solo tablas)", "backlog", "alta"),
                    ("Registrar dominio ladolcemammina.cl en NIC Chile", "por_hacer", "alta"),
                    ("Deploy en Render + Cloudflare", "por_hacer", "media"),
                    ("Confirmar plan de mantención mensual $15.000", "por_hacer", "media"),
                    ("Agregar como caso de éxito en gogodevs.cl", "por_hacer", "baja"),
                    ("Desarrollo funcional completado", "hecho", "media"),
                    ("Pago completo recibido", "hecho", "media"),
                ],
                "pagos": [
                    ("adelanto", 100000, True),
                    ("entrega", 100000, True),
                ],
            }
        ],
    },
    {
        "cliente": {
            "nombre": "Diego Dinamarca",
            "empresa": "GoGoDevS (Proyecto propio)",
            "email": "diegodinamarca.a@gmail.com",
            "notas": "Proyecto propio de GoGoDevS. Plataforma de directorio y marketplace de negocios locales para Chile.",
        },
        "proyectos": [
            {
                "nombre": "ServiPlace — Directorio Local Chile",
                "tipo": "sistema",
                "estado": "prospecto",
                "descripcion": "Plataforma escalable de directorio y marketplace de negocios y servicios locales. Piloto en Ciudad de los Valles, luego Maipú y finalmente Chile completo. Modelo tipo directorio local con perfiles de negocios, categorías y búsqueda por zona.",
                "dominio": "serviplace.cl",
                "stack": "Django · PostgreSQL · Render · Cloudflare",
                "monto_total": 0,
                "notas": "Proyecto propio con potencial MUY alto. Piloto estratégico en Ciudad de los Valles por conexión familiar de Diego. Objetivo escalar a comunas, ciudades y Chile completo. Futuro producto SaaS. No tiene cliente externo — es el gran proyecto propio de GoGoDevS.",
                "tareas": [
                    ("Definir MVP para Ciudad de los Valles", "por_hacer", "alta"),
                    ("Diseñar modelo de negocio y monetización", "por_hacer", "alta"),
                    ("Diseñar arquitectura de base de datos", "por_hacer", "media"),
                    ("Definir categorías de negocios del piloto", "por_hacer", "media"),
                    ("Diseñar landing y onboarding de negocios", "backlog", "media"),
                    ("Desarrollar módulo de búsqueda por zona/categoría", "backlog", "media"),
                    ("Conseguir primeros 10 negocios piloto en CDValles", "backlog", "alta"),
                    ("Definir estrategia SEO local por comuna", "backlog", "media"),
                    ("Concepto e idea validados", "hecho", "baja"),
                ],
                "pagos": [],
            }
        ],
    },
    {
        "cliente": {
            "nombre": "FCO Climatización",
            "empresa": "FCO Climatización",
            "notas": "Empresa de climatización y aire acondicionado. Proyecto completamente entregado y operativo en producción. Actualmente en plan gratuito de Render (servidor duerme por inactividad). Cliente no quiere pagar $7 USD/mes del plan Starter.",
        },
        "proyectos": [
            {
                "nombre": "FCO Climatización — Sitio Corporativo",
                "tipo": "web_profesional",
                "estado": "entregado",
                "descripcion": "Sitio corporativo completo para empresa de climatización. Portafolio de instalaciones y mantenciones, formulario de contacto, integración WhatsApp, SEO básico, panel administrativo Django. Deploy completo en producción.",
                "dominio": "fcoclimatizacion.cl",
                "stack": "Django · Bootstrap · PostgreSQL · Render · Cloudflare · GitHub · NIC Chile",
                "monto_total": 0,
                "notas": "100% operativo en producción. Dominio apuntando correctamente. Nameservers en Cloudflare. SSL activo. Proxy Cloudflare configurado. GitHub: GoGo-DevS/FcoClimatizacion. Problema actual: servidor duerme en plan gratuito Render. Cliente no quiere pagar upgrade. Solución definitiva es UptimeRobot — hace ping cada 5 minutos, mantiene servidor despierto, gratis, sin necesidad de PC prendido.",
                "tareas": [
                    ("Configurar UptimeRobot gratuito para evitar sleep en Render plan gratuito", "por_hacer", "alta"),
                    ("Resolver problema de sleep en Render plan gratuito", "por_hacer", "alta"),
                    ("Evaluar migración a hosting más económico compatible Django", "por_hacer", "media"),
                    ("Agregar como caso de éxito en gogodevs.cl", "por_hacer", "media"),
                    ("Deploy en producción completado", "hecho", "media"),
                    ("Dominio + Cloudflare + SSL configurado", "hecho", "baja"),
                    ("Panel administrativo Django funcionando", "hecho", "baja"),
                ],
                "pagos": [],
            }
        ],
    },
    {
        "cliente": {
            "nombre": "Dulcecitaa",
            "empresa": "Dulcecitaa",
            "notas": "Repostería artesanal premium. Alfajores, dulces, pedidos personalizados y despacho a domicilio. Marca femenina, elegante, minimalista y premium. Comunicación directa con Diego.",
        },
        "proyectos": [
            {
                "nombre": "Dulcecitaa — E-commerce Repostería",
                "tipo": "web_profesional",
                "estado": "pausado",
                "descripcion": "E-commerce completo para repostería artesanal premium. Catálogo de productos, carrito de compras, checkout, cálculo de despacho, confirmación automática por correo al cliente y notificación interna. Branding rosado pastel, tipografía elegante, mobile-first.",
                "dominio": "pendiente definir",
                "stack": "Django · Python · Bootstrap · HTML · CSS · JS vanilla · SMTP Gmail · App Password",
                "monto_total": 0,
                "notas": "Flujo de ecommerce ya funcional — carrito, checkout y correos HTML automáticos operativos. Pruebas desde celular en red local LAN. Problema ALLOWED_HOSTS resuelto en desarrollo. Pendiente deploy productivo, dominio, SSL y modo producción DEBUG=False. Proyecto de la pareja de Diego. Pausado porque ella no define logo ni paleta de colores. Vende repostería/banquetería a empresas incluyendo AZA. Sin Instagram activo, solo vende por contacto directo. Tiene cartera de clientes real. Potencial alto cuando ella se decida.",
                "tareas": [
                    ("Esperar decisión de paleta y logo de ella para reactivar", "por_hacer", "baja"),
                    ("Configurar deploy en Render producción", "por_hacer", "critica"),
                    ("Registrar y configurar dominio", "por_hacer", "alta"),
                    ("Configurar SSL y Cloudflare", "por_hacer", "alta"),
                    ("Activar DEBUG=False y static files producción", "por_hacer", "alta"),
                    ("Completar pruebas responsive mobile", "por_hacer", "alta"),
                    ("Integrar métodos de pago (Webpay u otro)", "por_hacer", "media"),
                    ("Configurar panel admin para gestión de productos y pedidos", "por_hacer", "media"),
                    ("Optimización SEO básico", "por_hacer", "baja"),
                    ("Integrar WhatsApp flotante", "por_hacer", "baja"),
                    ("Carrito de compras funcionando", "hecho", "media"),
                    ("Checkout funcional", "hecho", "media"),
                    ("Correos automáticos cliente + interno funcionando", "hecho", "media"),
                    ("SMTP Gmail configurado", "hecho", "baja"),
                    ("Branding y diseño visual definido", "hecho", "baja"),
                ],
                "pagos": [],
            }
        ],
    },
]


class Command(BaseCommand):
    help = "Poblar la base de datos con clientes, proyectos, tareas y pagos iniciales."

    def handle(self, *args, **kwargs):
        clientes_creados = 0
        proyectos_creados = 0
        proyectos_actualizados = 0
        tareas_creadas = 0
        tareas_actualizadas = 0
        pagos_creados = 0

        for entry in DATA:
            cd = entry["cliente"]
            cliente, created = Cliente.objects.get_or_create(
                nombre=cd["nombre"],
                empresa=cd["empresa"],
                defaults={
                    "email": cd.get("email", ""),
                    "instagram": cd.get("instagram", ""),
                    "telefono": cd.get("telefono", ""),
                    "notas": cd.get("notas", ""),
                },
            )
            if created:
                clientes_creados += 1
                self.stdout.write(f"  + Cliente: {cliente}")
            else:
                self.stdout.write(f"  ~ Cliente ya existe: {cliente}")

            for pd in entry["proyectos"]:
                proyecto, created = Proyecto.objects.update_or_create(
                    cliente=cliente,
                    nombre=pd["nombre"],
                    defaults={
                        "tipo": pd["tipo"],
                        "estado": pd["estado"],
                        "descripcion": pd["descripcion"],
                        "dominio": pd["dominio"],
                        "stack": pd["stack"],
                        "monto_total": pd["monto_total"],
                        "notas": pd["notas"],
                    },
                )
                if created:
                    proyectos_creados += 1
                    self.stdout.write(f"    + Proyecto: {proyecto.nombre}")
                else:
                    proyectos_actualizados += 1
                    self.stdout.write(f"    ~ Proyecto actualizado: {proyecto.nombre}")

                for orden, (titulo, estado, prioridad) in enumerate(pd["tareas"]):
                    _, created = Tarea.objects.update_or_create(
                        proyecto=proyecto,
                        titulo=titulo,
                        defaults={
                            "estado": estado,
                            "prioridad": prioridad,
                            "orden": orden,
                        },
                    )
                    if created:
                        tareas_creadas += 1
                    else:
                        tareas_actualizadas += 1

                for tipo, monto, pagado in pd["pagos"]:
                    _, created = Pago.objects.get_or_create(
                        proyecto=proyecto,
                        tipo=tipo,
                        monto=monto,
                        defaults={"pagado": pagado},
                    )
                    if created:
                        pagos_creados += 1

        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS("=" * 50))
        self.stdout.write(self.style.SUCCESS("Población completada:"))
        self.stdout.write(f"  Clientes creados:       {clientes_creados}")
        self.stdout.write(f"  Proyectos creados:      {proyectos_creados}")
        self.stdout.write(f"  Proyectos actualizados: {proyectos_actualizados}")
        self.stdout.write(f"  Tareas creadas:         {tareas_creadas}")
        self.stdout.write(f"  Tareas actualizadas:    {tareas_actualizadas}")
        self.stdout.write(f"  Pagos creados:          {pagos_creados}")
        self.stdout.write(self.style.SUCCESS("=" * 50))
