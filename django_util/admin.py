from typing import List, Set, Tuple, Type

from django_util.constants import complex_fields, related_fields

# Constants used for Django admin configuration
# Defines which fields should be excluded from list display and what filters to apply

# Convert field collections to sets for better performance
related_field_set: Set[Type] = set(related_fields)
complex_field_set: Set[Type] = set(complex_fields)

# Fields to exclude from list_display in admin
list_display_exclude: Tuple[Type, ...] = tuple(related_field_set | complex_field_set)

# Base filters for admin views
list_filter_base: List[str] = ["is_admin_verified"]
list_filter_base_public_contribute: List[str] = list_filter_base + ["is_verified"]
