from typing import AsyncGenerator, Optional

from fastapi import Header, HTTPException, status
from fastapi.param_functions import Depends

from fief.db import AsyncSession, get_account_session
from fief.dependencies.admin_session import get_account_from_admin_session
from fief.dependencies.global_managers import get_account_manager
from fief.errors import APIErrorCode
from fief.managers import AccountManager
from fief.models import Account


async def get_current_account(
    account_admin_session: Optional[Account] = Depends(get_account_from_admin_session),
    host: Optional[str] = Header(None, include_in_schema=False),
    manager: AccountManager = Depends(get_account_manager),
) -> Account:
    if account_admin_session is not None:
        return account_admin_session

    account = None
    if host is not None:
        account = await manager.get_by_domain(host)

    if account is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=APIErrorCode.CANT_DETERMINE_VALID_ACCOUNT,
        )

    return account


async def get_current_account_session(
    account: Account = Depends(get_current_account),
) -> AsyncGenerator[AsyncSession, None]:
    async with get_account_session(account) as session:
        yield session
