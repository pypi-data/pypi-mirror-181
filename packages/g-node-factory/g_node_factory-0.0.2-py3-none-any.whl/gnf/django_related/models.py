""" GNodeRegistry Models Definition """

import logging
import time
import uuid

from django.db import models

from gnf.data_classes import BaseGNode
from gnf.data_classes import GpsPoint
from gnf.enums import CoreGNodeRole
from gnf.enums import GNodeStatus
from gnf.errors import DcError
from gnf.errors import RegistryError


LOG_FORMAT = (
    "%(levelname) -10s %(asctime)s %(name) -30s %(funcName) "
    "-35s %(lineno) -5d: %(message)s"
)
LOGGER = logging.getLogger(__name__)


def rand_guid():
    uuid_value = uuid.uuid4()
    string_value = uuid_value.urn[9:]
    return string_value


def now_unix_s():
    return int(time.time())


class BaseGNodeDb(models.Model):

    g_node_id = models.CharField(
        max_length=210, default=rand_guid, null=True, blank=True
    )
    alias = models.CharField(max_length=210, default=None, null=True, blank=True)
    prev_alias = models.CharField(max_length=210, default=None, null=True, blank=True)
    status_value = models.CharField(
        max_length=210,
        choices=[(tag.value, tag.value) for tag in GNodeStatus],
        null=True,
        blank=True,
    )
    role_value = models.CharField(
        max_length=210,
        choices=[(tag.value, tag.value) for tag in CoreGNodeRole],
        null=True,
        blank=True,
    )
    g_node_registry_addr = models.CharField(
        max_length=210, default=None, null=True, blank=True
    )
    gps_point_id = models.CharField(max_length=210, default=None, null=True, blank=True)
    ownership_deed_nft_id = models.IntegerField(default=None, null=True, blank=True)
    ownership_deed_validator_addr = models.CharField(
        max_length=210, default=None, null=True, blank=True
    )
    owner_addr = models.CharField(max_length=210, default=None, null=True, blank=True)
    daemon_addr = models.CharField(max_length=210, default=None, null=True, blank=True)
    trading_rights_nft_id = models.IntegerField(default=None, null=True, blank=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        try:
            self._old_attrs = {
                key: value
                for key, value in vars(self).items()
                if (key != "id" and key != "_old_attrs" and key != "_state")
            }
        except AttributeError:
            LOGGER.debug("No old attributes found")
            self._old_attrs = {}
        # LOGGER.debug(f"self._old_attrs is {self._old_attrs}")

    class Meta:
        db_table = "base_g_node"

    @property
    def dc(self) -> BaseGNode:
        d = {
            key.name: getattr(self, key.name)
            for key in self._meta.fields
            if (not key.is_relation and key.name != "id" and key.name != "_old_attrs")
        }
        dc_d = dict(
            d,
            status=GNodeStatus(d["status_value"]),
            role=CoreGNodeRole(d["role_value"]),
        )
        del dc_d["status_value"]
        del dc_d["role_value"]
        if dc_d["g_node_id"] in BaseGNode.by_id.keys():
            return BaseGNode.by_id[dc_d["g_node_id"]]
        else:
            return BaseGNode(**dc_d)

    def save(self, *args, **kwargs):
        d = {
            key.name: getattr(self, key.name)
            for key in self._meta.fields
            if (not key.is_relation and key.name != "id" and key.name != "_old_attrs")
        }

        dc_d = dict(
            d,
            role=CoreGNodeRole(d["role_value"]),
            status=GNodeStatus(d["status_value"]),
        )
        del dc_d["role_value"]
        del dc_d["status_value"]

        if self.pk is None:
            # Creation axiom checks
            self.creation_axiom_1(d)
            try:
                BaseGNode.check_creation_axioms(dc_d)
            except DcError as e:
                raise RegistryError(e)
            dc_rep = BaseGNode(**dc_d)
        else:
            # Update axiom checks
            old_d = {
                key.name: self._old_attrs[key.name]
                for key in self._meta.fields
                if (
                    not key.is_relation
                    and key.name != "id"
                    and key.name != "_old_attrs"
                    and self._old_attrs.get(key.name, None)
                )
            }
            old_dc_d = dict(
                d,
                role=CoreGNodeRole(old_d["role_value"]),
                status=GNodeStatus(old_d["status_value"]),
            )
            del old_dc_d["role_value"]
            del old_dc_d["status_value"]
            dc_rep = BaseGNode(**old_dc_d)
            try:
                dc_rep.check_update_axioms(dc_d)
            except DcError as e:
                raise RegistryError(f"BaseGNode update failed: {e}")
            for key, value in d.items():
                setattr(dc_rep, key, value)
        super().save(*args, **kwargs)
        BaseGNode.by_id[d["g_node_id"]] = BaseGNode(**dc_d)
        BaseGNode.by_alias[d["alias"]] = BaseGNode(**dc_d)

        self._old_attrs = {
            key: value
            for key, value in vars(self).items()
            if (key != "id" and key != "_old_attrs" and key != "_state")
        }
        BaseGNodeHistory.objects.create(**d)

    def __str__(self):
        return self.dc.__repr__()

    @classmethod
    def creation_axiom_1(cls, attributes):
        """Creation Axiom 1: g_node_alias cannot be used, now or previously, by this or
        other BaseGNodes"""
        old_and_existing_aliases = list(
            BaseGNodeHistory.objects.order_by()
            .values_list("alias", flat=True)
            .distinct()
        )
        if attributes["alias"] in old_and_existing_aliases:
            raise RegistryError(
                "Axiom 6: g_node_alias cannot be used, now or previously, by this"
                f" or other other BaseGNodes.  Alias {attributes['alias']} already taken."
            )

    def update_axiom_1(self, new_attributes):
        """Update Axiom 1: g_node_alias cannot be used, now or previously, by this or
        other BaseGNodes"""
        if self.alias == new_attributes["alias"]:
            return
        old_and_existing = list(
            BaseGNodeHistory.objects.order_by()
            .values_list("alias", flat=True)
            .distinct()
        )
        if new_attributes["alias"] in old_and_existing:
            raise RegistryError(
                "Axiom 6: g_node_alias cannot be used, now or previously, by this"
                f" or other other BaseGNodes.  Alias {new_attributes['alias']} already taken."
            )


class BaseGNodeHistory(models.Model):
    time_s = models.IntegerField(default=now_unix_s)
    g_node_id = models.CharField(max_length=210, default=None, null=True, blank=True)
    alias = models.CharField(max_length=210, default=None, null=True, blank=True)
    prev_alias = models.CharField(max_length=210, default=None, null=True, blank=True)
    status_value = models.CharField(
        max_length=210,
        choices=[(tag.value, tag.value) for tag in GNodeStatus],
        null=True,
        blank=True,
    )
    role_value = models.CharField(
        max_length=210,
        choices=[(tag.value, tag.value) for tag in CoreGNodeRole],
        null=True,
        blank=True,
    )
    g_node_registry_addr = models.CharField(
        max_length=210, default=None, null=True, blank=True
    )
    gps_point_id = models.CharField(max_length=210, default=None, null=True, blank=True)
    ownership_deed_nft_id = models.IntegerField(default=None, null=True, blank=True)
    ownership_deed_validator_addr = models.CharField(
        max_length=210, default=None, null=True, blank=True
    )
    owner_addr = models.CharField(max_length=210, default=None, null=True, blank=True)
    daemon_addr = models.CharField(max_length=210, default=None, null=True, blank=True)
    trading_rights_nft_id = models.IntegerField(default=None, null=True, blank=True)

    class Meta:
        db_table = "base_g_node_history"


class GpsPointDb(models.Model):
    gps_point_id = models.CharField(max_length=210, default=rand_guid)
    lat = models.DecimalField(max_digits=9, decimal_places=6)
    lon = models.DecimalField(max_digits=9, decimal_places=6)
    # We will address encrypting the location later
    class Meta:
        db_table = "gps_point"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        try:
            self._old_attrs = {
                key: value
                for key, value in vars(self).items()
                if (key != "_old_attrs" and key != "_state")
            }
        except AttributeError:
            LOGGER.debug("No old attributes found")
            self._old_attrs = {}
        # LOGGER.debug(f"self._old_attrs is {self._old_attrs}")

    @property
    def dc(self) -> GpsPoint:
        d = {
            key.name: getattr(self, key.name)
            for key in self._meta.fields
            if (not key.is_relation and key.name != "id" and key.name != "_old_attrs")
        }
        if d["gps_point_id"] in GpsPoint.by_id.keys():
            return GpsPoint.by_id[d["gps_point_id"]]
        else:
            return GpsPoint(**d)

    def save(self, *args, **kwargs):
        d = {
            key.name: getattr(self, key.name)
            for key in self._meta.fields
            if (not key.is_relation and key.name != "id" and key.name != "_old_attrs")
        }
        if self.pk is None:
            try:
                GpsPoint.check_creation_axioms(d)
            except DcError as e:
                raise RegistryError(e)
            dc_rep = GpsPoint(**d)
        else:
            # Update axiom checks
            old_d = {
                key.name: self._old_attrs[key.name]
                for key in self._meta.fields
                if (
                    not key.is_relation
                    and key.name != "id"
                    and key.name != "_old_attrs"
                    and self._old_attrs.get(key.name, None)
                )
            }
            dc_rep = GpsPoint(**old_d)
            try:
                dc_rep.check_update_axioms(d)
            except DcError as e:
                raise RegistryError(f"GpsPoint update failed. {e}")
        super().save(*args, **kwargs)
        GpsPoint.by_id[d["gps_point_id"]] = GpsPoint(**d)

        self._old_attrs = {
            key: value
            for key, value in vars(self).items()
            if (key != "id" and key != "_old_attrs" and key != "_state")
        }
