import graphene
import graphene_django.filter as django_filter

import karrio.server.core.models as core
import karrio.server.graph.models as graph
import karrio.server.core.filters as filters
import karrio.server.core.gateway as gateway
import karrio.server.manager.models as manager
import karrio.server.tracing.models as tracing
import karrio.server.providers.models as providers
import karrio.server.user.serializers as user_serializers
import karrio.server.manager.serializers as manager_serializers
import karrio.server.graph.extension.base.mutations as mutations
import karrio.server.graph.extension.base.types as types
import karrio.server.graph.utils as utils


class Query:
    user = graphene.Field(types.UserType)
    token = graphene.Field(types.TokenType, org_id=graphene.String(required=False))

    user_connections = graphene.List(
        graphene.NonNull(types.ConnectionType),
        required=True,
        default_value=[],
    )
    system_connections = graphene.List(
        graphene.NonNull(types.SystemConnectionType),
        required=True,
        default_value=[],
    )

    default_templates = graphene.Field(
        types.DefaultTemplatesType, required=True, default_value={}
    )
    address_templates = django_filter.DjangoFilterConnectionField(
        types.AddressTemplateType, required=True, default_value=[]
    )
    customs_templates = django_filter.DjangoFilterConnectionField(
        types.CustomsTemplateType, required=True, default_value=[]
    )
    parcel_templates = django_filter.DjangoFilterConnectionField(
        types.ParcelTemplateType, required=True, default_value=[]
    )

    log = graphene.Field(types.LogType, id=graphene.Int(required=True))
    logs = django_filter.DjangoFilterConnectionField(
        types.LogType,
        required=True,
        default_value=[],
        filterset_class=filters.LogFilter,
    )

    tracingrecord = graphene.Field(
        types.TracingRecordType, id=graphene.String(required=True)
    )
    tracingrecords = django_filter.DjangoFilterConnectionField(
        types.TracingRecordType,
        required=True,
        default_value=[],
        filterset_class=filters.TracingRecordFilter,
    )

    shipment = graphene.Field(types.ShipmentType, id=graphene.String(required=True))
    shipments = django_filter.DjangoFilterConnectionField(
        types.ShipmentType,
        required=True,
        default_value=[],
        filterset_class=filters.ShipmentFilters,
    )

    tracker = graphene.Field(types.TrackerType, id=graphene.String(required=True))
    trackers = django_filter.DjangoFilterConnectionField(
        types.TrackerType,
        required=True,
        default_value=[],
        filterset_class=filters.TrackerFilters,
    )

    @utils.authentication_required
    @utils.authorization_required()
    def resolve_user(self, info):
        return types.User.objects.get(id=info.context.user.id)

    @utils.authentication_required
    @utils.authorization_required()
    def resolve_token(self, info, **kwargs):
        return user_serializers.TokenSerializer.retrieve_token(info.context, **kwargs)

    @utils.authentication_required
    @utils.authorization_required()
    def resolve_user_connections(self, info, **kwargs):
        connections = providers.Carrier.access_by(info.context).filter(
            created_by__isnull=False,
            test_mode=getattr(info.context, "test_mode", False),
        )
        return [connection.settings for connection in connections]

    @utils.authentication_required
    @utils.authorization_required()
    def resolve_system_connections(self, info, **kwargs):
        return gateway.Carriers.list(
            context=info.context,
            system_only=True,
        )

    @utils.authentication_required
    @utils.authorization_required()
    def resolve_default_templates(self, info, **kwargs):
        templates = graph.Template.access_by(info.context).filter(is_default=True)

        return dict(
            default_address=templates.filter(address__isnull=False).first(),
            default_customs=templates.filter(customs__isnull=False).first(),
            default_parcel=templates.filter(parcel__isnull=False).first(),
        )

    @utils.authentication_required
    @utils.authorization_required()
    def resolve_address_templates(self, info, **kwargs):
        return graph.Template.access_by(info.context).filter(address__isnull=False)

    @utils.authentication_required
    @utils.authorization_required()
    def resolve_customs_templates(self, info, **kwargs):
        return graph.Template.access_by(info.context).filter(customs__isnull=False)

    @utils.authentication_required
    @utils.authorization_required()
    def resolve_parcel_templates(self, info, **kwargs):
        return graph.Template.access_by(info.context).filter(parcel__isnull=False)

    @utils.authentication_required
    @utils.authorization_required()
    def resolve_log(self, info, **kwargs):
        return core.APILog.access_by(info.context).filter(**kwargs).first()

    @utils.authentication_required
    @utils.authorization_required()
    def resolve_logs(self, info, **kwargs):
        return core.APILog.access_by(info.context)

    @utils.authentication_required
    @utils.authorization_required()
    def resolve_tacingrecord(self, info, **kwargs):
        return tracing.TracingRecord.access_by(info.context).filter(**kwargs).first()

    @utils.authentication_required
    @utils.authorization_required()
    def resolve_tracingrecords(self, info, **kwargs):
        return tracing.TracingRecord.access_by(info.context)

    @utils.authentication_required
    @utils.authorization_required()
    def resolve_shipment(self, info, **kwargs):
        return manager.Shipment.access_by(info.context).filter(**kwargs).first()

    @utils.authentication_required
    @utils.authorization_required()
    def resolve_shipments(self, info, **kwargs):
        return manager.Shipment.access_by(info.context)

    @utils.authentication_required
    @utils.authorization_required()
    def resolve_tracker(self, info, **kwargs):
        return manager.Tracking.access_by(info.context).filter(**kwargs).first()

    @utils.authentication_required
    @utils.authorization_required()
    def resolve_trackers(self, info, **kwargs):
        return manager.Tracking.access_by(info.context)


class Mutation:
    # User related mutations
    update_user = mutations.UpdateUser.Field()
    register_user = mutations.RegisterUser.Field()
    confirm_email = mutations.ConfirmEmail.Field()
    mutate_token = mutations.TokenMutation.Field()
    change_password = mutations.ChangePassword.Field()
    request_email_change = mutations.RequestEmailChange.Field()
    confirm_email_change = mutations.ConfirmEmailChange.Field()
    request_password_reset = mutations.RequestPasswordReset.Field()
    confirm_password_reset = mutations.ConfirmPasswordReset.Field()
    enable_multi_factor = mutations.EnableMultiFactor.Field()
    confirm_multi_factor = mutations.ConfirmMultiFactor.Field()
    disable_multi_factor = mutations.DisableMultiFactor.Field()

    # Carrier connection related mutations
    create_connection = mutations.CreateCarrierConnection.Field()
    update_connection = mutations.UpdateCarrierConnection.Field()
    delete_connection = utils.create_delete_mutation(
        "DeleteConnection", providers.Carrier
    ).Field()
    mutate_system_connection = mutations.SystemCarrierMutation.Field()

    # Template related mutations
    create_address_template = mutations.create_template_mutation("Address").Field()
    update_address_template = mutations.create_template_mutation(
        "Address", True
    ).Field()
    create_customs_template = mutations.create_template_mutation("Customs").Field()
    update_customs_template = mutations.create_template_mutation(
        "Customs", True
    ).Field()
    create_parcel_template = mutations.create_template_mutation("Parcel").Field()
    update_parcel_template = mutations.create_template_mutation("Parcel", True).Field()
    delete_template = utils.create_delete_mutation(
        "DeleteTemplate", graph.Template
    ).Field()

    # Shipment related mutations
    # shipment update can be used to add/update address, customs and parcels
    partial_shipment_update = mutations.PartialShipmentUpdate.Field()

    # Commodity related mutations
    discard_commodity = utils.create_delete_mutation(
        "DiscardCommodity",
        manager.Commodity,
        validator=manager_serializers.can_mutate_commodity,
    ).Field()

    # Customs related mutations
    discard_customs = utils.create_delete_mutation(
        "DiscardCustoms",
        manager.Customs,
        validator=manager_serializers.can_mutate_customs,
    ).Field()

    # Customs related mutations
    discard_parcel = utils.create_delete_mutation(
        "DiscardParcel", manager.Parcel, validator=manager_serializers.can_mutate_parcel
    ).Field()

    mutate_metadata = mutations.MutateMetadata.Field()
