from exponent_server_sdk import (
    DeviceNotRegisteredError,
    PushClient,
    PushMessage,
    PushServerError,
    PushTicketError,
)
from requests.exceptions import ConnectionError, HTTPError


# Basic arguments. You should extend this function with the push features you
# want to use, or simply pass in a `PushMessage` object.
def send_push_message(token, title, message, extra):
    try:
        response = PushClient().publish(
            PushMessage(to=token,
                        title=title,
                        body=message,
                        data=extra))
    except PushServerError as exc:
        print(exc)
        raise
    except (ConnectionError, HTTPError) as exc:
        # Encountered some Connection or HTTP error - retry a few times in
        # case it is transient.
        print(exc)
        raise self.retry(exc=exc)

    try:
        # We got a response back, but we don't know whether it's an error yet.
        # This call raises errors so we can handle them with normal exception
        # flows.
        response.validate_response()
    except DeviceNotRegisteredError:
        # DO SOMETHING: Mark the push token as inactive
        # from app_notifications import models 
        pass
    except PushTicketError as exc:
        # Encountered some other per-notification error.
        print(exc)
        raise
