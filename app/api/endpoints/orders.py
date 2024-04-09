import random
from string import ascii_letters

from fastapi import APIRouter, Depends, Response, status, HTTPException
from fastapi.responses import Response
from asyncpg import exceptions
from app import schemas
from app.api import depends
from app.database import Database
from app.database.models.order import Order

router = APIRouter()


@router.post("/new",)
async def new_order(
    data: schemas.NewOrder,
    db: Database = Depends(depends.get_db),
):
    try:
        order = await db.order.new(
            client_id=data.client_id,
            address=data.address,
            created_at=data.created_at,
            created_by_microservice_id="Not developed",
        )
        await db.session.commit()
        return HTTPException(
            status_code=status.HTTP_201_CREATED,
            detail="Order added",
        )
    except Exception as ex:
        return HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=ex
        )


@router.get("/get_orders", response_model=list[schemas.Order])
async def get_orders(
    client_id: int,
    db: Database = Depends(depends.get_db)
):
    if not (orders := await db.order.get_many_by_client(client_id=client_id)):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Not found orders"
        )
    order_schemas = []
    for order in orders:
        order_schemas.append(
            schemas.Order(
                id=order.id,
                client_id=order.client_id,
                address=order.address,
                created_at=order.created_at,
                created_by_microservice_id=order.create_by_microservice_id,
            )
        )
    return order_schemas


@router.get("/get", response_model=schemas.Order)
async def get_order(
    order_id: int,
    db: Database = Depends(depends.get_db)
):
    if not (order := await db.order.get_by_id(id=order_id)):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Not found orders"
        )

    return schemas.Order(
        id=order.id,
        client_id=order.client_id,
        address=order.address,
        created_at=order.created_at,
        created_by_microservice_id=order.create_by_microservice_id,
    )


@router.delete("/delete_order")
async def delete_order(
    order_id: int,
    db: Database = Depends(depends.get_db)
):
    if not (order := await db.order.get_by_id(id=order_id)):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Not found orders"
        )
    
    
    try:
        await db.order.delete(order_id)
        return HTTPException(
            status_code=status.HTTP_202_ACCEPTED,
            detail="Order deleted"
        )
    except exceptions.ForeignKeyViolationError as ex:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Нельзя удалить. На данный Order всё ещё есть ссылки в таблице OrderItem"
        )
    except Exception as ex:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=ex.__str__
        )

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
