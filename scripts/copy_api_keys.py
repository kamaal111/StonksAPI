from pathlib import Path


env_file = Path(".env")
api_keys_file = Path("secrets/app-api-keys.json")


def create_env_file_if_not_exists():
    if not env_file.exists():
        env_file.write_text("")


def main():
    api_keys_file_text = api_keys_file.read_text()
    create_env_file_if_not_exists()
    env_file_text = env_file.read_text().splitlines()
    api_keys_index: int | None = None
    for index, line in env_file_text:
        if line.startswith("APP_API_KEYS"):
            api_keys_index = index
            break

    if api_keys_index is not None:
        env_file_text[api_keys_index] = f'APP_API_KEYS="{api_keys_file_text}"'
    else:
        env_file_text.append(f'APP_API_KEYS="{(api_keys_file_text.replace(" ", ""))}"')
    print(env_file_text)


if __name__ == "__main__":
    main()
