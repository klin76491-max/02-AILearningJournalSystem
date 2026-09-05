from django.db import transaction
from django.contrib.auth.models import User
from .models import MentalInventoryItem


class MentalInventoryService:
    @classmethod
    def save_bulk_inventory(cls, user: User, doing_text: str, should_text: str, want_text: str) -> int:
        items_to_create = []

        def process_lines(text, inv_type):
            for line in text.splitlines():
                line = line.strip().lstrip('•*- 1234567890. ')
                if line:
                    items_to_create.append(MentalInventoryItem(
                        user=user,
                        inventory_type=inv_type,
                        content=line[:250],
                        test_status=MentalInventoryItem.TestStatus.PENDING
                    ))

        process_lines(doing_text, MentalInventoryItem.InventoryType.DOING)
        process_lines(should_text, MentalInventoryItem.InventoryType.SHOULD_DO)
        process_lines(want_text, MentalInventoryItem.InventoryType.WANT_TO_DO)

        with transaction.atomic():
            created = MentalInventoryItem.objects.bulk_create(items_to_create)

        return len(created)

    @classmethod
    def sift_item(cls, user: User, item_id: int, test_status: str, category: str = 'none') -> bool:
        try:
            item = MentalInventoryItem.objects.get(id=item_id, user=user)
            item.test_status = test_status
            if category in MentalInventoryItem.Category.values:
                item.category = category
            item.save(update_fields=['test_status', 'category', 'updated_at'])
            return True
        except MentalInventoryItem.DoesNotExist:
            return False

    @classmethod
    def toggle_focus(cls, user: User, item_id: int) -> bool:
        try:
            item = MentalInventoryItem.objects.get(id=item_id, user=user)
            item.is_focus = not item.is_focus
            if item.is_focus:
                item.test_status = MentalInventoryItem.TestStatus.KEPT
                if item.category == MentalInventoryItem.Category.NONE:
                    item.category = MentalInventoryItem.Category.GOAL
            item.save(update_fields=['is_focus', 'test_status', 'category', 'updated_at'])
            return True
        except MentalInventoryItem.DoesNotExist:
            return False

    @classmethod
    def get_inventory_summary(cls, user: User) -> dict:
        items = MentalInventoryItem.objects.filter(user=user)
        doing_items = items.filter(inventory_type=MentalInventoryItem.InventoryType.DOING)
        should_items = items.filter(inventory_type=MentalInventoryItem.InventoryType.SHOULD_DO)
        want_items = items.filter(inventory_type=MentalInventoryItem.InventoryType.WANT_TO_DO)

        focus_items = items.filter(is_focus=True)
        kept_items = items.filter(test_status=MentalInventoryItem.TestStatus.KEPT)
        discarded_items = items.filter(test_status=MentalInventoryItem.TestStatus.DISCARDED)
        pending_items = items.filter(test_status=MentalInventoryItem.TestStatus.PENDING)

        return {
            'total_count': items.count(),
            'doing_items': doing_items,
            'should_items': should_items,
            'want_items': want_items,
            'focus_items': focus_items,
            'kept_items': kept_items,
            'discarded_items': discarded_items,
            'pending_items': pending_items,
            'has_completed_wizard': (items.count() > 0 and pending_items.count() == 0 and focus_items.count() > 0)
        }
