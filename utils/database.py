# Direct imports from db.py to avoid redundancy
from db import (
    get_user_products,
    get_deleted_products, 
    add_product,
    update_product,
    delete_product,
    restore_product
)

# All functions are now directly available from db.py
# No need for wrapper functions since db.py already has them