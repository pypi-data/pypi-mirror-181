"""mse_lib_sgx.global module."""

import threading
from typing import Optional

CODE_SYM_KEY: Optional[bytes] = None

EXIT_EVENT: threading.Event = threading.Event()

UUID: Optional[str] = None

SSL_PRIVATE_KEY: Optional[str] = None
NEED_SSL_PRIVATE_KEY: bool = False
