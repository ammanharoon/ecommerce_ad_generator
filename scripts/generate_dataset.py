import pandas as pd
import random
from pathlib import Path

categories = ["Electronics", "Clothing", "Home & Kitchen", "Sports", "Accessories", "Food & Beverage", "Beauty", "Books", "Toys", "Automotive"]

products_data = {
    "Electronics": [
        ("Wireless Bluetooth Headphones", "Premium noise-cancelling headphones with 30-hour battery life and superior sound quality", 79.99),
        ("Smart Fitness Watch", "Track your fitness goals with heart rate monitor, GPS, and sleep tracking", 149.99),
        ("Portable Phone Charger", "20000mAh power bank with fast charging for multiple devices", 39.99),
        ("4K Smart TV 55 inch", "Ultra HD display with HDR support and built-in streaming apps", 599.99),
        ("Wireless Gaming Mouse", "RGB gaming mouse with 16000 DPI and programmable buttons", 49.99),
        ("Bluetooth Speaker Waterproof", "Portable speaker with 360-degree sound and 12-hour battery", 34.99),
        ("USB-C Hub Multi-Port", "7-in-1 adapter with HDMI, USB 3.0, and SD card reader", 29.99),
        ("Mechanical Keyboard RGB", "Cherry MX switches with customizable backlighting", 89.99),
        ("Webcam 1080p HD", "Full HD webcam with autofocus and built-in microphone", 54.99),
        ("Smart Home Security Camera", "WiFi camera with night vision and motion detection", 79.99),
        ("Tablet 10 inch Android", "Octa-core processor with 64GB storage and stylus support", 199.99),
        ("Wireless Earbuds Pro", "Active noise cancellation with transparency mode", 129.99),
        ("Electric Toothbrush Smart", "Sonic technology with app connectivity and pressure sensor", 89.99),
        ("LED Desk Lamp Adjustable", "Touch control with multiple brightness levels and USB charging port", 39.99),
        ("External SSD 1TB", "Portable solid state drive with 1050MB/s read speed", 119.99),
    ],
    "Clothing": [
        ("Organic Cotton T-Shirt", "Comfortable 100% organic cotton t-shirt available in multiple colors", 24.99),
        ("Denim Jeans Slim Fit", "Classic blue jeans with stretch fabric for comfort", 49.99),
        ("Hooded Sweatshirt", "Soft fleece hoodie with kangaroo pocket", 39.99),
        ("Running Shorts Athletic", "Lightweight shorts with moisture-wicking fabric", 29.99),
        ("Winter Jacket Insulated", "Waterproof puffer jacket with removable hood", 99.99),
        ("Polo Shirt Cotton Blend", "Classic polo with embroidered logo", 34.99),
        ("Yoga Pants High Waist", "Stretchy leggings perfect for workouts", 44.99),
        ("Leather Belt Genuine", "Full grain leather belt with metal buckle", 29.99),
        ("Wool Sweater Crewneck", "Soft merino wool sweater for cold weather", 69.99),
        ("Sports Bra Compression", "High support bra for intense workouts", 34.99),
        ("Casual Dress Midi Length", "Flowy dress with floral print pattern", 54.99),
        ("Socks Pack Athletic", "6-pack cushioned socks with arch support", 19.99),
        ("Flannel Shirt Plaid", "Classic flannel button-up shirt", 39.99),
        ("Tank Top Racerback", "Moisture-wicking tank for gym or casual wear", 19.99),
        ("Cardigan Button Front", "Lightweight cardigan sweater with pockets", 44.99),
    ],
    "Home & Kitchen": [
        ("Stainless Steel Water Bottle", "Insulated water bottle keeps drinks cold for 24hrs or hot for 12hrs", 29.99),
        ("Memory Foam Pillow", "Ergonomic pillow with cooling gel technology for better sleep", 49.99),
        ("Non-Stick Cookware Set", "10-piece pots and pans with ceramic coating", 129.99),
        ("Electric Kettle Fast Boil", "1.7L kettle with auto shut-off and boil-dry protection", 34.99),
        ("Bamboo Cutting Board Set", "3-piece cutting board set with juice grooves", 39.99),
        ("Food Storage Containers", "Glass containers with airtight lids - 12 piece set", 44.99),
        ("Vacuum Sealer Machine", "Automatic vacuum sealer for food preservation", 79.99),
        ("Kitchen Knife Set Professional", "8-piece knife set with wooden block", 89.99),
        ("Coffee Maker Programmable", "12-cup coffee maker with auto-brew timer", 69.99),
        ("Air Fryer 6 Quart", "Oil-free air fryer with digital controls", 99.99),
        ("Blender High Speed", "1500W blender for smoothies and food processing", 79.99),
        ("Dish Drying Rack Stainless", "2-tier dish rack with utensil holder", 34.99),
        ("Mixing Bowl Set Nesting", "Stainless steel bowls in 5 sizes", 29.99),
        ("Kitchen Scale Digital", "Precise food scale with tare function", 24.99),
        ("Spice Rack Organizer", "Rotating spice rack with 20 glass jars", 39.99),
    ],
    "Sports": [
        ("Yoga Mat with Carrying Strap", "Non-slip exercise mat perfect for yoga, pilates, and floor workouts", 34.99),
        ("Running Shoes", "Lightweight running shoes with breathable mesh and cushioned sole", 69.99),
        ("Adjustable Dumbbells Set", "Quick-select dumbbells 5-52. 5 lbs with stand", 299.99),
        ("Resistance Bands Set", "5 resistance levels with handles and door anchor", 24.99),
        ("Jump Rope Speed", "Tangle-free jump rope with ball bearings", 14.99),
        ("Foam Roller Massage", "High-density foam roller for muscle recovery", 29.99),
        ("Exercise Ball 65cm", "Anti-burst stability ball with pump", 24.99),
        ("Pull Up Bar Doorway", "No-screw installation chin-up bar", 34.99),
        ("Kettlebell Cast Iron", "Powder-coated kettlebell with wide grip handle - 20 lbs", 39.99),
        ("Ankle Weights Adjustable", "Removable weight pouches up to 10 lbs each", 29.99),
        ("Ab Roller Wheel", "Core exercise wheel with knee pad", 19.99),
        ("Yoga Block Set Cork", "2 yoga blocks for support and balance", 24.99),
        ("Suspension Trainer Straps", "Bodyweight resistance training system", 49.99),
        ("Medicine Ball Slam", "Textured surface medicine ball - 15 lbs", 44.99),
        ("Battle Rope Heavy", "1.5 inch thick workout rope - 30 feet", 59.99),
    ],
    "Accessories": [
        ("Leather Laptop Bag", "Professional leather bag with padded laptop compartment fits up to 15 inch", 89.99),
        ("Sunglasses Polarized UV400", "Classic aviator style with metal frame", 39.99),
        ("Wallet RFID Blocking", "Genuine leather wallet with ID window", 29.99),
        ("Backpack Travel Waterproof", "40L backpack with laptop sleeve and USB port", 59.99),
        ("Watch Band Replacement", "Silicone sport band compatible with smartwatches", 14.99),
        ("Phone Case Protective", "Shockproof case with kickstand function", 19.99),
        ("Keychain Multi-Tool", "Compact tool with knife, screwdriver, bottle opener", 24.99),
        ("Scarf Cashmere Blend", "Soft winter scarf with fringe detail", 34.99),
        ("Hat Baseball Cap", "Adjustable cotton cap with embroidered logo", 19.99),
        ("Gloves Touchscreen Winter", "Warm gloves with conductive fingertips", 24.99),
        ("Tie Silk Business", "Classic necktie with subtle pattern", 29.99),
        ("Handbag Crossbody Leather", "Compact purse with adjustable strap", 79.99),
        ("Belt Buckle Reversible", "Leather belt with dual color options", 34.99),
        ("Jewelry Box Organizer", "Velvet-lined jewelry case with mirror", 44.99),
        ("Umbrella Compact Windproof", "Auto open/close travel umbrella", 29.99),
    ],
    "Food & Beverage": [
        ("Organic Green Tea Set", "Premium organic green tea collection with 6 different flavors", 19.99),
        ("Dark Chocolate Bar Pack", "Artisan chocolate bars 85% cacao - 5 pack", 24.99),
        ("Protein Powder Whey", "Grass-fed whey protein isolate - vanilla flavor 2 lbs", 39.99),
        ("Coffee Beans Whole Bean", "Single origin arabica beans medium roast 1 lb", 16.99),
        ("Extra Virgin Olive Oil", "Cold-pressed EVOO from Greece - 500ml", 29.99),
        ("Honey Raw Organic", "Unfiltered wildflower honey - 16 oz jar", 14.99),
        ("Almond Butter Natural", "Creamy almond butter no added sugar - 16 oz", 12.99),
        ("Granola Clusters Organic", "Gluten-free granola with nuts and seeds", 9.99),
        ("Matcha Powder Ceremonial", "Premium Japanese matcha green tea powder", 24.99),
        ("Coconut Oil Virgin", "Unrefined coconut oil for cooking - 14 oz", 11.99),
        ("Nut Mix Roasted Salted", "Premium mixed nuts cashews, almonds, pecans", 19.99),
        ("Apple Cider Vinegar Organic", "Raw unfiltered ACV with mother - 32 oz", 14.99),
        ("Quinoa Tricolor Organic", "White, red, and black quinoa blend - 2 lbs", 16.99),
        ("Chia Seeds Organic", "Black chia seeds rich in omega-3 - 1 lb", 12.99),
        ("Dried Fruit Medley", "Mixed dried fruits no sugar added - 16 oz", 14.99),
    ],
    "Beauty": [
        ("Face Moisturizer Hyaluronic", "Hydrating facial cream with SPF 30 protection", 29.99),
        ("Vitamin C Serum", "Brightening serum with ferulic acid and vitamin E", 34.99),
        ("Makeup Brush Set Professional", "12-piece brush set with travel case", 44.99),
        ("Hair Dryer Ionic", "1875W dryer with diffuser and concentrator attachments", 49.99),
        ("Facial Cleansing Brush", "Sonic cleansing device with 3 speed settings", 39.99),
        ("Essential Oil Diffuser", "Ultrasonic aromatherapy diffuser with LED lights", 29.99),
        ("Sheet Mask Set Variety", "Hydrating face masks 12-pack different formulas", 24.99),
        ("Nail Polish Set Gel", "6-color gel polish kit with UV lamp", 54.99),
        ("Body Lotion Shea Butter", "Rich moisturizing lotion with vitamin E - 16 oz", 19.99),
        ("Lip Balm Set Natural", "Organic lip balm variety pack - 4 flavors", 12.99),
        ("Eye Cream Anti-Aging", "Peptide eye cream reduces dark circles and puffiness", 39.99),
        ("Facial Roller Jade", "Natural jade stone face roller and gua sha set", 24.99),
        ("Dry Shampoo Spray", "Oil-absorbing dry shampoo for all hair types", 14.99),
        ("Makeup Remover Wipes", "Gentle cleansing wipes for sensitive skin - 60 count", 9.99),
        ("Perfume Roller Essential Oil", "Natural fragrance oil blend - 3 pack", 29.99),
    ],
    "Books": [
        ("Python Programming Guide", "Comprehensive guide to Python for data science and ML", 44.99),
        ("Machine Learning Basics", "Introduction to machine learning algorithms and applications", 39.99),
        ("Deep Learning Handbook", "Advanced neural networks and deep learning techniques", 54.99),
        ("Data Science Cookbook", "Practical recipes for data analysis and visualization", 49.99),
        ("Cloud Computing Essentials", "Guide to AWS, Azure, and Google Cloud Platform", 44.99),
        ("Kubernetes in Action", "Container orchestration for DevOps engineers", 49.99),
        ("Agile Project Management", "Scrum and agile methodologies for software teams", 34.99),
        ("System Design Interview", "Prepare for technical interviews with real scenarios", 39.99),
        ("Clean Code Principles", "Best practices for writing maintainable software", 44.99),
        ("Docker and Microservices", "Build and deploy containerized applications", 49.99),
        ("SQL Query Optimization", "Advanced database performance tuning techniques", 39.99),
        ("React Complete Guide", "Modern web development with React and Redux", 44.99),
        ("Cybersecurity Fundamentals", "Network security and ethical hacking basics", 49.99),
        ("Statistics for Data Analysis", "Statistical methods for machine learning practitioners", 39.99),
        ("Blockchain Technology", "Understanding cryptocurrency and distributed ledgers", 44.99),
    ],
    "Toys": [
        ("Building Blocks Set 1000 Pieces", "Compatible bricks with storage container", 34.99),
        ("Remote Control Car Racing", "High-speed RC car with rechargeable battery", 49.99),
        ("Puzzle 1000 Piece Landscape", "Challenging jigsaw puzzle with vibrant scenery", 24.99),
        ("Educational STEM Kit", "Science experiments for kids ages 8-12", 39.99),
        ("Board Game Strategy", "Family board game for 2-6 players", 29.99),
        ("Stuffed Animal Giant Teddy", "Soft plush bear 3 feet tall", 44.99),
        ("Art Supply Set Kids", "Complete drawing and painting kit with case", 34.99),
        ("Robot Toy Programmable", "Coding robot teaches programming basics", 79.99),
        ("Play-Doh Mega Set", "20-pack of modeling compound with tools", 19.99),
        ("Action Figure Collectible", "Articulated superhero figure with accessories", 24.99),
        ("Dollhouse Wooden 3-Story", "Furnished dollhouse with furniture set", 99.99),
        ("Nerf Blaster Mega", "Foam dart blaster with 10 darts included", 29.99),
        ("Musical Instrument Xylophone", "Colorful xylophone with songbook", 19.99),
        ("Slime Making Kit", "DIY slime supplies with glitter and add-ins", 24.99),
        ("Basketball Hoop Mini", "Over-the-door basketball set with foam ball", 19.99),
    ],
    "Automotive": [
        ("Car Phone Mount Magnetic", "Universal dashboard phone holder with 360-degree rotation", 19.99),
        ("Dash Cam HD 1080p", "Front and rear camera with night vision and loop recording", 89.99),
        ("Tire Pressure Gauge Digital", "Accurate PSI measurement with LED display", 14.99),
        ("Car Vacuum Cleaner Portable", "Cordless handheld vacuum with HEPA filter", 44.99),
        ("Jump Starter Portable Battery", "12V jump starter with USB ports and flashlight", 79.99),
        ("Car Air Freshener Set", "Vent clip air fresheners 10-pack assorted scents", 12.99),
        ("Floor Mats All-Weather", "Heavy-duty rubber floor mats 4-piece set", 39.99),
        ("Seat Covers Universal Fit", "Waterproof seat covers front and back", 49.99),
        ("Windshield Sunshade", "Reflective sun visor protector keeps car cool", 14.99),
        ("Car Charger Dual USB", "Fast charging adapter with 2 USB ports", 9.99),
        ("Trunk Organizer Collapsible", "Storage organizer with multiple compartments", 24.99),
        ("Microfiber Towels Car Detailing", "Ultra-soft cleaning cloths 12-pack", 19.99),
        ("LED Headlight Bulbs", "Super bright H11 LED conversion kit", 54.99),
        ("Emergency Roadside Kit", "Complete safety kit with tools and first aid", 39.99),
        ("Steering Wheel Cover Leather", "Breathable leather wrap with universal fit", 16.99),
    ],
}

def generate_creative_description(product_name, base_desc, category):
    """Generate varied descriptions"""
    templates = [
        f"{base_desc}.  Perfect for daily use and long-lasting durability.",
        f"{base_desc}. Great gift idea for any occasion.",
        f"{base_desc}. Best-seller in the {category} category.",
        f"{base_desc}. Premium quality guaranteed.",
        f"{base_desc}. Customer favorite with 5-star reviews.",
    ]
    return random.choice(templates)

def generate_large_dataset(output_path: str, num_products: int = 200):
    """Generate expanded product dataset"""
    data = []
    product_id = 1
    for _ in range(num_products):
        category = random.choice(categories)
        product_info = random.choice(products_data[category])
        product_name, base_description, base_price = product_info
        description = generate_creative_description(product_name, base_description, category)
        price_variation = random.uniform(0.9, 1.15)
        price = round(base_price * price_variation, 2)
        data.append({
            "product_id": product_id,
            "product_name": product_name,
            "category": category,
            "description": description,
            "price": price
        })
        product_id += 1
    df = pd.DataFrame(data)
    df = df.drop_duplicates(subset=['product_name', 'description'])
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"✅ Generated {len(df)} products")
    print(f"✅ Saved to: {output_path}")
    print(f"\nCategory distribution:")
    print(df['category'].value_counts())
    return df

if __name__ == "__main__":
    generate_large_dataset("data/raw/products.csv", num_products=200)