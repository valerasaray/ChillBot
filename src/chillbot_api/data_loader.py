import argparse
import asyncio
import csv
from pathlib import Path

from services.config.config import DatabaseConfig
from services.postgres.repositories.postgres_place_repository import PostgresPlaceRepository
from services.postgres.session import PostgresSession


async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--csv-file', type=str, help='Path to csv file')
    
    args = parser.parse_args()
    
    csv_file = Path(args.csv_file)
    
    if not csv_file.exists():
        raise FileNotFoundError(f'CSV file not found: {csv_file}')
    
    config = DatabaseConfig(
        host='localhost',
        port=5433,
        user='postgres',
        password='postgres',
        database='chillbot'
    )
    session = await PostgresSession(config).create()
    
    async with session() as s:
        repository = PostgresPlaceRepository(s)
        with csv_file.open(encoding='utf-8') as f:
            reader = csv.DictReader(f)

            for row in reader:
                name = row.get('name')
                category = row.get('category')
                city = row.get('city')

                if not name or not category or not city:
                    continue

                await repository.create(
                    name=name.strip(),
                    category=category.strip(),
                    city=city.strip()
                )


if __name__ == '__main__':
    asyncio.run(main())
    