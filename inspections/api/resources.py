from tastypie import fields
from tastypie.resources import ModelResource, ALL
from tastypie.contrib.gis.resources import ModelResource as GisModelResource
from django.contrib.gis.geos import Polygon

from inspections.models import Establishment, Inspection, Violation
from inspections.api.serializers import GeoJSONSerializer


class EstablishmentResource(GisModelResource):

    class Meta(object):
        queryset = Establishment.objects.filter(status='active')
        allowed_methods = ['get']
        serializer = GeoJSONSerializer()
        limit = 40
        filtering = {
            'external_id': ALL,
            'type': ALL,
            'location': ALL,
            'name': ALL,
        }
        ordering = ['update_date']

    def build_filters(self, filters=None):
        if filters is None:
            filters = {}

        orm_filters = super(EstablishmentResource, self).build_filters(filters)

        if "within" in filters:
            bbox = filters['within'].split(',')
            orm_filters["location__within"] = Polygon.from_bbox(bbox)

        return orm_filters


class InspectionResource(ModelResource):
    est_id = fields.ForeignKey(EstablishmentResource, 'external_id')

    class Meta(object):
        queryset = Inspection.objects.all()
        allowed_methods = ['get']
        limit = 20
        filtering = {
            'external_id': ALL,
            'type': ALL,
            'date': ALL,
        }
        ordering = ['insp_date']


class ViolationResource(ModelResource):
    inspection_id = fields.ForeignKey(InspectionResource, 'inspection_id')

    class Meta(object):
        queryset = Violation.objects.all()
        allowed_methods = ['get']
        limit = 20
        filtering = {
            'code': ALL,
            'date': ALL,
            'inspection_id': ALL,
        }
