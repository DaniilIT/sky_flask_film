import json

class TestUsersView:
    def test_user_get(self, client, tokens):
        response = client.get(
            '/user/',
            headers={'Authorization': f'Bearer {tokens["access_token"]}'}
        )

        assert response.status_code == 200
        data = response.json
        assert 'email' in data
        assert 'name' in data
        assert "password" not in data
        assert data['email'] == 'example@mail.ru'

    def test_user_patch(self, client, tokens):
        response = client.patch(
            '/user/',
            headers={'Authorization': f'Bearer {tokens["access_token"]}'},
            data=json.dumps({'name': 'Петр'}),
            content_type='application/json',
        )

        assert response.status_code == 204

        response = client.get(
            '/user/',
            headers={'Authorization': f'Bearer {tokens["access_token"]}'}
        )

        data = response.json
        assert data['name'] == 'Петр'

    def test_user_change_password(self, client, tokens):
        response = client.put(
            '/user/password/',
            headers={'Authorization': f'Bearer {tokens["access_token"]}'},
            data=json.dumps({
                'old_password': '1Aa#2Bb#3Cc#',
                'new_password': '1Aa#2Bb#3Cc#4Dd#',
            }),
            content_type='application/json',
        )

        assert response.status_code == 204
