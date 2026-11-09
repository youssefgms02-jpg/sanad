import unittest

from auth_utils import hash_password, verify_password, hash_session_token, new_session_token


class AuthUtilsTests(unittest.TestCase):
    def test_password_hash_is_salted_and_verifiable(self):
        first = hash_password("A-secure-example-password")
        second = hash_password("A-secure-example-password")
        self.assertNotEqual(first, second)
        self.assertTrue(verify_password("A-secure-example-password", first))
        self.assertFalse(verify_password("wrong-password", first))

    def test_session_tokens_are_random_and_hashed(self):
        first = new_session_token()
        second = new_session_token()
        self.assertNotEqual(first, second)
        self.assertNotEqual(first, hash_session_token(first))
        self.assertEqual(hash_session_token(first), hash_session_token(first))


if __name__ == "__main__":
    unittest.main()
