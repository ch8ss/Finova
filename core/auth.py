from core.supabase_client import get_supabase


def sign_up(email: str, password: str, owner_name: str, business_name: str, business_type: str):
    sb = get_supabase()
    try:
        res = sb.auth.sign_up({"email": email, "password": password})
        if not res.user:
            return None, None, "Sign up failed. Try a different email."
        user_id = str(res.user.id)
        sb.table("users").insert({
            "id": user_id,
            "owner_name": owner_name,
            "business_name": business_name,
            "business_type": business_type,
        }).execute()
        return user_id, {"owner_name": owner_name, "business_name": business_name, "business_type": business_type}, None
    except Exception as e:
        return None, None, str(e)


def sign_in(email: str, password: str):
    sb = get_supabase()
    try:
        res = sb.auth.sign_in_with_password({"email": email, "password": password})
        if not res.user:
            return None, None, "Invalid email or password."
        user_id = str(res.user.id)
        profile = sb.table("users").select("owner_name, business_name, business_type").eq("id", user_id).single().execute()
        return user_id, profile.data, None
    except Exception as e:
        return None, None, "Invalid email or password."


def sign_out():
    try:
        get_supabase().auth.sign_out()
    except Exception:
        pass
