from django.http import JsonResponse
from django.shortcuts import reverse

from cabot.cabotapp.models import Service


def hipchat_descriptor(request):
    descriptor_url = request.build_absolute_uri(reverse('hipchat-descriptor'))
    glance_url = request.build_absolute_uri(reverse('hipchat-glance'))

    descriptor = {
      "name": "Cabot Integration",
      "description": "An integration to allow Cabot to send notifications to HipChat",
      "key": "com.arachnys.cabot",
      "links": {
        "homepage": "",
        "self": descriptor_url
      },
      "capabilities": {
        "hipchatApiConsumer": {
          "scopes": [
            "send_notification"
          ],
          "glance": [
              {
                  "name": {
                      "value": "Cabot Glance"
                  },
                  "queryUrl": glance_url,
                  "key": "cabot-glance",
                  "icon": {
                      "url": "https://hipchat.com/img/connect.png",
                      "url@2x": "https://hipchat.com/img/connect.png"
                  },
                  "conditions": [
                  ]
              }
          ]
        }
      }
    }

    return JsonResponse(descriptor)


def hipchat_glance(request):
    passing_services_count = Service.objects.filter(overall_status='PASSING').count()
    total_services_count = Service.objects.count()

    worst_status = (Service.objects.filter(overall_status='CRITICAL') \
        or Service.objects.filter(overall_status='ERROR') \
        or Service.objects.filter(overall_status='WARNING') \
        or Service.objects.filter(overall_status='PASSING')).first()
    if worst_status:
        worst_status = worst_status.overall_status
    else:
        worst_status = None

    type_mapping = {
        None: "default",
        "PASSING": "success",
        "WARNING": "current",
        "CRITICAL": "error",
        "ERROR": "error",
    }

    lozenge_type = type_mapping.get(worst_status, 'default')

    lozenge_label = worst_status or 'UNKNOWN'

    return JsonResponse({
      "label": {
        "type": "html",
        "value": "<b>{}/{}</b> Services Passing".format(passing_services_count, total_services_count)
      },
      "status": {
        "type": "lozenge",
        "value": {
            "label": lozenge_label,
            "type": lozenge_type
        }
      },
      "metadata": {
        "isConfigured": True
      }
    })
