"""Provide common test tools for hassio."""

from __future__ import annotations

from dataclasses import fields, replace
import logging
from typing import Any
from unittest.mock import AsyncMock, Mock

from aiohasupervisor.models import (
    AddonBoot,
    AddonBootConfig,
    AddonsOptions,
    AddonsStats,
    AddonStage,
    AddonState,
    AppArmor,
    CpuArch,
    InstalledAddonComplete,
    Repository,
    StoreAddon,
    StoreAddonComplete,
    SupervisorRole,
)

from homeassistant.components.hassio.addon_manager import AddonManager
from homeassistant.core import HomeAssistant

LOGGER = logging.getLogger(__name__)
INSTALLED_ADDON_FIELDS = [field.name for field in fields(InstalledAddonComplete)]
STORE_ADDON_FIELDS = [field.name for field in fields(StoreAddonComplete)]
ADDONS_STATS_FIELDS = [field.name for field in fields(AddonsStats)]

MOCK_STORE_ADDONS = [
    StoreAddon(
        name="test",
        arch=[],
        documentation=False,
        advanced=False,
        available=True,
        build=False,
        description="Test add-on service",
        homeassistant=None,
        icon=False,
        logo=False,
        repository="core",
        slug="core_test",
        stage=AddonStage.EXPERIMENTAL,
        update_available=False,
        url="https://example.com/addons/tree/master/test",
        version_latest="1.0.0",
        version="1.0.0",
        installed=True,
    )
]

MOCK_REPOSITORIES = [
    Repository(
        slug="core",
        name="Official add-ons",
        source="core",
        url="https://home-assistant.io/addons",
        maintainer="Home Assistant",
    )
]


def mock_to_dict(obj: Mock, fields: list[str]) -> dict[str, Any]:
    """Aiohasupervisor mocks to dictionary representation."""
    return {
        field: getattr(obj, field)
        for field in fields
        if not isinstance(getattr(obj, field), Mock)
    }


def mock_addon_manager(hass: HomeAssistant) -> AddonManager:
    """Return an AddonManager instance."""
    return AddonManager(hass, LOGGER, "Test", "test_addon")


def mock_addon_store_info(
    supervisor_client: AsyncMock,
    addon_store_info_side_effect: Any | None,
) -> AsyncMock:
    """Mock Supervisor add-on store info."""
    supervisor_client.store.addon_info.side_effect = addon_store_info_side_effect
    supervisor_client.store.addon_info.return_value = StoreAddonComplete(
        slug="test",
        repository="core",
        available=True,
        installed=False,
        update_available=False,
        version="1.0.0",
        supervisor_api=False,
        supervisor_role=SupervisorRole.DEFAULT,
        advanced=False,
        arch=[CpuArch.AARCH64, CpuArch.AMD64, CpuArch.ARMV7],
        build=False,
        description="test",
        documentation=True,
        homeassistant=None,
        icon=True,
        logo=True,
        name="test",
        stage=AddonStage.STABLE,
        url=None,
        version_latest="1.0.0",
        apparmor=AppArmor.DEFAULT,
        auth_api=False,
        detached=False,
        docker_api=False,
        full_access=False,
        homeassistant_api=False,
        host_network=False,
        host_pid=False,
        ingress=False,
        long_description=None,
        rating=6,
        signed=True,
    )
    return supervisor_client.store.addon_info


def mock_addon_info(
    supervisor_client: AsyncMock, addon_info_side_effect: Any | None
) -> AsyncMock:
    """Mock Supervisor add-on info."""
    supervisor_client.addons.addon_info.side_effect = addon_info_side_effect
    supervisor_client.addons.addon_info.return_value = InstalledAddonComplete(
        slug="test",
        repository="core",
        available=True,
        update_available=False,
        version="1.0.0",
        supervisor_api=False,
        supervisor_role=SupervisorRole.DEFAULT,
        advanced=False,
        arch=[CpuArch.AARCH64, CpuArch.AMD64, CpuArch.ARMV7],
        build=False,
        description="test",
        documentation=True,
        homeassistant=None,
        icon=True,
        logo=True,
        name="test",
        stage=AddonStage.STABLE,
        url=None,
        version_latest="1.0.0",
        apparmor=AppArmor.DEFAULT,
        auth_api=False,
        detached=False,
        docker_api=False,
        full_access=False,
        homeassistant_api=False,
        host_network=False,
        host_pid=False,
        ingress=False,
        long_description=None,
        rating=6,
        signed=True,
        hostname="",
        options={},
        state=AddonState.UNKNOWN,
        dns=[],
        protected=True,
        boot_config=AddonBootConfig.AUTO,
        boot=AddonBoot.AUTO,
        schema=[],
        machine=[],
        network=None,
        network_description=None,
        host_ipc=False,
        host_uts=False,
        host_dbus=False,
        privileged=[],
        changelog=True,
        stdin=False,
        gpio=False,
        usb=False,
        uart=False,
        kernel_modules=False,
        devicetree=False,
        udev=False,
        video=False,
        audio=False,
        services=[],
        discovery=[],
        translations={},
        webui=None,
        ingress_entry=None,
        ingress_url=None,
        ingress_port=None,
        ingress_panel=None,
        audio_input=None,
        audio_output=None,
        auto_update=False,
        ip_address="0.0.0.0",
        watchdog=False,
        devices=[],
    )
    return supervisor_client.addons.addon_info


def mock_addon_not_installed(
    addon_store_info: AsyncMock, addon_info: AsyncMock
) -> AsyncMock:
    """Mock add-on not installed."""
    addon_store_info.return_value = replace(
        addon_store_info.return_value, available=True
    )
    return addon_info


def mock_addon_installed(
    addon_store_info: AsyncMock, addon_info: AsyncMock
) -> AsyncMock:
    """Mock add-on already installed but not running."""
    addon_store_info.return_value = replace(
        addon_store_info.return_value, available=True, installed=True
    )
    addon_info.return_value = replace(
        addon_info.return_value,
        available=True,
        hostname="core-test-addon",
        state=AddonState.STOPPED,
        version="1.0.0",
    )
    return addon_info


def mock_addon_running(addon_store_info: AsyncMock, addon_info: AsyncMock) -> AsyncMock:
    """Mock add-on already running."""
    addon_store_info.return_value = replace(
        addon_store_info.return_value, available=True, installed=True
    )
    addon_info.return_value = replace(addon_info.return_value, state=AddonState.STARTED)
    return addon_info


def mock_install_addon_side_effect(
    addon_store_info: AsyncMock, addon_info: AsyncMock
) -> Any | None:
    """Return the install add-on side effect."""

    async def install_addon(addon: str):
        """Mock install add-on."""
        addon_store_info.return_value = replace(
            addon_store_info.return_value, available=True, installed=True
        )
        addon_info.return_value = replace(
            addon_info.return_value,
            available=True,
            state=AddonState.STOPPED,
            version="1.0.0",
        )

    return install_addon


def mock_start_addon_side_effect(
    addon_store_info: AsyncMock, addon_info: AsyncMock
) -> Any | None:
    """Return the start add-on options side effect."""

    async def start_addon(addon: str) -> None:
        """Mock start add-on."""
        addon_store_info.return_value = replace(
            addon_store_info.return_value, available=True, installed=True
        )
        addon_info.return_value = replace(
            addon_info.return_value, available=True, state=AddonState.STARTED
        )

    return start_addon


def mock_set_addon_options_side_effect(addon_options: dict[str, Any]) -> Any | None:
    """Return the set add-on options side effect."""

    async def set_addon_options(slug: str, options: AddonsOptions) -> None:
        """Mock set add-on options."""
        addon_options.update(options.config)

    return set_addon_options


def mock_addon_stats(supervisor_client: AsyncMock) -> AsyncMock:
    """Mock addon stats."""
    supervisor_client.addons.addon_stats.return_value = AddonsStats(
        cpu_percent=0.99,
        memory_usage=182611968,
        memory_limit=3977146368,
        memory_percent=4.59,
        network_rx=362570232,
        network_tx=82374138,
        blk_read=46010945536,
        blk_write=15051526144,
    )
    return supervisor_client.addons.addon_stats
