import requests
from allauth.socialaccount import app_settings
from allauth.socialaccount.providers.oauth2.views import (
    OAuth2Adapter,
    OAuth2CallbackView,
    OAuth2LoginView,
)

from .provider import DubClubProvider


class DubClubOAuth2Adapter(OAuth2Adapter):
    provider_id = DubClubProvider.id

    @property
    def base_url(self):
        settings = app_settings.PROVIDERS.get(self.provider_id, {})
        server_url = settings.get("SERVER_URL")

        if not server_url:
            return "https://dubclub.win"

        return server_url.rstrip("/")

    @property
    def access_token_url(self):
        return "%s/oauth/token/" % self.base_url

    @property
    def authorize_url(self):
        return "%s/oauth/authorize" % self.base_url

    @property
    def profile_url(self):
        return "%s/oauth/userinfo" % self.base_url

    def complete_login(self, request, app, token, **kwargs):
        resp = requests.get(
            self.profile_url,
            params={"access_token": token.token},
        )
        resp.raise_for_status()
        extra_data = resp.json()
        return self.get_provider().sociallogin_from_response(request, extra_data)


oauth2_login = OAuth2LoginView.adapter_view(DubClubOAuth2Adapter)
oauth2_callback = OAuth2CallbackView.adapter_view(DubClubOAuth2Adapter)
