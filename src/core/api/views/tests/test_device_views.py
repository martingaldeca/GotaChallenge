import random
import factory
from django.urls import reverse
from rest_framework import status
from core.api.serializers import DeviceSerializer, CreateOrUpdateDeviceSerializer
from core.api.views.tests.base import APITestBase
from core.factories import DeviceFactory, ActionFactory
from django.core.files.base import ContentFile
from core.models import Device


class DeviceListViewTest(APITestBase):
    url = reverse('core:list-devices')

    def test_get_200_OK(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'], [])
        devices = []
        for i in range(random.randint(1, 5)):
            devices.append(DeviceSerializer(instance=DeviceFactory(), context=self.test_context).data)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'], devices)


class CreateNewDeviceViewTest(APITestBase):
    url = reverse('core:create-device')

    def setUp(self) -> None:
        super(CreateNewDeviceViewTest, self).setUp()
        self.device_name = 'test_name'
        self.device_description = 'test_description'
        self.device_active = True
        self.image = ContentFile(
            factory.django.ImageField()._make_data(
                {'width': 1024, 'height': 768}
            ), 'example.jpg'
        )
        self.device_allowed_actions = [ActionFactory(), ActionFactory()]
        self.device_allowed_actions_uuids = [action.uuid.hex for action in self.device_allowed_actions]

    def test_create_new_device_201_CREATED(self):
        data_to_send = {
            'name': self.device_name,
            'description': self.device_description,
            'image': self.image,
            'allowed_actions': self.device_allowed_actions_uuids,
            'active': self.device_active,
        }
        self.assertEqual(Device.objects.count(), 0)
        response = self.client.post(self.url, data=data_to_send)
        self.assertEqual(Device.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        device = Device.objects.last()
        self.assertEqual(response.data, CreateOrUpdateDeviceSerializer(instance=device).data)

        self.assertEqual(device.name, self.device_name)
        self.assertEqual(device.description, self.device_description)
        self.assertSameFile(device.image, self.image)
        self.assertEqual(set(device.allowed_actions.all()), set(self.device_allowed_actions))


class RetrieveUpdateDestroyDeviceViewTest(APITestBase):
    url = reverse('core:device', kwargs={'uuid': None})

    def test_get_device_200_OK(self):
        device: Device = DeviceFactory()
        self.url = reverse('core:device', kwargs={'uuid': device.uuid.hex})
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, CreateOrUpdateDeviceSerializer(instance=device).data)

    def test_update_device_200_OK(self):
        device: Device = DeviceFactory()
        self.url = reverse('core:device', kwargs={'uuid': device.uuid.hex})

        new_name = 'test_name_2'
        new_description = 'test_description_2'
        data = {
            'name': new_name,
            'description': new_description,
        }

        response = self.client.put(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        device.refresh_from_db()
        self.assertEqual(response.data, CreateOrUpdateDeviceSerializer(instance=device).data)
        self.assertEqual(device.name, new_name)
        self.assertEqual(device.description, new_description)

    def test_delete_device_204_NO_CONTENT(self):
        device: Device = DeviceFactory()
        self.assertEqual(Device.objects.count(), 1)
        self.url = reverse('core:device', kwargs={'uuid': device.uuid.hex})
        response = self.client.delete(self.url)
        self.assertEqual(Device.objects.count(), 0)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
