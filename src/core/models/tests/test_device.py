from django.db import transaction
from django.test import TestCase

from core.factories import DeviceFactory, ActionFactory
from core.models import Device


class DeviceTest(TestCase):
    def test_active_actions(self):
        device: Device = DeviceFactory(allowed_actions__total_active=3, allowed_actions__total_deactivated=3)
        self.assertEqual(device.allowed_actions.count(), 6)
        self.assertEqual(device.active_actions.count(), 3)

    def test_deactivated_actions(self):
        device: Device = DeviceFactory(allowed_actions__total_active=3, allowed_actions__total_deactivated=3)
        self.assertEqual(device.allowed_actions.count(), 6)
        self.assertEqual(device.deactivated_actions.count(), 3)

    def test_add_action(self):
        device: Device = DeviceFactory(allowed_actions__total_active=0, allowed_actions__total_deactivated=0)
        test_data_list = [
            (True, 1, 0),
            (False, 0, 1),
        ]
        for test_data in test_data_list:
            with self.subTest(
                    test_data=test_data
            ), transaction.atomic():
                active, total_active, total_deactivated = test_data
                device.add_action(action=ActionFactory(), active=active)
                self.assertEqual(device.allowed_actions.count(), 1)
                self.assertEqual(device.active_actions.count(), total_active)
                self.assertEqual(device.deactivated_actions.count(), total_deactivated)
                transaction.set_rollback(True)
