from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Notificacion

def create_response_notification(comentario, remitente, destinatario):
    notificacion = Notificacion.objects.create(destinatario=destinatario, remitente=remitente, tipo="respuesta", comentario=comentario)
    # Emitir evento de notificación de respuesta a like
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"notifications_{destinatario.id}",
        {
            "type": "send_response_notification",
            "notification": {
                "id": notificacion.id,
                "tipo": notificacion.tipo,
                "remitente_id": notificacion.remitente.id,
                "comentario_id": notificacion.comentario.id,
                "vista": notificacion.vista,
                "fecha_creacion": notificacion.fecha_creacion.strftime("%Y-%m-%d %H:%M:%S")
            }
        }
    )