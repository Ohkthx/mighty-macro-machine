from script import Script
from lang import Engine


def main():
    """Main entry point of the application."""
    # script = Script.create_default("hello_world.mx3")
    script = Script.load_script("hello_world.mx3")

    engine = Engine(script.code)
    engine.run()


if __name__ == "__main__":
    main()
