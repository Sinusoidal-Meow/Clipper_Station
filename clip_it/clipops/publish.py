"""YouTube and Instagram publishing via official APIs."""

import json
import base64
from pathlib import Path
from typing import Optional, Dict, Any

from clipops.config import settings, get_brand_config
from clipops.db import get_db, init_db


def encrypt_token(plaintext: str) -> str:
    """Encrypt a token using the encryption key (simplified)."""
    key = settings.TOKEN_ENCRYPTION_KEY
    if not key:
        return plaintext
    # Simple XOR encryption - NOT for production use
    key_bytes = key.encode() if isinstance(key, str) else key
    plain_bytes = plaintext.encode()
    encrypted = bytes(b ^ key_bytes[i % len(key_bytes)] for i, b in enumerate(plain_bytes))
    return base64.b64encode(encrypted).decode()


def decrypt_token(encrypted: str) -> str:
    """Decrypt a stored token."""
    key = settings.TOKEN_ENCRYPTION_KEY
    if not key:
        return encrypted
    key_bytes = key.encode() if isinstance(key, str) else key
    encrypted_bytes = base64.b64decode(encrypted.encode())
    decrypted = bytes(b ^ key_bytes[i % len(key_bytes)] for i, b in enumerate(encrypted_bytes))
    return decrypted.decode()


def connect_youtube(brand: str, label: str = "YouTube channel") -> bool:
    """Initiate OAuth flow for YouTube. Returns True when connected."""
    from google_auth_oauthlib.flow import Flow
    from googleapiclient.discovery import build
    import webbrowser
    import tempfile

    if not settings.YOUTUBE_CLIENT_ID or not settings.YOUTUBE_CLIENT_SECRET:
        print("[publish] Missing YOUTUBE_CLIENT_ID or YOUTUBE_CLIENT_SECRET in .env")
        return False

    scopes = ["https://www.googleapis.com/auth/youtube.upload",
              "https://www.googleapis.com/auth/yt-analytics.readonly"]

    flow = Flow.from_client_config(
        {"web": {
            "client_id": settings.YOUTUBE_CLIENT_ID,
            "client_secret": settings.YOUTUBE_CLIENT_SECRET,
            "redirect_uris": ["http://localhost:8080/callback"]
        }},
        scopes=scopes
    )

    auth_url, _ = flow.authorization_url(prompt='consent')
    print(f"[publish] Open this URL in browser to authorize YouTube for brand '{brand}':")
    print(auth_url)
    print("After authorizing, paste the authorization code here: ", end="")

    code = input().strip()
    try:
        flow.fetch_token(code=code)
        creds = flow.credentials
        token_data = creds.to_json()
        encrypted = encrypt_token(token_data)

        conn = get_db()
        with conn:
            conn.execute(
                "INSERT OR REPLACE INTO connected_accounts (id, platform, brand, label, encrypted_token, created_at) VALUES (?, ?, ?, ?, ?, ?)",
                (f"youtube_{brand}", "youtube", brand, label, encrypted, "now()")
            )
        conn.close()
        print(f"[publish] YouTube connected for brand '{brand}'")
        return True
    except Exception as e:
        print(f"[publish] OAuth error: {e}")
        return False


def upload_clip(file_path: str, brand: str, title: str, description: str,
                tags: list, scheduled: bool = False) -> Optional[str]:
    """Upload clip to YouTube using the connected account."""
    if not settings.PUBLISH_ENABLED:
        print("[publish] Publishing disabled. Set CLIPOPS_PUBLISH_ENABLED=1")
        return None

    from googleapiclient.discovery import build
    from google.oauth2.credentials import Credentials

    conn = get_db()
    row = conn.execute(
        "SELECT encrypted_token FROM connected_accounts WHERE platform='youtube' AND brand=?",
        (brand,)
    ).fetchone()
    conn.close()

    if not row:
        print(f"[publish] No YouTube account connected for brand '{brand}'")
        return None

    creds = Credentials.from_authorized_user_info(json.loads(decrypt_token(row[0])))
    youtube = build("youtube", "v3", credentials=creds)

    request_body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": tags,
            "categoryId": "20",
        },
        "status": {
            "privacyStatus": "private" if not scheduled else "private",
            "publishAt": None
        }
    }

    try:
        from googleapiclient.http import MediaFileUpload
        media = MediaFileUpload(file_path, chunksize=-1, resumable=True, mimetype="video/mp4")
        response = youtube.videos().insert(body=request_body, media_body=media, part="snippet,status").execute()
        video_id = response.get("id")
        print(f"[publish] Uploaded: https://youtube.com/watch?v={video_id}")
        return video_id
    except Exception as e:
        print(f"[publish] Upload failed: {e}")
        return None