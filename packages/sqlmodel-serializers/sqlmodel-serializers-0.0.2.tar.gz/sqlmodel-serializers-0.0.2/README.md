# sqlmodel-serializers

DRF like SQLModel serializer which allows us to create valid response schemes and easily add dynamic fields in responses


# Installation

```bash
pip install sqlmodel-serializers
```


# Usage


```python
from sqlmodel_serializers import SQLModelSerializer


from .models import Hero


class HeroUpdate(SQLModelSerializer):
    class Meta:
        model = Hero

        optional = '__all__'

        fields = ('name', 'secret_name', 'age')


class HeroRead(SQLModelSerializer):
    id: int
    full_name: str

    class Meta:
        model = Hero


class HeroCreate(SQLModelSerializer):
    class Meta:
        model = Hero

        fields = ('name', 'secret_name', 'age')
```

Now you can create your routes like this:


```python
from typing import List

from sqlmodel import Session, select
from fastapi import FastAPI, HTTPException, status

from .models import engine, Hero, create_tables
from .serializers import HeroRead, HeroCreate, HeroUpdate


app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_tables(engine)


@app.post("/heroes", response_model=HeroRead)
def create_hero(data: HeroCreate):
    hero = Hero(**data.dict())

    with Session(engine) as session:
        session.add(hero)

        session.commit()

        session.refresh(hero)

        return hero


@app.get("/heroes", response_model=List[HeroRead])
def read_heroes():
    with Session(engine) as session:
        heroes = session.exec(select(Hero)).all()
        return heroes


@app.get('/heroes/pk', response_model=HeroRead)
def retrieve_hero(pk: int):
    with Session(engine) as session:
        instance  = session.get(Hero, pk)

        if not instance:
            raise HTTPException(
                detail='Hero not found',
                status_code=status.HTTP_404_NOT_FOUND
            )

        return instance

@app.patch('/heroes/{pk}', response_model=HeroRead)
def update_hero(pk: int, data: HeroUpdate):
    with Session(engine) as session:
        instance  = session.get(Hero, pk)

        if not instance:
            raise HTTPException(
                detail='Hero not found',
                status_code=status.HTTP_404_NOT_FOUND
            )

        hero_data = data.dict(exclude_unset=True)

        for key, value in hero_data.items():
            setattr(instance, key, value)

        session.add(instance)

        session.commit()

        session.refresh(instance)

        return instance

```

This results in these schemes

![Schemes](https://notabug.org/kapustlo/sqlmodel-serializers/raw/master/images/schemes.webp?raw=true "Schemes")
