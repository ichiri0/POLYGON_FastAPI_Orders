import random
from string import ascii_letters

from fastapi import APIRouter, Depends, Response, status, HTTPException

from app import schemas
from app.api import depends
from app.database import Database

router = APIRouter()


async def generate_link(db: Database) -> str:
    link = "".join(random.choices(ascii_letters, k=10))
    if await db.link.get_by_link(link):
        return await generate_link(db)
    return link


@router.post("/", response_model=schemas.GetLink)
async def new_link(
    data: schemas.NewLink,
    user: dict = Depends(depends.get_user),
    db: Database = Depends(depends.get_db),
):
    user_id = user.get("id")
    link = await generate_link(db)
    link = await db.link.new(user_id=user_id, link=link, comment=data.comment)
    await db.session.commit()
    return schemas.GetLink(
        link=link.link, comment=link.comment, referral_counts=0
    )


@router.get("/", response_model=list[schemas.GetLink])
async def get_links(
    user: dict = Depends(depends.get_user), db: Database = Depends(depends.get_db)
):
    if not (links := await db.link.get_many_by_user(user.get("id"))):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Not found links"
        )
    links_schemas = []
    for link in links:
        tariffs_paid = 0
        if not link.delete:
            referrals = await db.referral.get_many_by_link_fk(link.id)
            for referral in referrals:
                if referral.tariff_paid:
                    tariffs_paid += 1
            links_schemas.append(
                schemas.GetLink(
                    link=link.link,
                    comment=link.comment,
                    tariffs_paid=tariffs_paid,
                    referrals_count=len(referrals),
                )
            )
    return links_schemas


@router.delete("/", response_class=Response)
async def delete_link(
    link: str,
    user: dict = Depends(depends.get_user),
    db: Database = Depends(depends.get_db),
):
    if not (link := await db.link.get_by_link(link)):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Link not found"
        )
    if link.user_id != user.get("id"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to for delete this link",
        )
    await db.link.update(link.id, delete=True)
    await db.session.commit()
    return Response(status_code=status.HTTP_200_OK, content="link deleted")


@router.post("/restore", response_class=Response)
async def restore_link(
    link: str,
    user: dict = Depends(depends.get_user),
    db: Database = Depends(depends.get_db),
):
    if not (link := await db.link.get_by_link(link)):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Link not found"
        )
    if link.user_id != user.get("id"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to for restore this link",
        )
    await db.link.update(link.id, delete=False)
    await db.session.commit()
    return Response(status_code=status.HTTP_200_OK, content="link restored")


@router.delete("/autodelete_links/", response_class=Response)
async def autodelete_links(
    days: int = 84,
    _service=Depends(depends.service),
    db: Database = Depends(depends.get_db),
):
    zero_links = []
    for link in await db.link.get_many_by_months(days):
        if not await db.referral.get_many_by_link_fk(link.id):
            zero_links.append(link)
    if not zero_links:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Link not found"
        )
    for link in zero_links:
        await db.link.update(link.id, delete=True)
    await db.session.commit()
    return Response(status_code=status.HTTP_200_OK, content="links deleted")
