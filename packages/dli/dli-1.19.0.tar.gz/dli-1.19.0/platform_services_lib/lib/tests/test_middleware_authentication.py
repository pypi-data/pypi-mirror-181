import base64
import uuid
from typing import Optional, List
from unittest.mock import MagicMock, patch

import hypothesis
import hypothesis.strategies as st
import pytest
import jwt

from requests import Response

from ..context.environments import _Environment
from ..authentication.middleware import ServiceMiddleware
from ..authentication.auth import _sam_app_flow, _sam_pat_flow, _pre_request_get_token, decode_token, Unauthorized
from ..authentication import auth

from .conftest import disconnected_middleware_client
from ..services.view_exceptions import InternalServerError, BadRequest, Forbidden

_ = disconnected_middleware_client  # stop import being marked as unused (fixture is used everywhere below)


class TestMiddlewareAuthentication:

    def test_no_auth(self, benchmark, disconnected_middleware_client):
        @benchmark
        def func(): return disconnected_middleware_client.get("/test")
        assert func.status_code == 401
        assert func.data.decode() == ServiceMiddleware.MSG_NOT_AUTHORIZED

    def test_unrecognized_auth(self, benchmark, disconnected_middleware_client):
        @benchmark
        def func(): return disconnected_middleware_client.get("/test", headers={"Authorization": "Random XXXXX"})
        assert func.status_code == 401
        assert func.data.decode() == ServiceMiddleware.MSG_NOT_AUTHORIZED

    def test_unrecognized_jwt_decode(self, benchmark, disconnected_middleware_client):
        @benchmark
        def func(): return disconnected_middleware_client.get("/test", headers={"Authorization": "Bearer JWT"})
        assert func.status_code == 401
        assert func.data.decode() == ServiceMiddleware.MSG_NOT_AUTHORIZED

    def test_recognized_jwt_hits_backend(self, benchmark, disconnected_middleware_client):
        payload = {
            "aud": 'aud',
            "some": "payload",
            "name": "Joseph",
            "email": "joseph@ihsmarkit.com",
            "datalake": {"organisation_id": "1111-1111-1111-1111"},
        }
        jw = jwt.encode(payload=payload, key="secret", algorithm="HS256")

        @benchmark
        def func(): return disconnected_middleware_client.get("/test", headers={"Authorization": f"Bearer {jw}"})
        assert func.status_code == 200
        assert func.data.decode() == "HELLO, WORLD"

    def test_resolver_is_called(self, benchmark, disconnected_middleware_client):
        with patch.object(ServiceMiddleware, '_resolve', return_value=MagicMock()) as mock_method:
            jw = jwt.encode(payload={"some": "payload"}, key="secret", algorithm="HS256")
            @benchmark
            def func(): return disconnected_middleware_client.get("/test", headers={"Authorization": f"Bearer {jw}"})
            mock_method.assert_called()

    def test_resolver_calls_correct_method_for_auth_type_jwt(self, benchmark, disconnected_middleware_client):
        # make all the caller methods magicmocks
        jw = jwt.encode(payload={"<jwt_user>": "payload"}, key="secret", algorithm="HS256")

        with patch.object(ServiceMiddleware, '_type_bearer', return_value=(jw, "NOP", "JWT")) as _bearer,\
             patch.object(ServiceMiddleware, '_type_ldap', return_value=("app_user", "app_pasw", None)) as _ldap,\
             patch.object(ServiceMiddleware, '_type_s3_rest', return_value=("app_user", "app_pass", None)) as _rest,\
             patch.object(ServiceMiddleware, '_type_v4_signature', return_value=("app_user", "app_pass", None)) as _sig,\
             patch.object(ServiceMiddleware, '_credentials_to_token', return_value=MagicMock()
        ):
            def func(): return disconnected_middleware_client.get("/test", headers={"Authorization": f"Bearer {jw}"})
            func()
            # check only this one was called
            assert _bearer.call_count == 1
            assert _ldap.call_count == 0
            assert _sig.call_count == 0
            assert _rest.call_count == 0
            # check we called it how we expected
            _bearer.assert_called_with("\\", jw)

            benchmark(func)

    def test_resolver_calls_correct_method_for_auth_type_ldap(self, benchmark, disconnected_middleware_client):

        # make all the caller methods magicmocks
        jw = jwt.encode(payload={"<jwt_user>": "payload"}, key="secret", algorithm="HS256")

        with patch.object(ServiceMiddleware, '_type_bearer', return_value=(jw, "NOP", "JWT")) as _bearer,\
             patch.object(ServiceMiddleware, '_type_ldap', return_value=("app_user", "app_pasw", None)) as _ldap,\
             patch.object(ServiceMiddleware, '_type_s3_rest', return_value=("app_user", "app_pass", None)) as _rest,\
             patch.object(ServiceMiddleware, '_type_v4_signature', return_value=("app_user", "app_pass", None)) as _sig,\
             patch.object(ServiceMiddleware, '_credentials_to_token', return_value=MagicMock()
        ):
            ldap = base64.urlsafe_b64encode(b"<app_user>:<app_pasw>")
            def func(): return disconnected_middleware_client.get("/test", headers={"Authorization": f"Basic {ldap}"})
            func()
            # check only this one was called
            assert _bearer.call_count == 0
            assert _ldap.call_count == 1
            assert _sig.call_count == 0
            assert _rest.call_count == 0
            _ldap.assert_called_with("\\", str(ldap))

            benchmark(func)

    def test_resolver_calls_correct_method_for_auth_type_rest(self, benchmark, disconnected_middleware_client):

        # make all the caller methods magicmocks
        jw = jwt.encode(payload={"<jwt_user>": "payload"}, key="secret", algorithm="HS256")

        with patch.object(ServiceMiddleware, '_type_bearer', return_value=(jw, "NOP", "JWT")) as _bearer,\
             patch.object(ServiceMiddleware, '_type_ldap', return_value=("app_user", "app_pasw", None)) as _ldap,\
             patch.object(ServiceMiddleware, '_type_s3_rest', return_value=("app_user", "app_pass", None)) as _rest,\
             patch.object(ServiceMiddleware, '_type_v4_signature', return_value=("app_user", "app_pass", None)) as _sig,\
             patch.object(ServiceMiddleware, '_credentials_to_token', return_value=MagicMock()
        ):
            # https://docs.aws.amazon.com/AmazonS3/latest/userguide/RESTAuthentication.html
            rest ="<app_user\\app_pasw>:<signature>"
            @benchmark
            def func(): return disconnected_middleware_client.get("/test", headers={"Authorization": f"AWS {rest}"})
            _rest.assert_called_with("\\", rest)

    def test_resolver_calls_correct_method_for_auth_type_sig(self, benchmark, disconnected_middleware_client):
        # make all the caller methods magicmocks
        jw = jwt.encode(payload={"<jwt_user>": "payload"}, key="secret", algorithm="HS256")

        with patch.object(ServiceMiddleware, '_type_bearer', return_value=(jw, "NOP", "JWT")) as _bearer,\
             patch.object(ServiceMiddleware, '_type_ldap', return_value=("app_user", "app_pasw", None)) as _ldap,\
             patch.object(ServiceMiddleware, '_type_s3_rest', return_value=("app_user", "app_pass", None)) as _rest,\
             patch.object(ServiceMiddleware, '_type_v4_signature', return_value=("app_user", "app_pass", None)) as _sig,\
             patch.object(ServiceMiddleware, '_credentials_to_token', return_value=MagicMock()
        ):
            # https://docs.aws.amazon.com/general/latest/gr/sigv4-signed-request-examples.html
            sig = ("Credential=<app_user\\app_pasw>/<date>/<region>/<aws_service>/aws4_request, "
                "SignedHeaders=amz-sdk-invocation-id;amz-sdk-retry;content-type;host;user-agent;x-amz-content-sha256;x-amz-date, "
                "Signature=<calc_signature>")

            @benchmark
            def func(): return disconnected_middleware_client.get("/test", headers={"Authorization": f"AWS4-HMAC-SHA256 {sig}"})
            _sig.assert_called_with("\\", sig)

    def test_split_jwt_credentials_colon_case_present(self, benchmark):
        @benchmark
        def func(): return ServiceMiddleware._split_to_jwt_or_credentials(auth_credential_delimiter=":", field_aws_access_key_id="user:password")
        assert func == ("user", "password", None)

    def test_split_jwt_credentials_backslash_case_present(self, benchmark):
        @benchmark
        def func(): return ServiceMiddleware._split_to_jwt_or_credentials(auth_credential_delimiter="\\", field_aws_access_key_id="user\\password")
        assert func == ("user", "password", None)

    def test_split_jwt_credentials_divider_missing(self, benchmark):
        JWT = "jwt005"
        @benchmark
        def func(): return ServiceMiddleware._split_to_jwt_or_credentials(auth_credential_delimiter="\\", field_aws_access_key_id=JWT)
        assert func == (JWT, "NOP", "JWT")

    def test_split_jwt_credentials_divider_in_password(self, benchmark):
        # we have confirmed the relevant divider cannot be present in: the user+header auth (CC - [A-Za-z0-9], or PAT - [UUID])
        # we have confirmed the relevant divider "\\" is not/cannot be present in the SAM PAT password (thus the choice)
        @benchmark
        def func(): return ServiceMiddleware._split_to_jwt_or_credentials(auth_credential_delimiter="\\", field_aws_access_key_id="user\\pass\\w\\ord")
        assert func == ("user", "pass\\w\\ord", None)

    def test_type_ldap(self, benchmark):
        ldap = base64.urlsafe_b64encode(b"<app_user>:<app_pasw>")
        @benchmark
        def func(): return ServiceMiddleware._type_ldap("\\", ldap)
        assert func == ("<app_user>", "<app_pasw>", None)

    def test_type_bearer(self, benchmark):
        jw = jwt.encode(payload={"some": "payload"}, key="secret", algorithm="HS256")
        @benchmark
        def func(): return ServiceMiddleware._type_bearer("\\", jw)
        assert func == (jw, "NOP", "JWT")

    def test_type_s3_rest(self, benchmark):
        rest ="<app_user>\\<app_pasw>:<signature>"
        @benchmark
        def func(): return ServiceMiddleware._type_s3_rest("\\", rest)
        assert func == ("<app_user>", "<app_pasw>", None)

    def test_type_v4_signature(self, benchmark):
        sig = ("Credential=<app_user>\\<app_pasw>/<date>/<region>/<aws_service>/aws4_request, "
               "SignedHeaders=amz-sdk-invocation-id;amz-sdk-retry;content-type;host;user-agent;x-amz-content-sha256;"
               "x-amz-date, Signature=<calc_signature>")
        @benchmark
        def func(): return ServiceMiddleware._type_v4_signature("\\", sig)
        assert func == ("<app_user>", "<app_pasw>", None)

    def test_sam_app_flow(self, benchmark):
        # we aren't going overboard with testing on this method, since it will move to catalogue
        env = _Environment("https://catalogue-dev.udpmarkit.net")

        session = MagicMock()
        catalogue_response = Response()
        catalogue_response._content = b'{"access_token": "<JWT3>"}'
        catalogue_response.headers.update({})
        catalogue_response.status_code = 200

        session.post.return_value = catalogue_response

        @benchmark
        def func(): return _sam_app_flow(env, "user", "pasw", external_session=session)

        assert func == "<JWT3>"

    def test_sam_pat_flow(self, benchmark):
        # we aren't going overboard with testing on this method, since it will move to catalogue
        env = _Environment("https://catalogue-dev.udpmarkit.net")

        # with patch.object(auth, 'external_session', return_value=resp) as response:
        session = MagicMock()
        catalogue_response = Response()
        catalogue_response._content = b'{"access_token": "<JWT3>"}'
        catalogue_response.headers.update({})
        catalogue_response.status_code = 200

        session.post.return_value = catalogue_response

        @benchmark
        def func(): return _sam_pat_flow(env, "user", "pasw", external_session=session)

        assert func == "<JWT3>"

    def test_decode_token_good_token(self, benchmark):
        good_jwt = jwt.encode(payload={"some": "payload"}, key="secret", algorithm="HS256")
        @benchmark
        def func(): return decode_token(good_jwt)
        assert func == {"some": "payload"}

    def test_decode_token_bad_token(self, benchmark):
        bad_jwt = "not_a_jwt"
        @benchmark
        def func():
            with pytest.raises(Exception) as execinfo:
                decode_token(bad_jwt)

    def test_pre_request_get_token_hinted_PAT_case_and_provided_PAT(self, benchmark):
        env = _Environment("https://catalogue-dev.udpmarkit.net")

        with patch.object(auth, '_sam_pat_flow', return_value=MagicMock()) as patflow:
            with patch.object(auth, '_sam_app_flow', return_value=MagicMock()) as appflow:
                with patch.object(auth, 'decode_token', return_value=MagicMock()) as decodetoken:
                    # hinted PAT case, and provided PAT
                    @benchmark
                    def func(): return _pre_request_get_token(env, str(uuid.uuid4()), "<pass>", "PAT", external_session=MagicMock())
                    patflow.assert_called()

    def test_pre_request_get_token_hinted_PAT_case_and_not_provided_PAT(self, benchmark):
        env = _Environment("https://catalogue-dev.udpmarkit.net")

        with patch.object(auth, '_sam_pat_flow', return_value=MagicMock()) as patflow:
            with patch.object(auth, '_sam_app_flow', return_value=MagicMock()) as appflow:
                with patch.object(auth, 'decode_token', return_value=MagicMock()) as decodetoken:
                    # hinted PAT case, and not provided PAT
                    @benchmark
                    def func():
                        with pytest.raises(ValueError) as execinfo:
                            _pre_request_get_token(env, "APP_USER", "<pass>", "PAT", external_session=MagicMock())

    def test_pre_request_get_token_hinted_JWT_case_and_provided_JWT(self, benchmark):
        env = _Environment("https://catalogue-dev.udpmarkit.net")

        with patch.object(auth, '_sam_pat_flow', return_value=MagicMock()) as patflow:
            with patch.object(auth, '_sam_app_flow', return_value=MagicMock()) as appflow:
                with patch.object(auth, 'decode_token', return_value=MagicMock()) as decodetoken:
                    # hinted JWT case and provided JWT
                    jw = jwt.encode(payload={"some": "payload"}, key="secret", algorithm="HS256")
                    @benchmark
                    def func(): return _pre_request_get_token(env, str(jw), "<pass>", "JWT", external_session=MagicMock())
                    decodetoken.assert_called()

    def test_pre_request_get_token_hinted_JWT_case_and_not_provided_JWT(self, benchmark):
        env = _Environment("https://catalogue-dev.udpmarkit.net")

        with patch.object(auth, '_sam_pat_flow', return_value=MagicMock()) as patflow:
            with patch.object(auth, '_sam_app_flow', return_value=MagicMock()) as appflow:
                # hinted JWT case and not provided JWT
                @benchmark
                def func():
                    with pytest.raises(jwt.DecodeError) as execinfo:
                        _pre_request_get_token(env, str(uuid.uuid4()), "<pass>", "JWT", external_session=MagicMock())

    def test_pre_request_get_token_hinted_APP_case_and_provided_APP(self, benchmark):
        env = _Environment("https://catalogue-dev.udpmarkit.net")

        with patch.object(auth, '_sam_pat_flow', return_value=MagicMock()) as patflow:
            with patch.object(auth, '_sam_app_flow', return_value=MagicMock()) as appflow:
                # hinted APP case, and provided APP
                @benchmark
                def func(): return _pre_request_get_token(env, "APP_USER", "<pass>", "APP", external_session=MagicMock())
                appflow.assert_called()

    def test_pre_request_get_token_hinted_APP_case_and_not_provided_APP(self, benchmark):
        env = _Environment("https://catalogue-dev.udpmarkit.net")

        with patch.object(auth, '_sam_pat_flow', return_value=MagicMock()) as patflow:
            # hinted APP case, and not provided APP
            # we now need to patch requests post to be a 403, as its actually gonna go to the EP
            # Test HTTP 403
            session = MagicMock()
            catalogue_response = Response()
            catalogue_response._content = b'{"access_token": "<JWT3>"}'
            catalogue_response.headers.update({})
            catalogue_response.status_code = 403

            session.post.return_value = catalogue_response

            @benchmark
            def func():
                with pytest.raises(Forbidden) as execinfo:
                    _pre_request_get_token(env, str(uuid.uuid4()), "<pass>", "APP", external_session=session)

    def test_pre_request_get_token_Catalogue_http_status_401(self, benchmark):
        env = _Environment("https://catalogue-dev.udpmarkit.net")

        with patch.object(auth, '_sam_pat_flow', return_value=MagicMock()) as patflow:
            # Test other bad responses from the Catalogue.
            #
            # Test HTTP 401
            session = MagicMock()
            catalogue_response = Response()
            catalogue_response._content = b'{"access_token": "<JWT3>"}'
            catalogue_response.headers.update({})
            catalogue_response.status_code = 401

            session.post.return_value = catalogue_response

            @benchmark
            def func():
                with pytest.raises(Unauthorized) as execinfo:
                    _pre_request_get_token(env, str(uuid.uuid4()), "<pass>", "APP", external_session=session)

    def test_pre_request_get_token_Catalogue_http_status_400(self, benchmark):
        env = _Environment("https://catalogue-dev.udpmarkit.net")

        with patch.object(auth, '_sam_pat_flow', return_value=MagicMock()) as patflow:
            # Test HTTP 400
            session = MagicMock()
            catalogue_response = Response()
            catalogue_response._content = b'{"access_token": "<JWT3>"}'
            catalogue_response.headers.update({})
            catalogue_response.status_code = 400

            session.post.return_value = catalogue_response

            @benchmark
            def func():
                with pytest.raises(BadRequest) as execinfo:
                    _pre_request_get_token(env, str(uuid.uuid4()), "<pass>", "APP", external_session=session)

    def test_pre_request_get_token_catalogue_http_status_500(self, benchmark):
        env = _Environment("https://catalogue-dev.udpmarkit.net")

        with patch.object(auth, '_sam_pat_flow', return_value=MagicMock()) as patflow:
            # Test HTTP 500
            session = MagicMock()
            catalogue_response = Response()
            catalogue_response._content = b'{"access_token": "<JWT3>"}'
            catalogue_response.headers.update({})
            catalogue_response.status_code = 500

            session.post.return_value = catalogue_response

            @benchmark
            def func():
                with pytest.raises(InternalServerError) as execinfo:
                    _pre_request_get_token(env, str(uuid.uuid4()), "<pass>", "APP", external_session=session)

    def test_pre_request_get_token_unhinted_and_not_provided(self, benchmark):
        env = _Environment("https://catalogue-dev.udpmarkit.net")
        auth._sam_pat_flow = MagicMock()
        auth._sam_app_flow = MagicMock()
        auth._decode_token = decode_token
        auth.sam_app_flow = _sam_app_flow
        auth.decode_token = MagicMock()

        session = MagicMock()

        # not provided username/pass
        @benchmark
        def func():
            with pytest.raises(Unauthorized) as execinfo:
                _pre_request_get_token(env, None, None, None, external_session=session)

    def test_pre_request_get_token_unhinted_and_provided_pat(self, benchmark):
        env = _Environment("https://catalogue-dev.udpmarkit.net")
        auth._sam_pat_flow = MagicMock()
        auth._sam_app_flow = MagicMock()
        auth._decode_token = decode_token
        auth.sam_app_flow = _sam_app_flow
        auth.decode_token = MagicMock()

        session = MagicMock()

        # unhinted PAT case, and provided PAT
        @benchmark
        def func(): return _pre_request_get_token(env, str(uuid.uuid4()), "<pass>", None, external_session=session)
        auth._sam_pat_flow.assert_called()

    def test_pre_request_get_token_unhinted_and_provided_jwt(self, benchmark):
        env = _Environment("https://catalogue-dev.udpmarkit.net")
        auth._sam_pat_flow = MagicMock()
        auth._sam_app_flow = MagicMock()
        auth._decode_token = decode_token
        auth.sam_app_flow = _sam_app_flow
        auth.decode_token = MagicMock()

        session = MagicMock()

        # unhinted JWT case, and provided JWT
        jw = jwt.encode(payload={"some": "payload"}, key="secret", algorithm="HS256")
        @benchmark
        def func(): return _pre_request_get_token(env, str(jw), "<pass>", None, external_session=session)
        auth.decode_token.assert_called()

    def test_pre_request_get_token_unhinted_and_provided_app(self, benchmark):
        env = _Environment("https://catalogue-dev.udpmarkit.net")
        auth._sam_pat_flow = MagicMock()
        auth._sam_app_flow = MagicMock()
        auth._decode_token = decode_token
        auth.sam_app_flow = _sam_app_flow
        auth.decode_token = MagicMock()

        session = MagicMock()

        # unhinted APP case, and provided APP
        auth.decode_token = auth._decode_token
        @benchmark
        def func(): return _pre_request_get_token(env, "APP_USER", "<pass>", None, external_session=session)
        auth._sam_app_flow.assert_called()

    def test_pre_request_get_token_unhinted_and_not_valid(self, benchmark):
        env = _Environment("https://catalogue-dev.udpmarkit.net")
        auth._sam_pat_flow = MagicMock()
        auth._sam_app_flow = MagicMock()
        auth._decode_token = decode_token
        auth.sam_app_flow = _sam_app_flow
        auth.decode_token = MagicMock()

        session = MagicMock()

        auth.decode_token = auth._decode_token

        # unhinted case, and not valid
        auth._sam_app_flow = auth.sam_app_flow

        @benchmark
        def func():
            with pytest.raises(Unauthorized) as execinfo:
                _pre_request_get_token(env, "<user>", "<pass>", None, external_session=session)

    random_key_strategy = st.text().filter(lambda x: not x.startswith('oidc_id_token'))
    value_strategy = st.text()
    key_value_strategy = st.tuples(random_key_strategy, value_strategy).map(lambda x: f'{x[0]}={x[1]}')

    @hypothesis.example(cookies=None)
    @hypothesis.example(cookies='')  # empty string in cookie
    @hypothesis.example(cookies=';')
    @hypothesis.example(cookies='a')
    @hypothesis.example(cookies='a=b')  # Not the correct key name (`oidc_id_token`)
    @hypothesis.example(cookies='oidc_id_token')  # Correct key name but no partition or value
    @hypothesis.example(cookies='oidc_id_token=')  # Correct key name and has partition but no value
    @hypothesis.given(
        cookies=st.one_of(
            st.none(),
            st.lists(st.one_of(random_key_strategy, key_value_strategy)).map(lambda x: ';'.join(x)),
        ),
    )
    def test_extract_jwt_from_cookie_without_auth_cookie(self, cookies: Optional[List[str]]):
        assert ServiceMiddleware.extract_jwt_from_cookie(environ={'HTTP_COOKIE': cookies}) is None

    @hypothesis.example(auth_cookie='oidc_id_token=jwt', random=[])
    @hypothesis.example(auth_cookie='oidc_id_token=jwt', random=['a=b'])
    @hypothesis.example(auth_cookie=' oidc_id_token=jwt', random=['a=b'])  # Space before key name
    @hypothesis.given(
        auth_cookie=st.text(min_size=1).map(lambda token: f'oidc_id_token={token}'),
        random=st.lists(st.one_of(random_key_strategy, key_value_strategy)),
    )
    def test_extract_jwt_from_cookie_with_auth_cookie(self, auth_cookie: str, random: List[str]):
        random.append(auth_cookie)
        cookies = ';'.join(random)
        assert ServiceMiddleware.extract_jwt_from_cookie(environ={'HTTP_COOKIE': cookies}) is not None

    def test_benchmark_extract_jwt_from_cookie_with_auth_cookie(self, benchmark):
        auth_cookie = ' oidc_id_token=jwt'
        random = ['a=b', auth_cookie]
        cookies = ';'.join(random)
        @benchmark
        def func(): return ServiceMiddleware.extract_jwt_from_cookie(environ={'HTTP_COOKIE': cookies})
