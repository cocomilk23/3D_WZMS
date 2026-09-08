#!/usr/bin/env python3
"""Small command-line client for Unreal Engine's local MCP server."""

from __future__ import annotations

import argparse
import http.client
import json
import sys
from typing import Any


HOST = "127.0.0.1"
PORT = 8010
PATH = "/mcp"
PROTOCOL_VERSION = "2025-11-25"


def _decode_response(body: str) -> dict[str, Any]:
    body = body.strip()
    if not body:
        return {}
    if body.startswith("{"):
        return json.loads(body)

    messages: list[dict[str, Any]] = []
    for line in body.splitlines():
        if line.startswith("data:"):
            payload = line[5:].strip()
            if payload:
                messages.append(json.loads(payload))
    if not messages:
        raise RuntimeError(f"Unrecognized MCP response: {body[:500]}")
    return messages[-1]


class UnrealMcpClient:
    def __init__(self) -> None:
        self.session_id: str | None = None
        self.protocol_version = PROTOCOL_VERSION
        self._next_id = 1

    def _request(
        self,
        method: str,
        payload: dict[str, Any] | None = None,
    ) -> tuple[int, dict[str, str], dict[str, Any]]:
        # Large editor mutations (dense foliage placement, MetaHuman assembly,
        # packaging preparation) legitimately keep the game thread busy for
        # several minutes.  Keep the transport alive long enough for the
        # official UE MCP call to return its real result instead of abandoning
        # a still-running operation at the former two-minute boundary.
        connection = http.client.HTTPConnection(HOST, PORT, timeout=600)
        headers = {"Accept": "application/json, text/event-stream"}
        if payload is not None:
            headers["Content-Type"] = "application/json"
        if self.session_id:
            headers["Mcp-Session-Id"] = self.session_id
            headers["Mcp-Protocol-Version"] = self.protocol_version
        body = None if payload is None else json.dumps(payload).encode("utf-8")
        connection.request(method, PATH, body=body, headers=headers)
        response = connection.getresponse()
        response_headers = {key.lower(): value for key, value in response.getheaders()}
        if "text/event-stream" in response_headers.get("content-type", ""):
            event_lines: list[str] = []
            while True:
                raw_line = response.readline()
                if not raw_line:
                    break
                line = raw_line.decode("utf-8", "replace")
                if line in ("\n", "\r\n"):
                    if event_lines:
                        break
                    continue
                event_lines.append(line.rstrip("\r\n"))
            response_body = "\n".join(event_lines)
        else:
            response_body = response.read().decode("utf-8", "replace")
        connection.close()
        decoded = _decode_response(response_body) if response_body.strip() else {}
        return response.status, response_headers, decoded

    def connect(self) -> None:
        status, headers, response = self._request(
            "POST",
            {
                "jsonrpc": "2.0",
                "id": self._next_id,
                "method": "initialize",
                "params": {
                    "protocolVersion": PROTOCOL_VERSION,
                    "capabilities": {},
                    "clientInfo": {
                        "name": "wzms-automation",
                        "version": "1.0",
                    },
                },
            },
        )
        self._next_id += 1
        if status != 200:
            raise RuntimeError(f"MCP initialize failed with HTTP {status}")
        self.session_id = headers.get("mcp-session-id")
        if not self.session_id:
            raise RuntimeError("MCP initialize did not return a session id")
        result = response.get("result", {})
        self.protocol_version = result.get("protocolVersion", PROTOCOL_VERSION)
        initialized_status, _, _ = self._request(
            "POST",
            {
                "jsonrpc": "2.0",
                "method": "notifications/initialized",
                "params": {},
            },
        )
        if initialized_status != 202:
            raise RuntimeError(
                f"MCP initialized notification failed with HTTP {initialized_status}"
            )

    def close(self) -> None:
        if self.session_id:
            try:
                self._request("DELETE")
            finally:
                self.session_id = None

    def rpc(self, method: str, params: dict[str, Any]) -> dict[str, Any]:
        status, _, response = self._request(
            "POST",
            {
                "jsonrpc": "2.0",
                "id": self._next_id,
                "method": method,
                "params": params,
            },
        )
        self._next_id += 1
        if status != 200:
            raise RuntimeError(f"MCP request failed with HTTP {status}: {response}")
        if "error" in response:
            raise RuntimeError(json.dumps(response["error"], ensure_ascii=False))
        return response.get("result", {})

    def call_meta(self, name: str, arguments: dict[str, Any]) -> Any:
        result = self.rpc(
            "tools/call",
            {"name": name, "arguments": arguments},
        )
        if result.get("isError"):
            raise RuntimeError(json.dumps(result, ensure_ascii=False))
        content = result.get("content", [])
        if not content:
            return None
        text = content[0].get("text")
        if text is None:
            return content
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            return text


def _parse_arguments(raw: str | None) -> dict[str, Any]:
    if not raw:
        return {}
    value = json.loads(raw)
    if not isinstance(value, dict):
        raise ValueError("Tool arguments must be a JSON object")
    return value


def main() -> int:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("list")

    describe_parser = subparsers.add_parser("describe")
    describe_parser.add_argument("toolset")
    describe_parser.add_argument("--filter", default="")

    call_parser = subparsers.add_parser("call")
    call_parser.add_argument("toolset")
    call_parser.add_argument("tool")
    call_parser.add_argument("--arguments", default="{}")

    args = parser.parse_args()
    client = UnrealMcpClient()
    try:
        client.connect()
        if args.command == "list":
            result = client.call_meta("list_toolsets", {})
        elif args.command == "describe":
            result = client.call_meta(
                "describe_toolset",
                {"toolset_name": args.toolset},
            )
            if args.filter and isinstance(result, dict):
                needle = args.filter.casefold()
                result = {
                    **{key: value for key, value in result.items() if key != "tools"},
                    "tools": [
                        tool
                        for tool in result.get("tools", [])
                        if needle in tool.get("name", "").casefold()
                    ],
                }
        else:
            result = client.call_meta(
                "call_tool",
                {
                    "toolset_name": args.toolset,
                    "tool_name": args.tool,
                    "arguments": _parse_arguments(args.arguments),
                },
            )
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except Exception as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1
    finally:
        client.close()


if __name__ == "__main__":
    raise SystemExit(main())
