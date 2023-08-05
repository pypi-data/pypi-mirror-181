"""
An engine that reads messages from the salt event bus and pushes
them onto a Vector endpoint.

:configuration:

    Example configuration

    .. code-block:: yaml

        engines:
          - vector:
              # host_id: myid  # master or minion id override, optional
              address: "127.0.0.1:9000"
              # include_tags:
              #   - "*"
              exclude_tags:
                - salt/auth
                - minion_start
                - minion/refresh/*
                - "[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]"
"""
import fnmatch
import logging
import socket

import salt.utils.event
import salt.utils.json

log = logging.getLogger(__name__)

__virtualname__ = "vector"


def __virtual__():
    return __virtualname__


def _event_bus_context(opts):
    """
    Return Salt event bus context
    """
    if opts["__role"] == "master":
        event_bus = salt.utils.event.get_master_event(opts, opts["sock_dir"], listen=True)
    else:
        event_bus = salt.utils.event.get_event(
            "minion",
            opts=opts,
            sock_dir=opts["sock_dir"],
            listen=True,
        )
    log.debug("Vector engine started")
    return event_bus


def _connect(address):
    """
    Open socket connection
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    addr, port = address.split(":")
    sock.connect((addr, int(port)))
    return sock


def _match_tag(tag, include_tags, exclude_tags):
    """
    Match tag according to include and exclude lists
    """
    if include_tags:
        match = False
        for inc in include_tags:
            if fnmatch.fnmatch(tag, inc):
                match = True
                break
    else:
        match = True

    for exc in exclude_tags:
        if fnmatch.fnmatch(tag, exc):
            match = False
            break

    return match


def start(address, host_id=None, include_tags=None, exclude_tags=None):
    """
    Listen to events and send them to Vector
    """
    if __opts__["__role"] == "master":
        id_key = "master_id"
    else:
        id_key = "minion_id"
    id_value = host_id or __opts__.get("id")

    include_tags = [] if include_tags is None else include_tags
    if not isinstance(include_tags, list):
        raise TypeError("include_tags is not a list")

    exclude_tags = [] if exclude_tags is None else exclude_tags
    if not isinstance(exclude_tags, list):
        raise TypeError("exclude_tags is not a list")

    sock = _connect(address)
    with _event_bus_context(__opts__) as event_bus:
        while True:
            event = event_bus.get_event(full=True)  # get_event_block?
            if event and _match_tag(event["tag"], include_tags, exclude_tags):
                event[id_key] = id_value
                frame = (salt.utils.json.dumps(event) + "\n").encode("utf8")
                try:
                    sock.sendall(frame)
                except OSError:
                    sock = _connect(address)
                    sock.sendall(frame)
