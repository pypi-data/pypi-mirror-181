import base64
import datetime
import json
import os
from typing import Optional, List
from unittest import mock
from unittest.mock import MagicMock, call, patch
import jwt
import pytest
import requests
from flask import Response, request, Blueprint
from werkzeug.datastructures import EnvironHeaders

from ..authentication.middleware import (
    HEADER_MODIFIER, RESPONSE_MODIFIER,
    UNAUTHORIZED_MODIFIER, EXCEPTION_MODIFIER,
    ServiceMiddleware
)
from ..authentication import auth
from ..providers.oidc_provider import public
from .conftest import mock_middleware_server, aud, key


class TestMiddleware:

    def test_wsgi_middleware_calls_expected_route_returns_http_status_200(self, disconnected_middleware_client, benchmark):
        payload = {
            "aud": aud,
            "some": "payload",
            "name": "Joseph",
            "email": "joseph@ihsmarkit.com",
            "datalake": {"organisation_id": "1111-1111-1111-1111"},
        }
        jw = jwt.encode(payload=payload, key=key, algorithm="HS256")

        # route that is hard coded to return 200
        @benchmark
        def response() -> Response: return disconnected_middleware_client.get("/", headers={"Authorization": f"Bearer {jw}"})
        assert response.status_code == 200
        assert response.data == b'HELLO, WORLD'

    def test_wsgi_middleware_calls_expected_route_returns_http_status_403(self, disconnected_middleware_client, benchmark):
        payload = {
            "aud": aud,
            "some": "payload",
            "name": "Joseph",
            "email": "joseph@ihsmarkit.com",
            "datalake": {"organisation_id": "1111-1111-1111-1111"},
        }
        jw = jwt.encode(payload=payload, key=key, algorithm="HS256")

        # direct_route that is hard coded to return 403
        @benchmark
        def response() -> Response: return disconnected_middleware_client.get("/direct_test", headers={"Authorization": f"Bearer {jw}"})
        assert response.status_code == 403
        assert response.data == b'BE GONE, DRAGON'

    def test_wsgi_middleware_calls_injected_header_modifier(self, disconnected_middleware_client, benchmark):
        # check that once we attach them, they are called

        payload = {
            "aud": aud,
            "some": "payload",
            "name": "Joseph",
            "email": "joseph@ihsmarkit.com",
            "datalake": {"organisation_id": "1111-1111-1111-1111"},
        }
        jw = jwt.encode(payload=payload, key=key, algorithm="HS256")
        header_modifier = MagicMock()
        header_modifier.side_effect = lambda jwt, env: env
        disconnected_middleware_client.application.injector.binder.bind(
            HEADER_MODIFIER,
            to=lambda: header_modifier,
            scope=request,
        )

        @benchmark
        def response() -> Response: return disconnected_middleware_client.get("/", headers={"Authorization": f"Bearer {jw}", "Another-Header": "findme"})
        header_modifier.assert_called()
        # argument list should be position[0] = jwt, position[1] = original headers (+ http/wsgi)
        header_modifier.assert_has_calls([
           call(jw, mock.ANY)
        ])
        # lets inspect those headers, make sure we have the one we passed
        recovered_headers_from_call_argument = header_modifier.call_args_list[0].args[1]
        assert "HTTP_ANOTHER_HEADER" in recovered_headers_from_call_argument
        # and that we popped the ones we didnt want already in middleware
        assert "HTTP_AUTHORIZATION" not in recovered_headers_from_call_argument
        assert "HTTP_HOST" not in recovered_headers_from_call_argument

    def test_wsgi_middleware_calls_injected_response_modifier(self, disconnected_middleware_client, benchmark):
        # check that once we attach them, they are called

        payload = {
            "aud": aud,
            "some": "payload",
            "name": "Joseph",
            "email": "joseph@ihsmarkit.com",
            "datalake": {"organisation_id": "1111-1111-1111-1111"},
        }
        jw = jwt.encode(payload=payload, key=key, algorithm="HS256")
        ground_zero = disconnected_middleware_client.get("/", headers={"Authorization": f"Bearer {jw}"})

        response_modifier = MagicMock()
        response_modifier.side_effect = lambda response: ("goodbye world", 403, {})
        disconnected_middleware_client.application.injector.binder.bind(
            RESPONSE_MODIFIER,
            to=lambda: response_modifier,
        )

        @benchmark
        def response() -> Response: return disconnected_middleware_client.get("/", headers={"Authorization": f"Bearer {jw}"})

        class ResponseAny():
            def __eq__(self, other):
                return type(other) == requests.models.Response

        response_modifier.assert_called()
        response_modifier.assert_has_calls([
            call(ResponseAny())
        ])

        # check our responsemodifier has overwritten the response vis-a-vis calling without
        assert response.data == b"goodbye world"
        assert response.status_code == 403
        assert ground_zero.status_code != response.status_code

    def test_wsgi_middleware_calls_injected_unauthorized_modifier(self, disconnected_middleware_client, benchmark):
        # check that once we attach them, they are called

        jw = "ladeedahdeedah"  # this will trigger an Unauthorized error

        def unauth(init, code, header, reason):
            init("403 Unauthorized", [("Content-Type", "text/xml")])
            return f"<xml>{reason}</xml>"

        disconnected_middleware_client.application.injector.binder.bind(
            UNAUTHORIZED_MODIFIER,
            to=lambda: unauth,
        )

        @benchmark
        def response() -> Response: return disconnected_middleware_client.get("/", headers={"Authorization": f"Bearer {jw}"})

        assert response.status_code == 403
        assert response.content_type == "text/xml"
        assert response.data.decode() == '<xml>Not enough segments</xml>'

    def test_wsgi_middleware_calls_injected_exception_modifier(self, disconnected_middleware_client, benchmark):
        # check that once we attach them, they are called

        payload = {
            "aud": aud,
            "some": "payload",
            "name": "Joseph",
            "email": "joseph@ihsmarkit.com",
            "datalake": {"organisation_id": "1111-1111-1111-1111"},
        }
        jw = jwt.encode(payload=payload, key=key, algorithm="HS256")

        def exception(init, code, header, exception):
            init(code, header)
            return f"<xml>{str(exception)}</xml>"

        def response_from_app():
            views = Blueprint('middleware', __name__)
            HTTP_METHODS = ['GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'CONNECT', 'OPTIONS', 'TRACE', 'PATCH']

            @views.route(
                '/',
                methods=HTTP_METHODS
            )
            def test_route(optional_path: Optional[str] = None):

                raise Exception()

            mock_response_app = mock_middleware_server(views)
            with mock_response_app.test_client() as client:
                return client

        disconnected_middleware_client = response_from_app()
        disconnected_middleware_client.application.injector.binder.bind(
            RESPONSE_MODIFIER,
            to=lambda: Exception(),   # bad modifier triggers our middleware to blow up
        )
        disconnected_middleware_client.application.injector.binder.bind(
            EXCEPTION_MODIFIER,
            to=lambda: exception,
        )

        @benchmark
        def response() -> Response: return disconnected_middleware_client.get("/", headers={"Authorization": f"Bearer {jw}"})

        assert response.status_code == 500
        assert response.content_type == "text/html"
        assert response.data.decode() == "<xml>'Exception' object is not callable</xml>"

    def test_wsgi_middleware_injectors_called_before_and_after_route(self, benchmark):
        # timing - we can check that within the route, the headers have been added/changed prior to route
        payload = {
            "aud": aud,
            "some": "payload",
            "name": "Joseph",
            "email": "joseph@ihsmarkit.com",
            "datalake": {"organisation_id": "1111-1111-1111-1111"},
        }
        jw = jwt.encode(payload=payload, key=key, algorithm="HS256")
        header_mod_called = None
        view_called = None
        response_mod_called = None

        def timing_header(jwt, env):
            nonlocal header_mod_called
            header_mod_called = datetime.datetime.now()
            return env

        def timing_response(response):
            nonlocal response_mod_called
            # assert we've not changed the response yet
            response_mod_called = datetime.datetime.now()
            return "goodbye world", 403, {}

        def timing_app():
            views = Blueprint('middleware', __name__)
            HTTP_METHODS = ['GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'CONNECT', 'OPTIONS', 'TRACE', 'PATCH']

            @views.route(
                '/',
                methods=HTTP_METHODS
            )
            def test_route(optional_path: Optional[str] = None):
                nonlocal view_called
                view_called = datetime.datetime.now()

                resp = MagicMock()
                resp.status_code = 200
                resp.headers = {}
                resp.content = "HELLO, WORLD"
                return resp.content, resp.status_code, resp.headers.items()

            timing_app = mock_middleware_server(views)
            with timing_app.test_client() as client:
                return client

        disconnected_middleware_client = timing_app()

        header_modifier = MagicMock()
        header_modifier.side_effect = timing_header
        disconnected_middleware_client.application.injector.binder.bind(
            HEADER_MODIFIER,
            to=lambda: header_modifier,
            scope=request,
        )
        response_modifier = MagicMock()
        response_modifier.side_effect = timing_response
        disconnected_middleware_client.application.injector.binder.bind(
            RESPONSE_MODIFIER,
            to=lambda: response_modifier,
        )

        @benchmark
        def response() -> Response: return disconnected_middleware_client.get("/", headers={"Authorization": f"Bearer {jw}"})

        assert header_mod_called < view_called < response_mod_called

    @staticmethod
    def __setup_payload_and_jwt():
        payload = {
            "aud": aud,
            "some": "payload",
            "name": "Joseph",
            "email": "joseph@ihsmarkit.com",
            "datalake": {"organisation_id": "1111-1111-1111-1111"},
        }
        jw = jwt.encode(payload=payload, key=key, algorithm="HS256")
        return payload, jw

    # underscores are flipped to dashes in the wsgi container, HTTP_ prefix is dropped.
    # so additional headers may not use "_"
    # i.e. HTTP_X_SOURCE = X-Source
    additional_headers = {
        "X-Additional-Header1": "tag",
        "X-Source": "middleware",
        "X-Source-User": "<JWT>",
        "Cache-Control": "no-cache",
        "Connection": 'keep-alive',
        "Content-Type": "application/json"
    }

    intercepted_headers: EnvironHeaders

    def __setup_wsgi_modifies_headers_correctly(self):

        # NOTE ignore Pycharm suggestion about name shadowing, this name MUST match `jwt` for the lambda to work.
        def __mod_header(jwt, env):
            new_headers = env.copy()

            # some kind of exchange has already taken place to get us a JWT from our creds in the params
            # so we place that into the bearer

            dd = {"HTTP_AUTHORIZATION": f"Bearer {jwt}"}

            # must be prefixed HTTP_ else won't end up in the middleware headers provided to the route
            # this way we also preserve the dash "-" which would otherwise be converted to underscore "_"
            # use 'HACK' of : dict([x for x in request.headers]) to read these back out without werkzeug throwing a fit
            for k, v in self.additional_headers.items():
                if v == "<JWT>":
                    dd["HTTP_" + k] = jwt
                else:
                    dd["HTTP_" + k] = v

            new_headers.update(dd)

            return new_headers

        def __inspect_header_app():
            views = Blueprint('middleware', __name__)
            HTTP_METHODS = ['GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'CONNECT', 'OPTIONS', 'TRACE', 'PATCH']

            @views.route(
                '/',
                methods=HTTP_METHODS
            )
            def test_route(optional_path: Optional[str] = None):
                # inspect the headers here to check they are already transformed as we would need to
                # make a request from here to an EP.
                self.intercepted_headers = request.headers

                def session():
                    return requests.Session()

                resp = MagicMock()
                resp.status_code = 200
                resp.headers = {}
                resp.content = "HELLO, WORLD"

                session()

                return resp.content, resp.status_code, resp.headers.items()

            inspect_app = mock_middleware_server(views)
            with inspect_app.test_client() as client:
                return client

        disconnected_middleware_client = __inspect_header_app()
        disconnected_middleware_client.application.injector.binder.bind(
            HEADER_MODIFIER,
            to=lambda: __mod_header,
            scope=request,
        )
        return disconnected_middleware_client

    def test_wsgi_modifies_headers_correctly_before_route_for_auth_type_ldap(self, disconnected_middleware_client, benchmark):
        # correctness - that the headers required are changed

        # here we will devise any incoming auth header should be intercepted and resolved by the time
        # we are in the view (be already transformed to custom auth header format)

        # example - our real endpoint only takes Authorisation: Bearer <TOKEN>, but our middleware we enter User:Pass
        #   we want to transform the Authorisation header into that form by exchanging the User:Pass -> Token prior
        #   to it arriving in the route which sends it onto the endpoint

        payload, jw = self.__setup_payload_and_jwt()

        # basic auth is going to go down this exchange to get the JWT passed to our header modifier func
        # pat auth is going to go down this exchange to get the JWT passed to our header modifier func
        with patch.object(auth, '_sam_app_flow', return_value=jw) as mock_app_flow, \
                patch.object(auth, '_sam_pat_flow', return_value=jw) as mock_pat_flow:

            disconnected_middleware_client = self.__setup_wsgi_modifies_headers_correctly()

            # the LDAP/Presto case for PAT or APP cases
            user_pass = base64.urlsafe_b64encode(b"<app_user>:<app_pasw>").decode("ascii")

            @benchmark
            def response() -> Response: return disconnected_middleware_client.get("/", headers={"Authorization": f"Basic {user_pass}"})

            assert self.intercepted_headers["Authorization"] == f"Bearer {jw}"

            # we also add some additional headers, that we wanted to pass along to the service for each request.
            # lets check those were added in mod_header (again, recall they are not going to be prefixed HTTP_ inside
            # of the wsgi container), i.e. "HTTP_something" in fn: mod_header == "something" in flask view

            dict_of_modded_headers = dict([x for x in self.intercepted_headers])
            for k, v in self.additional_headers.items():
                assert k in dict_of_modded_headers
                assert dict_of_modded_headers[k] == (v if not v == "<JWT>" else jw)

    def test_wsgi_modifies_headers_correctly_before_route_for_auth_type_jwt(self, disconnected_middleware_client, benchmark):
        # correctness - that the headers required are changed

        # here we will devise any incoming auth header should be intercepted and resolved by the time
        # we are in the view (be already transformed to custom auth header format)

        # example - our real endpoint only takes Authorisation: Bearer <TOKEN>, but our middleware we enter User:Pass
        #   we want to transform the Authorisation header into that form by exchanging the User:Pass -> Token prior
        #   to it arriving in the route which sends it onto the endpoint

        payload, jw = self.__setup_payload_and_jwt()

        # basic auth is going to go down this exchange to get the JWT passed to our header modifier func
        # pat auth is going to go down this exchange to get the JWT passed to our header modifier func
        with patch.object(auth, '_sam_app_flow', return_value=jw) as mock_app_flow, \
                patch.object(auth, '_sam_pat_flow', return_value=jw) as mock_pat_flow:

            disconnected_middleware_client = self.__setup_wsgi_modifies_headers_correctly()

            # the SDK case for Presto, passing JWT, ends up as the Identity function
            @benchmark
            def response() -> Response: return disconnected_middleware_client.get("/", headers={"Authorization": f"Bearer {jw}"})

            assert self.intercepted_headers["Authorization"] == f"Bearer {jw}"

            # we also add some additional headers, that we wanted to pass along to the service for each request.
            # lets check those were added in mod_header (again, recall they are not going to be prefixed HTTP_ inside
            # of the wsgi container), i.e. "HTTP_something" in fn: mod_header == "something" in flask view

            dict_of_modded_headers = dict([x for x in self.intercepted_headers])
            for k, v in self.additional_headers.items():
                assert k in dict_of_modded_headers
                assert dict_of_modded_headers[k] == (v if not v == "<JWT>" else jw)

    def test_wsgi_modifies_headers_correctly_before_route_for_auth_type_sig(self, disconnected_middleware_client, benchmark):
        # correctness - that the headers required are changed

        # here we will devise any incoming auth header should be intercepted and resolved by the time
        # we are in the view (be already transformed to custom auth header format)

        # example - our real endpoint only takes Authorisation: Bearer <TOKEN>, but our middleware we enter User:Pass
        #   we want to transform the Authorisation header into that form by exchanging the User:Pass -> Token prior
        #   to it arriving in the route which sends it onto the endpoint

        payload, jw = self.__setup_payload_and_jwt()

        # basic auth is going to go down this exchange to get the JWT passed to our header modifier func
        # pat auth is going to go down this exchange to get the JWT passed to our header modifier func
        with patch.object(auth, '_sam_app_flow', return_value=jw) as mock_app_flow, \
                patch.object(auth, '_sam_pat_flow', return_value=jw) as mock_pat_flow:

            disconnected_middleware_client = self.__setup_wsgi_modifies_headers_correctly()

            # the PAT or APP case, passing delimited user/pass secrets in the signature via Spark/Boto/tools (S3Proxy)
            sig = ("Credential=<app_user>\\<app_pasw>/<date>/<region>/<aws_service>/aws4_request, "
                   "SignedHeaders=amz-sdk-invocation-id;amz-sdk-retry;content-type;host;user-agent;x-amz-content-sha256;x-amz-date, "
                   "Signature=<calc_signature>")

            @benchmark
            def response() -> Response: return disconnected_middleware_client.get("/", headers={"Authorization": f"AWS4-HMAC-SHA256 {sig}"})

            assert self.intercepted_headers["Authorization"] == f"Bearer {jw}"

            # we also add some additional headers, that we wanted to pass along to the service for each request.
            # lets check those were added in mod_header (again, recall they are not going to be prefixed HTTP_ inside
            # of the wsgi container), i.e. "HTTP_something" in fn: mod_header == "something" in flask view

            dict_of_modded_headers = dict([x for x in self.intercepted_headers])
            for k, v in self.additional_headers.items():
                assert k in dict_of_modded_headers
                assert dict_of_modded_headers[k] == (v if not v == "<JWT>" else jw)

    def test_wsgi_modifies_headers_correctly_before_route_for_auth_type_rest(self, disconnected_middleware_client, benchmark):
        # correctness - that the headers required are changed

        # here we will devise any incoming auth header should be intercepted and resolved by the time
        # we are in the view (be already transformed to custom auth header format)

        # example - our real endpoint only takes Authorisation: Bearer <TOKEN>, but our middleware we enter User:Pass
        #   we want to transform the Authorisation header into that form by exchanging the User:Pass -> Token prior
        #   to it arriving in the route which sends it onto the endpoint

        payload, jw = self.__setup_payload_and_jwt()

        # basic auth is going to go down this exchange to get the JWT passed to our header modifier func
        # pat auth is going to go down this exchange to get the JWT passed to our header modifier func
        with patch.object(auth, '_sam_app_flow', return_value=jw) as mock_app_flow, \
                patch.object(auth, '_sam_pat_flow', return_value=jw) as mock_pat_flow:

            disconnected_middleware_client = self.__setup_wsgi_modifies_headers_correctly()

            # the SDK case for S3Proxy, passing JWT in the signature via boto (S3Proxy)
            sig2 = (f"Credential={jw}/<date>/<region>/<aws_service>/aws4_request, "
                    "SignedHeaders=amz-sdk-invocation-id;amz-sdk-retry;content-type;host;user-agent;x-amz-content-sha256;x-amz-date, "
                    "Signature=<calc_signature>")

            @benchmark
            def response() -> Response: return disconnected_middleware_client.get("/", headers={"Authorization": f"AWS4-HMAC-SHA256 {sig2}"})

            assert self.intercepted_headers["Authorization"] == f"Bearer {jw}"

            # we also add some additional headers, that we wanted to pass along to the service for each request.
            # lets check those were added in mod_header (again, recall they are not going to be prefixed HTTP_ inside
            # of the wsgi container), i.e. "HTTP_something" in fn: mod_header == "something" in flask view

            dict_of_modded_headers = dict([x for x in self.intercepted_headers])
            for k, v in self.additional_headers.items():
                assert k in dict_of_modded_headers
                assert dict_of_modded_headers[k] == (v if not v == "<JWT>" else jw)

    @pytest.mark.xfail
    def test_all_headers_data_sent_to_proxied_service(self, disconnected_middleware_client):
        # TBC - there isnt really a test for this, since its the app's responsibility in the view to decide
        # this is just to notate how to use those pesky headers that we hacked

        '''
            headers = dict([x for x in request.headers])  # headers back to dict to allow header[X] use in view
            resp = getattr(requests, request.method.lower())(upstream_service, headers=headers, data=request.data)
        '''

    def test_wsgi_modifies_response_correctly_after_route(self, disconnected_middleware_client, benchmark):
        # correctness - that the content/headers are modified how we want

        # here we will devise any outgoing response should be intercepted and
        # transformed before sending to client. Lets imagine our service gives a json response with
        # `follow` urls in the json for the client to make the consequent request.

        # We need to modify those `follow` urls to redirect the consequent request via the middleware rather than
        # directly back towards the service (which may not be visible to them, nor permit their auth).

        os.environ['JWT_SECRET_KEY'] = key
        os.environ['JWT_AUDIENCE'] = aud
        payload = {
            "aud": aud,
            "some": "payload",
            "name": "Joseph",
            "email": "joseph@ihsmarkit.com",
            "datalake": {"organisation_id": "1111-1111-1111-1111"},
        }

        # The client should then receive this modified response instead.
        jw = jwt.encode(payload=payload, key=key, algorithm="HS256")

        def mod_response(response):
            content = response.content
            a = json.loads(content)
            a["nextUri"] = a["nextUri"].replace("my-service", "my-middleware")
            a["inspectUri"] = a["inspectUri"].replace("my-service", "my-middleware")
            return json.dumps(a), response.status_code, response.headers.items()

        def response_from_app():
            views = Blueprint('middleware', __name__)
            HTTP_METHODS = ['GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'CONNECT', 'OPTIONS', 'TRACE', 'PATCH']

            @views.route(
                '/',
                methods=HTTP_METHODS
            )
            def test_route(optional_path: Optional[str] = None):

                resp = MagicMock()
                resp.status_code = 200
                resp.headers = {}

                json_body = {
                    "nextUri" : "http://my-service/1234",
                    "inspectUri": "http://my-service/inspect/1234?slug=vi54nvg65",
                }

                resp.content = json.dumps(json_body)

                return resp.content, resp.status_code, resp.headers.items()

            mock_response_app = mock_middleware_server(views)
            with mock_response_app.test_client() as client:
                return client

        # skip auth (patch before app)
        with patch.object(ServiceMiddleware, '_resolve', return_value=jw) as mock_method:

            disconnected_middleware_client = response_from_app()
            disconnected_middleware_client.application.injector.binder.bind(
                RESPONSE_MODIFIER,
                to=lambda: mod_response,
                scope=request,
            )

            @benchmark
            def response() -> Response: return disconnected_middleware_client.get("/", headers={"Authorization": f"Basic anything"})

            _json = json.loads(response.data)
            assert _json["nextUri"] == "http://my-middleware/1234"
            assert _json["inspectUri"] == "http://my-middleware/inspect/1234?slug=vi54nvg65"

    @pytest.mark.xfail # TODO
    def test_wsgi_respond_from_bad_reply_from_proxied_service(self, disconnected_middleware_client):
        # correctness - that say a 403/500 from the service is sent back through correctly
        pass

    @pytest.mark.xfail # TODO
    def test_public_route_allowed(self, disconnected_middleware_client):
        # correctness - any public routes will be trapped behind auth of the middleware, unless handled
        def public_app():
            views = Blueprint('middleware', __name__)
            HTTP_METHODS = ['GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'CONNECT', 'OPTIONS', 'TRACE', 'PATCH']

            @views.route(
                '/',
                methods=HTTP_METHODS
            )
            @public
            def test_route(optional_path: Optional[str] = None):

                resp = MagicMock()
                resp.status_code = 200
                resp.headers = {}

                json_body = {
                    "nextUri" : "http://my-service/1234",
                    "inspectUri": "http://my-service/inspect/1234?slug=vi54nvg65"
                }

                resp.content = json.dumps(json_body)

                return resp.content, resp.status_code, resp.headers.items()

            mock_response_app = mock_middleware_server(views)
            with mock_response_app.test_client() as client:
                return client

        disconnected_middleware_client = public_app()
        resp = disconnected_middleware_client.get("/")
        assert resp.status_code == 200