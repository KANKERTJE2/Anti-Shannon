import re
import random
from starlette.requests import Request
import logging

logger = logging.getLogger("wukong.honeyforms")

class HoneyFieldManager:
    """
    The Lure: Manages hidden fields in forms to trap automated bots.
    """
    def __init__(self):
        self.trap_fields = ["_admin_confirm", "secret_token", "verification_bypass", "internal_debug_id"]
        # CSS to hide the fields from humans but keep them in the DOM for bots
        self.hide_style = 'style="display:none !important; visibility:hidden !important; position:absolute !important; left:-9999px !important;"'

    def inject_traps(self, html: bytes) -> bytes:
        """
        Injects a hidden field into every <form> found in the HTML.
        """
        try:
            content = html.decode("utf-8")
        except UnicodeDecodeError:
            return html

        def add_trap(match):
            form_tag = match.group(0)
            token = random.choice(self.trap_fields)
            trap = f'\n<input type="text" name="{token}" value="" {self.hide_style} tabindex="-1" autocomplete="off">\n'
            return form_tag + trap

        # Regex to find <form ...> tags
        new_content = re.sub(r'<form[^>]*>', add_trap, content, flags=re.IGNORECASE)
        return new_content.encode("utf-8")

    async def is_triggered(self, request: Request) -> bool:
        """
        Checks if any of the trap fields are present in the form data.
        Only applies to POST requests.
        """
        if request.method != "POST":
            return False

        try:
            form_data = await request.form()
            for field in self.trap_fields:
                if form_data.get(field):
                    logger.critical(f"🍭 HONEY-FIELD TRIGGERED: Field '{field}' was filled!")
                    return True
        except Exception:
            pass
            
        return False
