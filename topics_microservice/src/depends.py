from fastapi import Header, HTTPException

# partner_id: int = Header(None)
async def get_current_partner_id() -> int:
    # if partner_id is None:
    #     raise HTTPException(
    #         status_code=401,
    #         detail='Partner ID must be provided',
    #     )

    # return int(partner_id)
    return 2