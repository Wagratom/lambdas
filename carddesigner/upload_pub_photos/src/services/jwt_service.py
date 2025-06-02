import jwt
from src.exceptions.jwt_exceptions import jwtException

class JwtService:
    def decode_jwt(self, jwt_token):
        """
        Função responsavel por decodificar um token JWT
        e retornar o subject do token

        Args:
            jwt_token (string): token JWT a ser decodificado

        Raises:
            jwtException: _raises jwtException if the token is invalid or expired

        Returns:
            dict: _payload do token JWT
        """
        try:
            if jwt_token.startswith("Bearer "):
                jwt_token = jwt_token[7:]

            decoder = jwt.decode(jwt_token, options={"verify_signature": False})
            sub = decoder.get("sub")
            if not sub:
                raise jwtException("Token does not contain 'sub' field")
            return sub
        except jwt.ExpiredSignatureError:
            raise jwtException("Token has expired")
        except jwt.InvalidTokenError:
            raise jwtException("Invalid token")
