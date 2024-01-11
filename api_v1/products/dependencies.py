from fastapi import Depends, HTTPException, Path, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Union, Annotated
from api_v1.products import crud
from core.models import db_helper, Product


async def get_product_by_id(
    product_id: Annotated[int, Path],
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> Union[Product, None]:
    product = await crud.get_product(
        session=session,
        product_id=product_id,
    )
    if product:
        return product
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Product with {product_id} not found",
    )
