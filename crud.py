import asyncio
from typing import Union, Optional
from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from core.models import db_helper, User, Profile, Post, Order, Product


async def create_user(session: AsyncSession, username: str):
    user = User(username=username)
    session.add(user)
    await session.commit()
    return user


async def create_user_profile(
    session: AsyncSession,
    user_id: int,
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
) -> Profile:
    profile = Profile(
        user_id=user_id,
        first_name=first_name,
        last_name=last_name,
    )
    session.add(profile)
    await session.commit()
    return profile


async def get_user_by_username(
    session: AsyncSession, username: str
) -> Union[User, None]:
    stmt = select(User).where(User.username == username)
    user = await session.scalar(stmt)
    return user


async def show_users_with_profiles(session: AsyncSession):
    stmt = select(User).options(joinedload(User.profile)).order_by(User.id)
    result: Result = await session.execute(stmt)
    users = result.unique().scalars()
    # users = await session.scalars(stmt)
    for user in users.unique().all():
        print(user)
        print(user.profile)


async def create_posts(
    session: AsyncSession,
    user_id: int,
    *post_titles: str,
) -> list[Post]:
    posts = [Post(title=title, user_id=user_id) for title in post_titles]
    session.add_all(posts)
    await session.commit()
    return posts


async def get_users_with_posts(
    session: AsyncSession,
):
    # stmt = select(User).options(joinedload(User.posts)).order_by(User.id)
    stmt = (
        select(User)
        .options(
            # joinedload(User.posts),
            selectinload(User.posts),
        )
        .order_by(User.id)
    )
    # users = await session.scalars(stmt)
    # result: Result = await session.execute(stmt)
    # # users = result.unique().scalars()
    # users = result.scalars()
    users = await session.scalars(stmt)

    # for user in users.unique():  # type: User
    for user in users:  # type: User
        print("**" * 10)
        print(user)
        for post in user.posts:
            print("-", post)


async def create_product(
    session: AsyncSession, name: str, description: str, price: int
) -> Product:
    product = Product(name=name, description=description, price=price)
    session.add(product)
    await session.commit()
    return product


async def create_order(session: AsyncSession, promocode: Optional[str] = None) -> Order:
    order = Order(promocode=promocode)
    session.add(order)
    await session.commit()
    return order


async def create_orders_with_products(session: AsyncSession):
    order_two = await create_order(session=session)
    order_promo = await create_order(session=session, promocode="promo")

    mouse = await create_product(
        session=session,
        name="Mouse",
        description="Great gaming mouse",
        price=149,
    )
    keyboard = await create_product(
        session=session,
        name="Keyboard",
        description="Great gaming keyboard",
        price=177,
    )
    display = await create_product(
        session=session,
        name="Display",
        description="office display",
        price=239,
    )
    order_two = await session.scalar(
        select(Order)
        .where(Order.id == order_two.id)
        .options(
            selectinload(Order.products),
        ),
    )
    order_promo = await session.scalar(
        select(Order)
        .where(Order.id == order_promo.id)
        .options(
            selectinload(Order.products),
        ),
    )
    order_promo.products = [keyboard, display]

    order_two.products.append(mouse)
    # order_promo.products.append(keyboard)

    await session.commit()


async def get_orders_with_products(session: AsyncSession) -> list[Order]:
    stmt = (
        select(Order)
        .options(
            selectinload(Order.products),
        )
        .order_by(Order.id)
    )
    orders = await session.scalars(stmt)
    return list(orders)


async def main_relations(session: AsyncSession):
    pass


async def demo_m2m(session: AsyncSession):
    await create_orders_with_products(session)
    orders = await get_orders_with_products(session)
    for order in orders:
        print(order.id, order.promocode, order.created_at)
        for product in order.products:
            print(product.id, product.name)


async def main():
    async with db_helper.session_factory() as session:
        # await create_user(session=session, username="alice")
        # await create_user(session=session, username="sam")
        # user_sam = await get_user_by_username(session=session, username="sam")
        # user_john = await get_user_by_username(session=session, username="john")
        # user_elis = await get_user_by_username(session=session, username="elis")
        # await create_user_profile(
        #     session=session, user_id=user_sam.id, first_name="John"
        # )
        # await show_users_with_profiles(session=session)
        # await create_posts(
        #     session,
        #     user_john.id,
        #     "SQLA 2.0",
        #     "SQLA Joins",
        # )
        # await create_posts(
        #     session,
        #     user_sam.id,
        #     "FASTAPI 2.0",
        #     "FASTAPI Joins",
        # )
        # await get_users_with_posts(session=session)
        await demo_m2m(session=session)


if __name__ == "__main__":
    asyncio.run(main())
