import random
from string import ascii_letters
from typing import Optional

from fastapi import APIRouter, Depends, Response, status, HTTPException
from fastapi.responses import Response

from app import schemas
from app.api import depends
from app.database import Database
from app.database.models.order import Order

router = APIRouter()


@router.post("/new",)
async def new_order_item(
    data: schemas.NewOrderItem,
    db: Database = Depends(depends.get_db),
):
    try:
        await db.order_item.new(
            order_fk=data.order_id,
            item_fk=data.item_id,
        )
        await db.session.commit()
        return HTTPException(
            status_code=status.HTTP_201_CREATED,
            detail="Order-Item Added",
        )
    except Exception as ex:
        return HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=ex
        )


@router.get("/get_all_by_order", response_model=Optional[list[schemas.OrderItem]])
async def get_order_items_by_order(
    order_id: int,
    db: Database = Depends(depends.get_db)
):
    if not (order_items := await db.order_item.get_many_by_order(order_fk=order_id)):
        return []
    
    order_item_schemas = []
    for order_item in order_items:
        order = await db.order.get_by_id(id=order_item.order_fk)
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"Order {order_item.order_fk} not found"
            )

        item = await db.item.get_by_id(id=order_item.item_fk)
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"Item {order_item.item_fk} not found"
            )

        order_item_schemas.append(
            schemas.OrderItem(
                id=order_item.id,
                order_id=schemas.Order(
                    id=order.id,
                    client_id=order.client_id,
                    address=order.address,
                    created_at=order.created_at,
                    created_by_microservice_id=order.create_by_microservice_id
                ),
                item_id=schemas.Item(
                    id=item.id,
                    name=item.name,
                    description=item.description
                )
            )
        )
        
    return order_item_schemas

@router.get("/get_all_by_item", response_model=Optional[list[schemas.OrderItem]])
async def get_order_items_by_item(
    item_id: int,
    db: Database = Depends(depends.get_db)
):
    if not (order_items := await db.order_item.get_many_by_item(item_fk=item_id)):
        return []
    
    order_item_schemas = []
    for order_item in order_items:
        print(order_item_schemas)
        order = await db.order.get_by_id(id=order_item.order_fk)
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"Order {order_item.order_fk} not found"
            )

        item = await db.item.get_by_id(id=order_item.item_fk)
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"Item {order_item.item_fk} not found"
            )

        order_item_schemas.append(
            schemas.OrderItem(
                id=order_item.id,
                order_id=schemas.Order(
                    id=order.id,
                    client_id=order.client_id,
                    address=order.address,
                    created_at=order.created_at,
                    created_by_microservice_id=order.create_by_microservice_id
                ),
                item_id=schemas.Item(
                    id=item.id,
                    name=item.name,
                    description=item.description
                )
            )
        )
        
    return order_item_schemas


@router.get("/get_all", response_model=Optional[list[schemas.OrderItem]])
async def get_all(
    db: Database = Depends(depends.get_db)
):
    if not (order_items := await db.order_item.get_all()):
        return []
    print(order_items)
    order_item_schemas = []
    for order_item in order_items:
        order = await db.order.get_by_id(id=order_item.order_fk)
        print(order)
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"Order {order_item.order_fk} not found"
            )

        item = await db.item.get_by_id(id=order_item.item_fk)
        print(item)
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"Item {order_item.item_fk} not found"
            )

        order_item_schemas.append(
            schemas.OrderItem(
                id=order_item.id,
                order_id=schemas.Order(
                    id=order.id,
                    client_id=order.client_id,
                    address=order.address,
                    created_at=order.created_at,
                    created_by_microservice_id=order.create_by_microservice_id
                ),
                item_id=schemas.Item(
                    id=item.id,
                    name=item.name,
                    description=item.description
                )
            )
        )
        
    return order_item_schemas

@router.get("/get", response_model=schemas.OrderItem)
async def get_order_item(
    order_item_id: int,
    db: Database = Depends(depends.get_db)
):
    if not (order_item := await db.order_item.get_by_id(id=order_item_id)):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Not found order-item"
        )
        
    order = await db.order.get_by_id(id=order_item.order_fk)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Order {order_item.order_fk} not found"
        )

    item = await db.item.get_by_id(id=order_item.item_fk)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Item {order_item.item_fk} not found"
        )

    return schemas.OrderItem(
                id=order_item.id,
                order_id=schemas.Order(
                    id=order.id,
                    client_id=order.client_id,
                    address=order.address,
                    created_at=order.created_at,
                    created_by_microservice_id=order.create_by_microservice_id
                ),
                item_id=schemas.Item(
                    id=item.id,
                    name=item.name,
                    description=item.description
                )
            )


# @router.delete("/delete_order")
# async def delete_order(
#     order_id: int,
#     db: Database = Depends(depends.get_db)
# ):
#     if not (order := await db.order.get_by_id(id=order_id)):
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND, detail="Not found orders"
#         )

#     where_clause = [id == order_id]
#     try:
#         await db.order.delete(where_clause)
#         return HTTPException(
#             status_code=status.HTTP_202_ACCEPTED,
#             detail="Order deleted"
#         )
#     except Exception as ex:
#         print(ex)

# @router.delete("/", response_class=Response)
# async def delete_link(
#     link: str,
#     user: dict = Depends(depends.get_user),
#     db: Database = Depends(depends.get_db),
# ):
#     if not (link := await db.link.get_by_link(link)):
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND, detail="Link not found"
#         )
#     if link.user_id != user.get("id"):
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail="You do not have permission to for delete this link",
#         )
#     await db.link.update(link.id, delete=True)
#     await db.session.commit()
#     return Response(status_code=status.HTTP_200_OK, content="link deleted")
# @router.post("/restore", response_class=Response)
# async def restore_link(
#     link: str,
#     user: dict = Depends(depends.get_user),
#     db: Database = Depends(depends.get_db),
# ):
#     if not (link := await db.link.get_by_link(link)):
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND, detail="Link not found"
#         )
#     if link.user_id != user.get("id"):
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail="You do not have permission to for restore this link",
#         )
#     await db.link.update(link.id, delete=False)
#     await db.session.commit()
#     return Response(status_code=status.HTTP_200_OK, content="link restored")
# @router.delete("/autodelete_links/", response_class=Response)
# async def autodelete_links(
#     days: int = 84,
#     _service=Depends(depends.service),
#     db: Database = Depends(depends.get_db),
# ):
#     zero_links = []
#     for link in await db.link.get_many_by_months(days):
#         if not await db.referral.get_many_by_link_fk(link.id):
#             zero_links.append(link)
#     if not zero_links:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND, detail="Link not found"
#         )
#     for link in zero_links:
#         await db.link.update(link.id, delete=True)
#     await db.session.commit()
#     return Response(status_code=status.HTTP_200_OK, content="links deleted")
