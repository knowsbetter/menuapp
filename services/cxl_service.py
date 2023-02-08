from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from menuapp import cache, config, crud, models, schemes
from menuapp.database import SessionLocal, engine


async def get_db():
    """Returns database session"""
    async with SessionLocal() as db:
        yield db


class CxlService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_test_menu(self, password: schemes.Password):
        if password.password == config.SPECIAL_PASSWORD:
            async with engine.begin() as conn:
                await conn.run_sync(models.Base.metadata.drop_all)
                await conn.run_sync(models.Base.metadata.create_all)
            await crud.FillMenu.fill(db=self.session)
            return {"status": True, "message": "Success"}
        else:
            return None

    async def create_excel_file(self):
        task_id = await crud.CreateXL.create_xl(db=self.session)
        await cache.set_cache(f"celery{task_id}", task_id)
        return {"task_id": task_id}


def get_cxl_service(session: AsyncSession = Depends(get_db)):
    return CxlService(session)
