from fastapi import APIRouter, Depends, HTTPException # Tools to build the API
from app.db.supabase import supabase # Connection to Supabase
from app.auth.deps import get_current_user # To check if the user is logged in

# Setup the router for health checks
router = APIRouter(prefix="/health", tags=["Health"])


# 1. Check if the database is connected and working
@router.get("/db")
def check_database_connection(user = Depends(get_current_user)):
    try:
        # Step 1: Try to ping the database to see if it responds
        supabase.postgrest.session.get("/").raise_for_status()

        # Step 2: If it works, return a success message
        return {
            "database": "supabase",
            "connected": True,
            "status": "ok"
        }

    except Exception as e:
        # Step 3: If it fails, return an error message
        raise HTTPException(
            status_code=500,
            detail={
                "database": "supabase",
                "connected": False,
                "error": str(e)
            }
        )
