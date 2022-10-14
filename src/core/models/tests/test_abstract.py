from core.models.abstract import (
    ActiveModel
)
from django.db import connection
from django.db import models
from django.test import TestCase


class ActiveModelTest(TestCase):
    class ContainerTestModel(ActiveModel):
        class Meta:
            app_label = "test_active_model"
            db_table = "test_active_model"

        objects = models.Manager.from_queryset(ActiveModel.QuerySet)()

    model = ContainerTestModel

    def setUp(self):
        with connection.schema_editor(atomic=True) as schema_editor:
            schema_editor.create_model(self.model)

    def tearDown(self):
        with connection.schema_editor() as schema_editor:
            schema_editor.delete_model(self.model)

    def test_is_active(self):
        self.assertEqual(self.model.objects.all().active.count(), 0)
        model_active: ActiveModel = self.model.objects.create()
        self.assertEqual(self.model.objects.all().active.count(), 0)

        self.assertFalse(model_active.is_active)
        model_active.activate()
        self.assertEqual(self.model.objects.all().active.count(), 1)
        self.assertTrue(model_active.is_active)

    def test_is_deactivated(self):
        self.assertEqual(self.model.objects.all().deactivated.count(), 0)
        model_active: ActiveModel = self.model.objects.create(active=True)
        self.assertEqual(self.model.objects.all().deactivated.count(), 0)

        self.assertFalse(model_active.is_deactivated)
        model_active.deactivate()
        self.assertEqual(self.model.objects.all().deactivated.count(), 1)
        self.assertTrue(model_active.is_deactivated)
