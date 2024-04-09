import random
from string import ascii_letters

from fastapi import APIRouter, Depends, Response, status, HTTPException
from fastapi.responses import Response

from app import schemas
from app.api import depends
from app.database import Database
from app.database.models.order import Order

router = APIRouter()


@router.post("/new",)
async def new_item(
    data: schemas.NewItem,
    db: Database = Depends(depends.get_db),
):
    try:
        await db.item.new(
            name=data.name,
            description=data.description,
        )
        await db.session.commit()
        return HTTPException(
            status_code=status.HTTP_201_CREATED,
            detail="Item added",
        )
    except Exception as ex:
        return HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=ex
        )


@router.get("/get_items", response_model=list[schemas.Item])
async def get_items(
    db: Database = Depends(depends.get_db)
):
    if not (items := await db.item.get_many()):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Not found orders"
        )
    item_schemas = []
    for item in items:
        item_schemas.append(
            schemas.Item(
                id=item.id,
                name=item.name,
                address=item.description,
            )
        )
    return item_schemas


@router.get("/get", response_model=schemas.Item)
async def get_item(
    item_id: int,
    db: Database = Depends(depends.get_db)
):
    if not (item := await db.item.get_by_id(id=item_id)):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Not found orders"
        )

    return schemas.Item(
        id=item.id,
        name=item.name,
        address=item.description,
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
