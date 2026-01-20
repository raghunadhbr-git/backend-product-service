from app import create_app
from app.extensions import db
from app.models.product import Product, ProductVariant

app = create_app()
app.app_context().push()

products = Product.query.all()
count = 0

for p in products:
    if p.color and p.stock is not None:
        exists = ProductVariant.query.filter_by(
            product_id=p.id,
            color=p.color
        ).first()

        if not exists:
            db.session.add(
                ProductVariant(
                    product_id=p.id,
                    color=p.color,
                    stock=p.stock
                )
            )
            count += 1

db.session.commit()
print(f"✅ Migrated {count} variants")


# Run this from the project root with 
# -m scriptyts.migrate_variants 
# means to run the migrate_variants script as a module.
# python -m scripts.migrate_variants
