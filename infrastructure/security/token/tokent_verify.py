from domain.security.service import TokenVerifyService
from infrastructure.security.token.requester import TokenRequester


class TokenVerify:

    def __init___(
            self,
            verify_provider: TokenVerifyService,
            token_decoder: TokenRequester
    ):
        self.verify_provider = verify_provider
        self.token_decoder = token_decoder

    def verify(self, token: str) -> bool:
        return self.verify_provider.verify(token, self.token_decoder)

    @classmethod
    def create(
            cls,
            verify_provider: TokenVerifyService,
            token_decoder: TokenRequester
    ):
        return cls(verify_provider, token_decoder)
