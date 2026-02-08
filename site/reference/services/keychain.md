# Keychain

The Keychain service provides secure storage for passwords, API tokens, and other sensitive data using the macOS Keychain. Data is encrypted at rest and protected by the system. Access it via `app.keychain`.

```python
# Store a credential
app.keychain.set("MyApp", "api_token", "sk-abc123")

# Retrieve it later
token = app.keychain.get("MyApp", "api_token")
```

## Methods

### `get(service, account)`

Retrieve a password from the keychain.

```python
app.keychain.get(service: str, account: str) -> str | None
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `service` | `str` | Service name, typically your app identifier (e.g., `"com.myapp"`) |
| `account` | `str` | Account name (username, email, or key identifier) |

Returns the stored password as a string, or `None` if no matching entry exists.

### `set(service, account, password)`

Store a password in the keychain. If an entry already exists for the given service/account combination, it is updated.

```python
app.keychain.set(service: str, account: str, password: str) -> bool
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `service` | `str` | Service name |
| `account` | `str` | Account name |
| `password` | `str` | The password or secret to store |

Returns `True` if stored successfully.

### `delete(service, account)`

Delete a password from the keychain.

```python
app.keychain.delete(service: str, account: str) -> bool
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `service` | `str` | Service name |
| `account` | `str` | Account name |

Returns `True` if deleted successfully.

### `exists(service, account)`

Check whether a keychain entry exists without retrieving its value.

```python
app.keychain.exists(service: str, account: str) -> bool
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `service` | `str` | Service name |
| `account` | `str` | Account name |

Returns `True` if the entry exists, `False` otherwise.

---

## Examples

### Store and retrieve an API token

```python
import nib

def main(app: nib.App):
    app.title = "Keychain"
    app.icon = nib.SFSymbol("key.fill")
    app.width = 340
    app.height = 250

    SERVICE = "com.myapp"
    ACCOUNT = "api_token"

    token_field = nib.SecureField(placeholder="Enter API token")
    status = nib.Text("", foreground_color=nib.Color.SECONDARY)

    def save_token():
        if token_field.text:
            success = app.keychain.set(SERVICE, ACCOUNT, token_field.text)
            status.content = "Saved!" if success else "Failed to save"
        else:
            status.content = "Enter a token first"

    def load_token():
        token = app.keychain.get(SERVICE, ACCOUNT)
        if token:
            status.content = f"Token: {token[:8]}..."
        else:
            status.content = "No token stored"

    def delete_token():
        success = app.keychain.delete(SERVICE, ACCOUNT)
        status.content = "Deleted" if success else "Nothing to delete"

    app.on_appear = load_token

    app.build(
        nib.VStack(
            controls=[
                nib.Text("API Token Manager", font=nib.Font.HEADLINE),
                token_field,
                nib.HStack(
                    controls=[
                        nib.Button("Save", action=save_token, style=nib.ButtonStyle.BORDERED_PROMINENT),
                        nib.Button("Load", action=load_token, style=nib.ButtonStyle.BORDERED),
                        nib.Button("Delete", action=delete_token, role=nib.ButtonRole.DESTRUCTIVE),
                    ],
                    spacing=8,
                ),
                status,
            ],
            spacing=12,
            padding=20,
        )
    )

nib.run(main)
```

### Login form with keychain persistence

```python
import nib

def main(app: nib.App):
    app.title = "Login"
    app.icon = nib.SFSymbol("person.crop.circle")
    app.width = 320
    app.height = 220

    SERVICE = "com.myapp.login"

    username = nib.TextField(placeholder="Username")
    password = nib.SecureField(placeholder="Password")
    status = nib.Text("", foreground_color=nib.Color.SECONDARY)

    def login():
        if username.text and password.text:
            # Save credentials for next session
            app.keychain.set(SERVICE, "username", username.text)
            app.keychain.set(SERVICE, "password", password.text)
            status.content = f"Logged in as {username.text}"

    def load_saved():
        saved_user = app.keychain.get(SERVICE, "username")
        if saved_user:
            username.text = saved_user
            status.content = "Loaded saved credentials"

    app.on_appear = load_saved

    app.build(
        nib.Form(
            controls=[
                username,
                password,
                nib.Button("Login", action=login, style=nib.ButtonStyle.BORDERED_PROMINENT),
                status,
            ],
            padding=20,
        )
    )

nib.run(main)
```
