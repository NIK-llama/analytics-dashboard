import os
import random
import sys
from datetime import datetime, timedelta, timezone

from faker import Faker

# Add src to path to import models and session
sys.path.insert(0, os.path.dirname(__file__))

from api.db.session import engine
from api.events.models import EventModel
from api.events.utils import get_location_from_ip
from sqlmodel import Session

fake = Faker()

PAGES = ["/", "/about", "/projects", "/blog", "/contact", "/resume"]
BROWSERS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15",
    "Mozilla/5.0 (Linux; Android 10; SM-G975F) AppleWebKit/537.36",
]

def seed_database(num_events: int = 1000):
    print(f"Seeding {num_events} events into the database...")
    now = datetime.now(timezone.utc)
    
    with Session(engine) as session:
        for i in range(num_events):
            days_ago = random.uniform(0, 90) # Last 90 days
            event_time = now - timedelta(days=days_ago)
            ip = fake.ipv4_public()
            country = fake.country()
            city = fake.city()
            
            event = EventModel(
                time=event_time,
                page=random.choice(PAGES),
                user_agent=random.choice(BROWSERS),
                ip_address=ip,
                referrer=random.choice(["https://google.com", "https://twitter.com", "https://github.com", ""]),
                session_id=fake.uuid4(),
                duration=random.randint(5, 300),
                country=country,
                city=city,
            )
            session.add(event)
            
            if i > 0 and i % 100 == 0:
                session.commit()
                print(f"Inserted {i} events")
                
        session.commit()
        print("Done!")

if __name__ == "__main__":
    seed_database(500)
