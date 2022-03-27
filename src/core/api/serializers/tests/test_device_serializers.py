import factory
import uuid
from unittest import mock
from django.core.files.base import ContentFile
from core.exceptions import api as api_exceptions
from django.test import TestCase
from django.db import transaction
from core.api.serializers import DeviceSerializer, ActionSerializer, CreateOrUpdateDeviceSerializer
from core.factories import DeviceFactory, ActionFactory
from core.models import Device


class DeviceSerializerTest(TestCase):

    def test_data(self):
        device: Device = DeviceFactory()
        expected_data = {
            'uuid': device.uuid.hex,
            'name': device.name,
            'description': device.description,
            'allowed_actions': ActionSerializer(device.allowed_actions, many=True).data,
            'image': device.image.url,
            'active': device.active,
            'deactivated_actions': ActionSerializer(device.deactivated_actions, many=True).data,
            'active_actions': ActionSerializer(device.active_actions, many=True).data,
        }
        self.assertEqual(DeviceSerializer(device).data, expected_data)


class CreateOrUpdateDeviceSerializerTest(TestCase):

    def setUp(self) -> None:
        self.device_name = 'test_name'
        self.device_description = 'test_description'
        self.device_allowed_actions = [ActionFactory(), ActionFactory()]
        self.device_allowed_actions_uuids = [action.uuid.hex for action in self.device_allowed_actions]
        self.image = ContentFile(
            factory.django.ImageField()._make_data(
                {'width': 1024, 'height': 768}
            ), 'example.jpg'
        )

    def test_validate_allowed_actions_action_not_found(self):
        device: Device = DeviceFactory()
        with self.assertRaises(api_exceptions.NotFoundException) as expected_exception:
            data = {
                'device': device.uuid.hex,
                'name': self.device_name,
                'description': self.device_description,
                'image': self.image,
                'allowed_actions': [uuid.uuid4(), ],
            }
            serializer = CreateOrUpdateDeviceSerializer(data=data)
            serializer.is_valid()
        self.assertEqual(expected_exception.exception.detail['message'], 'action-not-found')

    def test_create(self):
        test_data_list = [
            (self.device_allowed_actions_uuids, len(self.device_allowed_actions_uuids)),
            ([], 0),
        ]
        for test_data in test_data_list:
            with self.subTest(test_data=test_data), transaction.atomic():
                allowed_actions, add_action_call_count, = test_data
                with mock.patch.object(
                    Device, 'add_action'
                ) as mock_add_action:
                    data = {
                        'name': self.device_name,
                        'description': self.device_description,
                        'image': ContentFile(
                            factory.django.ImageField()._make_data(
                                {'width': 1024, 'height': 768}
                            ), 'example.jpg'
                        ),
                        'allowed_actions': allowed_actions,
                    }
                    serializer = CreateOrUpdateDeviceSerializer(data=data)
                    self.assertTrue(serializer.is_valid(raise_exception=True))
                    self.assertEqual(Device.objects.count(), 0)
                    serializer.create(serializer.validated_data)
                    self.assertEqual(Device.objects.count(), 1)
                    device = Device.objects.last()
                    self.assertEqual(device.name, self.device_name)
                    self.assertEqual(device.description, self.device_description)
                    self.assertIsNotNone(device.image)
                    self.assertEqual(mock_add_action.call_count, add_action_call_count)
                transaction.set_rollback(True)

    def test_data(self):
        device: Device = DeviceFactory()
        with mock.patch.object(
            Device, 'add_action'
        ) as mock_add_action:
            data = {
                'device': device.uuid.hex,
                'name': self.device_name,
                'description': self.device_description,
                'image': ContentFile(
                    factory.django.ImageField()._make_data(
                        {'width': 1024, 'height': 768}
                    ), 'example.jpg'
                ),
                'allowed_actions': self.device_allowed_actions_uuids,
            }
            serializer = CreateOrUpdateDeviceSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.create(serializer.validated_data)
            device = Device.objects.last()
            self.assertEqual(serializer.data, DeviceSerializer(device).data)
            self.assertEqual(mock_add_action.call_count, len(self.device_allowed_actions_uuids))
