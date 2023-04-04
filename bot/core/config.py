import os

_ENV_VAR_PREFIX = "MTATB_"

_debug_mode = os.environ.get(_ENV_VAR_PREFIX + "DEBUG_MODE")
debug_mode = False
if _debug_mode == "true" or _debug_mode == "True":
    debug_mode = True


api_key = os.environ.get(_ENV_VAR_PREFIX + "WOMBO_API_KEY")
if api_key is None:
    print("MTATB_WOMBO_API_KEY not set, exiting...")
    exit(1)

deezer_master_key = os.environ.get(_ENV_VAR_PREFIX + "DEEZER_MASTER_KEY")
if deezer_master_key is None:
    print("MTATB_DEEZER_MASTER_KEY not set, exiting...")
    exit(1)

twitter_api_key = os.environ.get(_ENV_VAR_PREFIX + "TWITTER_API_KEY")
if twitter_api_key is None:
    print("MTATB_TWITTER_API_KEY not set, exiting...")
    exit(1)

twitter_api_secret = os.environ.get(_ENV_VAR_PREFIX + "TWITTER_API_SECRET")
if twitter_api_secret is None:
    print("MTATB_TWITTER_API_SECRET not set, exiting...")
    exit(1)

twitter_access_token = os.environ.get(_ENV_VAR_PREFIX + "TWITTER_ACCESS_TOKEN")
if twitter_access_token is None:
    print("MTATB_TWITTER_ACCESS_TOKEN not set, exiting...")
    exit(1)

twitter_access_token_secret = os.environ.get(
    _ENV_VAR_PREFIX + "TWITTER_ACCESS_TOKEN_SECRET"
)
if twitter_access_token_secret is None:
    print("MTATB_TWITTER_ACCESS_TOKEN_SECRET not set, exiting...")
    exit(1)

wombo_style_id = int(os.environ.get(_ENV_VAR_PREFIX + "WOMBO_STYLE_ID"))
if wombo_style_id is None:
    print("MTATB_WOMBO_STYLE_ID not set, exiting...")
    exit(1)

video_height = os.environ.get(_ENV_VAR_PREFIX + "VIDEO_HEIGHT")
if video_height is None:
    print("MTATB_VIDEO_HEIGHT not set, exiting...")
    exit(1)

video_width = os.environ.get(_ENV_VAR_PREFIX + "VIDEO_WIDTH")
if video_width is None:
    print("MTATB_VIDEO_WIDTH not set, exiting...")
    exit(1)

_openai_api_key = os.environ.get("OPENAI_API_KEY")
if _openai_api_key is None:
    print("OPENAI_API_KEY not set, exiting...")
    exit(1)
