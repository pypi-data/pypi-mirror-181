from yapygen.gen import generate_project
from yapygen.meta import get_meta


def main():
    meta = get_meta()
    generate_project(meta)


if __name__ == "__main__":
    main()
