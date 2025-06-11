import random

from faker import Faker

from comments.models import TopComment, NestedComment, BaseComment


class CommentGenerator:

    def __init__(
            self,
            amount: int,
            frequency: int,
            language: str = 'en_US',
            fake: Faker = None,
    ):
        self.amount = amount
        self.frequency = frequency
        self.fake = fake if fake else Faker(language)
        self.pk_list = list(BaseComment.objects.values_list('pk', flat=True))

    def run(self):
        for i in range(self.amount):
            data = self.data_gen(self.fake)
            if random.random() < self.frequency/10:
                TopComment.objects.create(**data)
            else:
                data.update({'parent_comment_id': random.choice(self.pk_list)})
                obj = NestedComment.objects.create(**data)
                self.pk_list.append(obj.pk)

    @staticmethod
    def data_gen(fake: Faker):
        return {
            'user_name': fake.user_name(),
            'email': fake.email(),
            'home_page': fake.url(),
            'text': fake.text()
        }
