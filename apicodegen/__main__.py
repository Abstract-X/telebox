from apicodegen.documentation.documentation import get_documentation
from apicodegen.generation.generation import create_code


def main() -> None:
    documentation = get_documentation()
    create_code(documentation)


if __name__ == "__main__":
    main()
