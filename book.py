import sqlalchemy
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from class_shoop import *
import json

Base = declarative_base()



DSN = "postgresql://postgres:postgres@localhost:5432/shoop"
engine = sqlalchemy.create_engine(DSN)
create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()


with open('tests_data.json', 'r') as fd:
    data = json.load(fd)

for record in data:
    model = {
        'publisher': Publisher,
        'shop': Shop,
        'book': Book,
        'stock': Stock,
        'sale': Sale,}[record.get('model')]
    session.add(model(id=record.get('pk'), **record.get('fields')))
session.commit()


for s in session.query(Publisher).all():
    print(f'ID {s.name} = {s.id}')

i=input("Введите идентификатор издателя:")

q = session.query(Book).join(Publisher.books).filter(Publisher.id == i)
for s in q.all():
    h = session.query(Stock).join(Book.stock).filter(Stock.id_book==s.id)
    for r in h.all():
        t = session.query(Shop).join(Stock).join(Sale).filter(Sale.id_stock==r.id)
        for w in t.all():
            k = session.query(Sale).join(Stock.sale).filter(Sale.id_stock==r.id)          
            for l in k.all():

                    print(f'{s.title} | {w.name} | {l.price} | {l.date_sale}')

    

session.close()
