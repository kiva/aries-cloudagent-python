from aiohttp import web
from aiohttp.test_utils import AioHTTPTestCase, unittest_run_loop

from ..http import fetch, fetch_stream, FetchError


class TestTransportUtils(AioHTTPTestCase):
    async def setUpAsync(self):
        self.fail_calls = 0
        self.succeed_calls = 0

    async def get_application(self):
        app = web.Application()
        app.add_routes(
            [web.get("/fail", self.fail_route), web.get("/succeed", self.succeed_route)]
        )
        return app

    async def fail_route(self, request):
        self.fail_calls += 1
        raise web.HTTPForbidden()

    async def succeed_route(self, request):
        self.succeed_calls += 1
        ret = web.json_response([True])
        return ret

    @unittest_run_loop
    async def test_fetch_stream(self):
        server_addr = f"http://localhost:{self.server.port}"
        stream = await fetch_stream(
            f"{server_addr}/succeed", session=self.client.session
        )
        result = await stream.read()
        assert result == b"[true]"
        assert self.succeed_calls == 1

    @unittest_run_loop
    async def test_fetch_stream_default_client(self):
        server_addr = f"http://localhost:{self.server.port}"
        stream = await fetch_stream(f"{server_addr}/succeed")
        result = await stream.read()
        assert result == b"[true]"
        assert self.succeed_calls == 1

    @unittest_run_loop
    async def test_fetch_stream_fail(self):
        server_addr = f"http://localhost:{self.server.port}"
        with self.assertRaises(FetchError):
            await fetch_stream(
                f"{server_addr}/fail",
                max_attempts=2,
                interval=0,
                session=self.client.session,
            )
        assert self.fail_calls == 2

    @unittest_run_loop
    async def test_fetch(self):
        server_addr = f"http://localhost:{self.server.port}"
        result = await fetch(
            f"{server_addr}/succeed", session=self.client.session, json=True
        )
        assert result == [1]
        assert self.succeed_calls == 1

    @unittest_run_loop
    async def test_fetch_default_client(self):
        server_addr = f"http://localhost:{self.server.port}"
        result = await fetch(f"{server_addr}/succeed", json=True)
        assert result == [1]
        assert self.succeed_calls == 1

    @unittest_run_loop
    async def test_fetch_fail(self):
        server_addr = f"http://localhost:{self.server.port}"
        with self.assertRaises(FetchError):
            result = await fetch(
                f"{server_addr}/fail",
                max_attempts=2,
                interval=0,
                session=self.client.session,
            )
        assert self.fail_calls == 2
