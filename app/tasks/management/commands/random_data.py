import random


from tasks.models import Task, TaskStatuses
from typing import Any, Optional
from django.contrib.auth import get_user_model
from django.core.management import BaseCommand
from django.core.management.base import CommandParser
from django.contrib.auth.hashers import make_password
import faker


class Command(BaseCommand):
    help = "Populate some random data."
    faker = faker.Faker()

    user_model = get_user_model()
    task_model = Task

    def handle(self, *args: Any, **options: Any) -> Optional[str]:
        self.create_staff_users(**options)
        self.create_normal_users(**options)
        self.create_tasks(**options)
        self.set_random_relationships()
        self.stdout.write(
            "Random data sucessfully created.", style_func=self.style.SUCCESS
        )

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("-up", "--user_prefix", default="normal")
        parser.add_argument("-sp", "--staff_prefix", default="staff")
        parser.add_argument("-p", "--password", default="password123")

    def create_staff_users(self, **kwargs):
        password = kwargs.get("password")
        staff_prefix = kwargs.get("staff_prefix")
        staff_users = [
            self.user_model(
                first_name=self.faker.first_name(),
                last_name=self.faker.last_name(),
                is_staff=True,
                username=f"{staff_prefix}_{i}",
                password=make_password(password),
            )
            for i in range(1, 11)
        ]
        self.user_model.objects.bulk_create(staff_users)

    def create_normal_users(self, **kwargs):
        user_prefix = kwargs.get("user_prefix")
        password = kwargs.get("password")
        normal_users = [
            self.user_model(
                first_name=self.faker.first_name(),
                last_name=self.faker.last_name(),
                is_staff=False,
                username=f"{user_prefix}_{i}",
                password=make_password(password),
            )
            for i in range(1, 11)
        ]
        self.user_model.objects.bulk_create(normal_users)

    def create_tasks(self, **kwargs):
        staff_users = self.user_model.objects.filter(is_staff=True)
        normal_users = self.user_model.objects.exclude(is_staff=True, is_superuser=True)
        tasks_choices = TaskStatuses.choices
        tasks = [
            self.task_model(
                reporter=random.choice(staff_users),
                title=f"Task Title {i}",
                content=self.faker.text(),
                status=random.choices(tasks_choices)[0][0],
                assignee=random.choice(normal_users),
            )
            for i in range(20)
        ]
    
        self.task_model.objects.bulk_create(tasks)

    def set_random_relationships(self):
        for task in self.task_model.objects.all():
            assignee_and_reporter_ids = [task.reporter_id, task.assignee_id]
            wathcers = self.user_model.objects.exclude(id__in=assignee_and_reporter_ids).order_by('?')[:2]
            task.watchers.add(*wathcers)
